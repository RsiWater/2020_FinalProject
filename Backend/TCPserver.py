import socket
from PackageHandler import *
from db_class_account import Account
from db_class_schedule import Schedule

hostname = '127.0.0.1' #設定主機名
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
    rcv_event = connect_socket.recv(1024)
    
    packageType = rcv_event[:3].decode('UTF-8')
    if packageType == 'acc':
        rcv_package = decodeAccountPackage(rcv_event[3:])

        print(rcv_package.get_status())
        connect_socket.send(encodeAccountPackage(account))

    elif packageType == 'sch':
        rcv_package = decodeSchedulePackage(rcv_event[3:])

        print(rcv_package.get_todo())
        connect_socket.send(encodeSchedulePackage(schedule))

    connect_socket.close()

