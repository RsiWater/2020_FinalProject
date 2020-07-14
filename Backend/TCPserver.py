import socket
from ProgressThread import *
# from PackageHandler import *
# from db_class_account import Account
# from db_class_schedule import Schedule
# from DB_Classes import *

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='life-8c6775870f64.json'

hostname = "192.168.203.108" #設定主機名
port = 6666  #設定埠號 要確保這個埠號沒有被使用，可以在cmd裡面檢視
addr = (hostname,port)
srv = socket.socket() #建立一個socket
srv.bind(addr)
srv.listen(5)
print("Waitting the connection.")

#
account = Account()
account.set_day(10)
account.set_month(6)
account.set_year(20)
account.randomize_number()
account.set_money(100)
account.set_item("你好")
account.set_detail("嗯嗯嗯")
account.set_status(1)

#
schedule = Schedule()
schedule.randomize_number()
schedule.set_todo("今天天氣真好")
schedule.set_year(30)
schedule.set_month(3)
schedule.set_day(21)
schedule.set_start(0)
schedule.set_end(124)
#

while True:
    connect_socket, client_addr = srv.accept()
    print(client_addr)

    childThread = ProgressThread(connect_socket, client_addr)
    childThread.start()