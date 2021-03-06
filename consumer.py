import pika
import ast
from  ChatlogManager import Chatlog

class Receive(object):
    def __init__(self, callbackf , binding_key, exchange):
        self._binding_key = binding_key
       # Makes connection to given link
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        # Creates channel out of the connection
        self._channel = self._connection.channel()
        # declare exchange and exchange type
        self._channel.exchange_declare(exchange = exchange , exchange_type = 'direct')
        
        # Get result to later get temp queue name
        # durable = True means data won't be lost 
        self.result = self._channel.queue_declare(queue= '', durable = True)
        # Makes a temporary queue
        self.q_name = self.result.method.queue
        # Binds this queue to exchange
        self._channel.queue_bind(exchange =exchange , queue = self.q_name , routing_key = self._binding_key)
        # Specifies which q to consume from and calls the function mentioned 
        self._channel.basic_consume(queue= self.q_name, on_message_callback = callbackf)
   
    def consume(self):
        print("[O] Waiting for message")
        # makes sure one task is completed before taking another
        self._channel.basic_qos(prefetch_count = 1)
        # Starts accepting tasks
        self._channel.start_consuming()




def callback(ch, method, properties, body ):
    
    
    try :
        clm = Chatlog()
        obj = ast.literal_eval(body.decode('utf-8'))
        clm.save_message(obj);
        print(obj)

        print("[o] recived and saved  %r"%body)
    except Exception as e:
        print('Some problem has occured ')
        print(e) 
    
    
if __name__ == '__main__':
    print('Recive form ?')
    binding_key = input()
    rb = Receive(exchange='mydirex', binding_key= binding_key,callbackf=callback)
    rb.consume()