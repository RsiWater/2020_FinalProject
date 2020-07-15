import os
import socket
import json
import Crawl
from ProgressThread import *


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='life-8c6775870f64.json'

# Crawl.writeData()

weatherData = dict()
try:
    with open('weatherData.json', 'r') as fp:
        weatherData = json.load(fp)
except:
    Crawl.writeData()
    with open('weatherData.json', 'r') as fp:
        weatherData = json.load(fp)

print(weatherData.keys())


hostname = "192.168.203.108" #設定主機名
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
    childThread.setWeatherData(weatherData)
    childThread.start()