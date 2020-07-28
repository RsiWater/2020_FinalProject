from DB_Classes import *
from dialogflow_f import *
import Crawl
import response_judge
import hashlib

def classifyPackage(package):
    packageType = package[:3].decode("utf-8")
    
    if packageType == 'acc':
        print("accc")
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
        checkNumber=Crawl.receiptCrawler()
        send_package=receiptSearch(checkNumber,package[3:])
        return send_package

    elif packageType == 'log':
        # login
        rcv_package = decodeLoginPackage(package[3:])
        
        send_package = encodeLoginMessage(rcv_package)
        return send_package
        

    # elif packageType == 'deb':
    #     message = rcv_event.decode("UTF-8")
    #     print(message)

def encodeLoginMessage(userClass):    
    zero, passSize, keySize = 0, 2, 64

    package = bytes("log", encoding="UTF-8")
    if(userClass.check()):
        package += bytes("OK", encoding="UTF-8")
        package += bytes(userClass.key, encoding="UTF-8")
    else:
        package += bytes("NO", encoding="UTF-8")
        package += bytes(SHA256_encode("NULL"), encoding="UTF-8")
    
    return package
    

def decodeLoginPackage(package):
    resultAccount = UserAccount()
    resultAccount.name = package[:20].decode('utf-8').split('\x00', 1)[0]
    resultAccount.password = package[20:].decode('utf-8').split('\x00', 1)[0]
    resultAccount.key = SHA256_encode(resultAccount.name)

    resultAccount.updateKey(resultAccount.key)

    return resultAccount

def encodeAccountPackage(accountClass): # return bytearray

    package, zero, itemSize, detailSize, receiptSize, noteSize, userSize = 0, 0, 18, 18, 2, 90, 20
    
    package = bytes("acc", encoding='utf-8')
    package += accountClass.get_key().to_bytes(4, 'big')
    package += accountClass.get_money().to_bytes(4, 'big')
    package += accountClass.get_year().to_bytes(4, 'big')
    package += accountClass.get_month().to_bytes(1, 'big')
    package += accountClass.get_day().to_bytes(1,'big')
   
    package += bytes(accountClass.get_item(), encoding = "UTF-8")
    package += zero.to_bytes(itemSize - (len(accountClass.get_item().encode('UTF-8'))), 'big')
    package += bytes(accountClass.get_detail(), encoding = "UTF-8")
    package += zero.to_bytes(detailSize - (len(accountClass.get_detail().encode('UTF-8'))), 'big')
    
    package += bytes(accountClass.get_receipt(), encoding = "UTF-8")
    package += zero.to_bytes(receiptSize - (len(accountClass.get_receipt().encode('UTF-8'))), 'big')
    package += bytes(accountClass.get_note(), encoding = "UTF-8")
    package += zero.to_bytes(noteSize - (len(accountClass.get_note().encode('UTF-8'))), 'big')

    package += accountClass.get_status().to_bytes(1, 'big')
    package += accountClass.get_operaionCode().to_bytes(1, 'big')
    package += bytes(accountClass.get_user(),encoding='UTF-8')
    package += zero.to_bytes(userSize - (len(accountClass.get_user())), 'big')
    
    # print(package)
    # for i in package:
    #     print(i)

    return package

def decodeAccountPackage(package): # return AccountClass
    
    resultAccount = Account()
    
    p_id, p_money, p_year , p_month= int.from_bytes(package[:4], 'big'), int.from_bytes(package[4:8],'big'), int.from_bytes(package[8:12], 'big'), package[12]
    p_day, p_item, p_detail, p_receipt, p_note, p_status = package[13], package[14:32].decode('utf-8').split('\x00', 1)[0], package[32:50].decode('utf-8').split('\x00', 1)[0], package[50:52].decode('utf-8').split('\x00', 1)[0], package[52:142].decode('utf-8').split('\x00', 1)[0], package[142]
    p_operationCode, p_user = package[143], package[144:164].decode('utf-8').split('\x00', 1)[0]

    resultAccount.set_key(p_id)
    resultAccount.set_money(p_money)
    resultAccount.set_year(p_year)
    resultAccount.set_month(p_month)
    resultAccount.set_day(p_day)
    resultAccount.set_item(p_item)
    resultAccount.set_detail(p_detail)
    resultAccount.set_receipt(p_receipt)
    resultAccount.set_note(p_note)
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
    package += zero.to_bytes(todo_size - (len(scheduleClass.get_todo().encode('UTF-8'))), 'big')
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
    package += zero.to_bytes(city_size - (len(weatherClass.get_city().encode("UTF-8"))), 'big')
    package += bytes(weatherClass.get_period(), encoding= 'UTF-8')
    package += zero.to_bytes(period_size - (len(weatherClass.get_period().encode("UTF-8"))), 'big')
    package += bytes(weatherClass.get_situation(), encoding= 'UTF-8')
    package += zero.to_bytes(situation_size - (len(weatherClass.get_situation().encode("UTF-8"))), 'big')
    package += weatherClass.get_max_temperature().to_bytes(1, 'big')
    package += weatherClass.get_min_temperature().to_bytes(1, 'big')

    return package

def Sentence(package):  #return bytearray
    fulfillment_size, zero = 90, 0

    send_package,intent,operate,fulfillment=0,0,0,''
    p_intent,p_operate,p_sentence=int.from_bytes(package[:4], 'big'),int.from_bytes(package[4:8], 'big'),package[8:98].decode('utf-8').split('\x00', 1)[0]
    if p_intent==0:
        number=random.randint(0,1000)
        response=detect_texts('life-nxuajt',str(number),p_sentence,'zh-TW')
        intent,operate=response_judge.judge(response)
        # 一段式
        fulfillment=response.query_result.fulfillment_text
    if p_intent==1:
        # 記帳
        if p_operate==1:
            # 新增
            year,month,day,item,detail,money,status,key,user,errorFlag=response_judge.cutSentenceAccount(p_sentence)
            if errorFlag==False:
                setAccount=Account()
                setAccount.set_year(int(str(year)[2:4]))
                setAccount.set_month(month)
                setAccount.set_day(day)
                setAccount.set_item(item)
                setAccount.set_detail(detail)
                setAccount.set_money(money)
                setAccount.set_status(status)
                setAccount.set_key(key)
                setAccount.set_user(user)
                setAccount.insert()
                fulfillment='已新增'
            else:
                fulfillment='請重新輸入'
        elif p_operate==2:
            # 刪除
            pass
        elif p_operate==3:
            # 修改
            pass
        elif p_operate==4:
            # 查詢
            pass
        intent=0
        operate=0
    if p_intent==2:
        # 行程
        if p_operate==1:
            # 新增
            todo,key,user,yearList,monthList,dayList,h,m=response_judge.cutSentenceSchedule_add(p_sentence)
            setSchedule=Schedule()
            setSchedule.set_todo(todo)
            setSchedule.set_key(key)
            setSchedule.set_user(user)
            setSchedule.set_start_in_format(yearList[0],monthList[0],dayList[0],h[0],m[0])
            setSchedule.set_end_in_format(yearList[len(yearList)-1],monthList[len(monthList)-1],dayList[len(dayList)-1],h[len(h)-1],m[len(m)-1])
            setSchedule.insert()
            fulfillment='已新增'
        elif p_operate==2:
            # 刪除
            pass
        elif p_operate==3:
            # 修改
            pass
        elif p_operate==4:
            # 查詢
            pass
        intent=0
        operate=0
    if p_intent==3:
        # 猜意圖
        pass

    send_package=bytes("sen", encoding='UTF-8')
    send_package+=intent.to_bytes(4,'big')
    send_package+=operate.to_bytes(4,'big')
    send_package+=bytes(fulfillment ,encoding='UTF-8')
    send_package+=zero.to_bytes(fulfillment_size - (len(fulfillment.encode("UTF-8"))), 'big')
    return send_package

def encodeReceiptPackage(accountClass): # return bytearray

    package, zero, itemSize, detailSize ,userSize = 0, 0, 18, 18, 20
    
    package = bytes("rec", encoding='utf-8')
    package += accountClass.get_key().to_bytes(4, 'big')
    package += accountClass.get_money().to_bytes(4, 'big')
    package += accountClass.get_year().to_bytes(1, 'big')
    package += accountClass.get_month().to_bytes(1, 'big')
    package += accountClass.get_day().to_bytes(1,'big')
   
    package += bytes(accountClass.get_item(), encoding = "UTF-8")
    package += zero.to_bytes(itemSize - (len(accountClass.get_item().encode("UTF-8"))), 'big')
    package += bytes(accountClass.get_detail(), encoding = "UTF-8")
    package += zero.to_bytes(detailSize - (len(accountClass.get_detail()).encode("UTF-8")), 'big')
    package += accountClass.get_status().to_bytes(1, 'big')
    package += bytes(accountClass.get_user(),encoding='UTF-8')
    package += zero.to_bytes(userSize - (len(accountClass.get_user())), 'big')
    
    # print(package)
    # for i in package:
    #     print(i)

    return package

def receiptSearch(checkNumber,package):
    p_user=package[:20].decode('utf-8').split('\x00', 1)[0]
    checkAccount=Account()
    checkAccount.set_user(p_user)
    checkAccount.select()
    send_package=bytes('',encoding='utf-8')

    for i in checkNumber:
        for data in checkAccount.findAll:
            if data[1]==i[len(i)-2]:
                if data[2]==i[len(i)-1] or data[2]==i[len(i)-1]+1:
                    for number in i[:len(i)-2]:
                        if data[6]==number:
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
                            send_package+=encodeReceiptPackage(checkAccount)
                            break
    return send_package

def SHA256_encode(mes):
    s = hashlib.sha256()

    temp = mes
    s.update(temp.encode("UTF-8"))
    temp = s.hexdigest()
    return temp
                

