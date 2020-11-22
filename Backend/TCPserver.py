import os
import socket
import json
import Crawl
from UpdateThread import *
from ProgressThread import *


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='life-8c6775870f64.json'

# hostname = "localhost"
hostname = "192.168.203.101"
port = 6666  
addr = (hostname,port)
srv = socket.socket()
srv.bind(addr)
srv.listen(5)

updateThread = UpdateThread()
updateThread.start()

print("Waitting the connection.")
while True:
    connect_socket, client_addr = srv.accept()
    print(client_addr)

    childThread = ProgressThread(connect_socket, client_addr)
    childThread.start()