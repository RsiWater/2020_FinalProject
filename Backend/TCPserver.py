import socket
import os
from ProgressThread import *
# from PackageHandler import *
# from db_class_account import Account
# from db_class_schedule import Schedule
# from DB_Classes import *

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='life-8c6775870f64.json'


hostname = '127.0.0.1' #設定主機名
port = 6666  #設定埠號 要確保這個埠號沒有被使用，可以在cmd裡面檢視
addr = (hostname,port)
srv = socket.socket() #建立一個socket
srv.bind(addr)
srv.listen(5)
print("Waitting the connection.")

while True:
    connect_socket, client_addr = srv.accept()
    print(client_addr)

    childThread = ProgressThread(connect_socket, client_addr)
    childThread.start()