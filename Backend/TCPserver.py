import os
import socket
import json
import Crawl
from UpdateThread import *
from ProgressThread import *


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='life-8c6775870f64.json'

# Crawl.checkDate()
# Crawl.writeData()

hostname = "192.168.203.112" #設定主機名
port = 6666  #設定埠號 要確保這個埠號沒有被使用，可以在cmd裡面檢視
addr = (hostname,port)
srv = socket.socket() #建立一個socket
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