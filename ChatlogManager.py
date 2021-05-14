from csv import DictWriter
from csv import DictReader
import os
class Chatlog(object):
    def __init__(self):
       self._file_name = 'chatlog.csv'
    def save_message(self,message):
        with open(self._file_name,'a' ,newline= '') as cl:   
            # Write keys as field names
            f_names = list(message.keys())
            
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = DictWriter(cl, fieldnames = f_names)
            #writes header if not present
            if(os.path.getsize('chatlog.csv')==0):
                writer_object.writeheader()
            
            writer_object.writerow(message)
            cl.close()
    
    def read_chat(self):
        with open(self._file_name,'r') as cl:
            reader_object = DictReader(cl)
            msg_list = list(reader_object)
            size_msg_list = len(msg_list)
            if(size_msg_list>=10):
                msg_list = msg_list[-10:]
                for row in msg_list:
                    print(row)
            else:
                for row in msg_list:
                    print(row)
    
        
        
if (__name__ == '__main__'):
    a = Chatlog()
    a.save_message({'name':'Priyanshi10','txt':'Hello my, frnd "Avi" '})
    a.read_chat()