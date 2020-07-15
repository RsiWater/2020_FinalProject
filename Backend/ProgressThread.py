import threading
import time
from PackageHandler import *
# from db_class_account import *

class ProgressThread(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.connect_socket = socket
        self.address = address
        self.weatherData = None
    
    def setWeatherData(self, data):
        self.weatherData = data

    def run(self):
        rcv_event = self.connect_socket.recv(1024)
        # identify user.
        
        # receive package
        send_package = classifyPackage(rcv_event)
        if send_package != None :
            self.connect_socket.send(send_package)
        elif send_package == 'wea':
            send_package = list()
            for ele in self.weatherData:
                send_package.append(encodeWeatherPackage(ele))
            # 
            for ele in send_package:
                print(ele)
        else:
            self.connect_socket.send("package received.".encode('UTF-8'))


        self.connect_socket.close()


    


