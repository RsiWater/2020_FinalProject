import os
import socket
import json
import Crawl
from UpdateThread import *
from ProgressThread import *


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='life-8c6775870f64.json'

hostname = "10.1.202.145"
# hostname = "172.20.10.8"
# hostname = "218.166.235.74"
# hostname = "192.168.1.55"
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