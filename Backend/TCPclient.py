import socket
hostname = "192.168.203.108"
port = 6666
addr = (hostname,port)
print(hostname)
clientsock = socket.socket() ## 建立一個socket
clientsock.connect(addr) # 建立連線
say = input("輸入你想傳送的訊息：")
clientsock.send(bytes(say,encoding='gbk')) #傳送訊息
recvdata = clientsock.recv(1024)  #接收訊息 recvdata 是bytes形式的
print(str(recvdata,encoding='gbk')) # 我們看不懂bytes，所以轉化為 str
clientsock.close()