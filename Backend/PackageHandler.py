from DB_Classes import *
from dialogflow_f import *
import Crawl

def classifyPackage(package):
    packageType = package[:3].decode("utf-8")
    
    if packageType == 'acc':
        send_package=bytes('',encoding='utf-8')
        rcv_package = decodeAccountPackage(package[3:])
        rcv_package.operateAction()
        if rcv_package.operationCode==3:
            for data in rcv_package.findAll:
                rcv_package.set_money(data[0])
                rcv_package.set_year(data[1])
                rcv_package.set_month(data[2])
                rcv_package.set_day(data[3])
                rcv_package.set_item(data[4])
                rcv_package.set_detail(data[5])
                rcv_package.set_receipt(data[6])
                rcv_package.set_note(data[7])
                rcv_package.set_status(data[8])
                rcv_package.set_key(data[9])
                rcv_package.set_user(data[10])
                send_package+=encodeAccountPackage(rcv_package)
            return send_package

        # connect_socket.send(encodeAccountPackage(account))

    elif packageType == 'sch':
        send_package=bytes('',encoding='utf-8')
        rcv_package = decodeSchedulePackage(package[3:])
        rcv_package.operateAction()
        if rcv_package.operationCode==3:
            for data in rcv_package.findAll:
                rcv_package.set_todo(data[0])
                rcv_package.set_year(data[1])
                rcv_package.set_month(data[2])
                rcv_package.set_day(data[3])
                rcv_package.set_start(data[4])
                rcv_package.set_end(data[5])
                rcv_package.set_key(data[6])
                rcv_package.set_user(data[7])
                send_package+=encodeSchedulePackage(rcv_package)
            return send_package

        # print(rcv_package.get_todo())
        # connect_socket.send(encodeSchedulePackage(schedule))

    elif packageType == 'wea':
        send_package = bytes('', encoding="UTF-8")
        weatherData = Crawl.getWeatherData()
        for eleList in weatherData.values():
            for ele in eleList:
                send_package+=encodeWeatherPackage(ele)
        # 
        return send_package

    elif packageType=='sen':
        send_package=Sentence(package[3:])
        return send_package

    elif packageType=='rec':
        #need crawl
        checkNumber=[]
        send_package=receiptSearch(checkNumber,package[3:])
        return send_package

    elif packageType == 'log':
        # login
        rcv_package = decodeLoginPackage(package[3:])
        if(rcv_package.check()):
            return "logAccepted".encode("UTF-8")
        else:
            return "logRejected".encode("UTF-8")
        

    # elif packageType == 'deb':
    #     message = rcv_event.decode("UTF-8")
    #     print(message)


def decodeLoginPackage(package):
    resultAccount = UserAccount()
    resultAccount.name = package[:20].decode('utf-8').split('\x00', 1)[0]
    resultAccount.password = package[20:].decode('utf-8').split('\x00', 1)[0]

    return resultAccount

def encodeAccountPackage(accountClass): # return bytearray

    package, zero, itemSize, userSize = 0, 0, 18, 20
    
    package = bytes("acc", encoding='utf-8')
    package += accountClass.get_key().to_bytes(4, 'big')
    package += accountClass.get_money().to_bytes(4, 'big')
    package += accountClass.get_year().to_bytes(1, 'big')
    package += accountClass.get_month().to_bytes(1, 'big')
    package += accountClass.get_day().to_bytes(1,'big')
   
    package += bytes(accountClass.get_item(), encoding = "UTF-8")
    package += zero.to_bytes(itemSize - (len(accountClass.get_item() * 3)), 'big')
    package += bytes(accountClass.get_detail(), encoding = "UTF-8")
    package += zero.to_bytes(itemSize - (len(accountClass.get_detail()) * 3), 'big')
    package += accountClass.get_status().to_bytes(1, 'big')
    package += bytes(accountClass.get_user(),encoding='UTF-8')
    package += zero.to_bytes(userSize - (len(accountClass.get_user())), 'big')
    
    # print(package)
    # for i in package:
    #     print(i)

    return package

def decodeAccountPackage(package): # return AccountClass
    
    resultAccount = Account()
    
    p_id, p_money, p_year , p_month= int.from_bytes(package[:4], 'big'), int.from_bytes(package[4:8],'big'), package[8], package[9]
    p_day, p_item, p_detail, p_status = package[10], package[11:29].decode('utf-8').split('\x00', 1)[0], package[29:47].decode('utf-8').split('\x00', 1)[0], package[47]
    p_operationCode, p_user = package[48], package[49:68].decode('utf-8').split('\x00', 1)[0]

    resultAccount.set_key(p_id)
    resultAccount.set_money(p_money)
    resultAccount.set_year(p_year)
    resultAccount.set_month(p_month)
    resultAccount.set_day(p_day)
    resultAccount.set_item(p_item)
    resultAccount.set_detail(p_detail)
    resultAccount.set_status(p_status)
    resultAccount.set_operationCode(p_operationCode)
    resultAccount.set_user(p_user)

    #
    # resultAccount.set_receipt("898")
    # resultAccount.set_note("testest")
    #


    # update resultAccount.

    return resultAccount


def encodeSchedulePackage(scheduleClass): # return bytearray

    package, zero, todo_size, userSize = 0, 0, 36, 20
    
    package = bytes("sch", encoding='utf-8')
    package += scheduleClass.get_key().to_bytes(4,'big')
    package += bytes(scheduleClass.get_todo(), encoding='UTF-8')
    package += zero.to_bytes(todo_size - (len(scheduleClass.get_todo() * 3)), 'big')
    package += scheduleClass.get_year().to_bytes(1, 'big')
    package += scheduleClass.get_month().to_bytes(1, 'big')
    package += scheduleClass.get_day().to_bytes(1, 'big')
    package += scheduleClass.get_start().to_bytes(4, 'big')
    package += scheduleClass.get_end().to_bytes(4, 'big')
    package += bytes(scheduleClass.get_user,encoding='UTF-8')
    package += zero.to_bytes(userSize - (len(scheduleClass.get_todo())), 'big')

    return package

def decodeSchedulePackage(package): # return AccountClass
    
    resultSchedule = Schedule()
    
    p_id, p_todo, p_year , p_month= int.from_bytes(package[:4], 'big'), package[4:40].decode('utf-8'), package[40], package[41]
    p_day, p_start, p_end = package[42], int.from_bytes(package[43:47], 'big'), int.from_bytes(package[47:51], 'big')
    p_user=package[52:71].decode('utf-8')
    
    resultSchedule.set_key(p_id)
    resultSchedule.set_todo(p_todo)
    resultSchedule.set_year(p_year)
    resultSchedule.set_month(p_month)
    resultSchedule.set_day(p_day)
    resultSchedule.set_start(p_start)
    resultSchedule.set_end(p_end)
    resultSchedule.set_user(p_user)

    # update resultAccount

    return resultSchedule

def encodeWeatherPackage(weatherClass):
    
    package, zero, city_size, period_size, situation_size = 0, 0, 12, 12, 45
    
    package = bytes("wea", encoding='utf-8')
    package += weatherClass.get_month().to_bytes(1, 'big')
    package += weatherClass.get_day().to_bytes(1, 'big')
    package += bytes(weatherClass.get_city(), encoding= 'UTF-8')
    package += zero.to_bytes(city_size - (len(weatherClass.get_city()) * 3), 'big')
    package += bytes(weatherClass.get_period(), encoding= 'UTF-8')
    package += zero.to_bytes(period_size - (len(weatherClass.get_period()) * 3), 'big')
    package += bytes(weatherClass.get_situation(), encoding= 'UTF-8')
    package += zero.to_bytes(situation_size - (len(weatherClass.get_situation()) * 3), 'big')
    package += weatherClass.get_max_temperature().to_bytes(1, 'big')
    package += weatherClass.get_min_temperature().to_bytes(1, 'big')

    return package

def Sentence(package):  #return bytearray

    send_package=0
    p_sentence=package[:75].decode('utf-8').split('\x00', 1)[0]
    number=random.randint(0,1000)
    response=dialogflow_f.detect_texts('life-nxuajt',str(number),p_sentence,'zh-TW')
    send_package=bytes("sen", encoding='UTF-8')
    send_package+=bytes(response.query_result.intent.display_name,encoding='UTF-8')
    send_package+=bytes(response.query_result.fulfillment_text ,encoding='UTF-8')

    return send_package

def receiptSearch(checkNumber,package):
    p_user=package[:20].decode('utf-8').split('\x00', 1)[0]
    checkAccount=Account()
    checkAccount.set_user(p_user)
    checkAccount.select()
    send_package=bytes('',encoding='utf-8')
    for i in checkNumber:
        for data in checkAccount.findAll:
            if data[6]==i:
                checkAccount.set_money(data[0])
                checkAccount.set_year(data[1])
                checkAccount.set_month(data[2])
                checkAccount.set_day(data[3])
                checkAccount.set_item(data[4])
                checkAccount.set_detail(data[5])
                checkAccount.set_receipt(data[6])
                checkAccount.set_note(data[7])
                checkAccount.set_status(data[8])
                checkAccount.set_key(data[9])
                checkAccount.set_user(data[10])
                send_package+=encodeAccountPackage(checkAccount)
    return send_package

                

