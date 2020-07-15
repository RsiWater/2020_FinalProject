import threading
import time
from PackageHandler import *
# from db_class_account import *

class ProgressThread(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.connect_socket = socket
        self.address = address

    def run(self):
        rcv_event = self.connect_socket.recv(1024)
        # identify user.
        
        # receive package
        send_package = classifyPackage(rcv_event)
        if send_package != None :
            self.connect_socket.send(send_package)
        else:
            self.connect_socket.send("package received.".encode('UTF-8'))


        self.connect_socket.close()


    


