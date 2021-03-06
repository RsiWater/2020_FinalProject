from DB_Classes import *
from dialogflow_f import *
import Crawl
import response_judge
import hashlib
import os

def classifyPackage(package):
    packageType = package[:3].decode("utf-8")
    
    if packageType == 'acc':
        print("account")
        send_package=bytes('',encoding='utf-8')
        
        for i in range((int) (len(package) / Account.PACKAGE_SIZE)):
            ptr = i * Account.PACKAGE_SIZE
            rcv_package = decodeAccountPackage(package[ptr + 3 : (i + 1) * Account.PACKAGE_SIZE])
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
        print('schedule')
        send_package=bytes('',encoding='utf-8')

        for i in range((int) (len(package) / Schedule.PACKAGE_SIZE)):
            ptr = i * Schedule.PACKAGE_SIZE
            rcv_package = decodeSchedulePackage(package[ptr + 3 : (i + 1) * Schedule.PACKAGE_SIZE])
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
        print('weather')
        send_package = bytes('', encoding="UTF-8")
        weatherData = Crawl.getWeatherData()
        for eleList in weatherData.values():
            for ele in eleList:
                send_package+=encodeWeatherPackage(ele)
        # 
        return send_package

    elif packageType=='sen':
        print('sentence')
        send_package=Sentence(package[3:])
        return send_package

    elif packageType == 'rec':
        print('receipt')
        checkData = Crawl.readReceiptData()
        send_package = receiptSearch(checkData,package[3:])
        return send_package

    elif packageType == "rqr":
        print("receipt QR")
        checkNumber = Crawl.readReceiptData()
        
        send_package = encodeReceiptQRPackage(checkNumber)
        return send_package

    elif packageType == 'log':
        print("login")        
        rcv_package = decodeLoginPackage(package[3:])
        
        send_package = encodeLoginPackage(rcv_package)
        return send_package

    elif packageType == 'reg':
        print('reg')
        rcv_package = decodeLoginPackage(package[3:])
        generateNewJson(rcv_package)

        send_package = encodeRegisterPackage(rcv_package)
        return send_package

    elif packageType == 'ver': #version control.
        print("ver")
        rcvUserAccount = decodeVersionPackage(package[3:])
        serverUserAccount = UserAccount()
        serverUserAccount.name = rcvUserAccount.name
        serverUserAccount.selectByName()
        if (rcvUserAccount.version > serverUserAccount.version and rcvUserAccount.version <= 65535 and serverUserAccount.version <= 65535) or (rcvUserAccount.version == 0 and serverUserAccount.version == 65535):
            serverUserAccount.updateVersion(rcvUserAccount.version)


        send_package = encodeVersionPackage(serverUserAccount)
        return send_package

    else:
        print('none')

    
    # elif packageType == 'deb':
    #     message = rcv_event.decode("UTF-8")
    #     print(message)

def decodeVersionPackage(package):
    resultUserAccount = UserAccount()

    resultUserAccount.version = int.from_bytes(package[:4], 'big')
    resultUserAccount.name = package[4:].decode("utf-8").split('\x00', 1)[0]
    return resultUserAccount

def encodeVersionPackage(userClass):
    package, zero, VERSION_SIZE, NAME_SIZE = 0, 0, 4, 20
    
    package = bytes("ver", encoding="UTF-8")
    package += userClass.version.to_bytes(VERSION_SIZE, 'big')
    package += bytes(userClass.name, encoding="utf-8")
    package += zero.to_bytes(NAME_SIZE - (len(userClass.name.encode('UTF-8'))), 'big')

    return package

def encodeLoginPackage(userClass):    
    zero, passSize, keySize = 0, 2, 64

    package = bytes("log", encoding="UTF-8")
    checkPassAuthorization = False
    if userClass.name == "key":
        checkPassAuthorization = userClass.checkKey()
    else:
        checkPassAuthorization = userClass.check()
            
    if checkPassAuthorization:
        package += bytes("OK", encoding="UTF-8")
        if userClass.name == "key":
            package += bytes("OK", encoding="UTF-8")
            package += zero.to_bytes(keySize - (len("OK".encode('UTF-8'))), 'big')
        else:
            package += bytes(userClass.key, encoding="UTF-8")
    else:
        package += bytes("NO", encoding="UTF-8")
        package += bytes(SHA256_encode("NULL"), encoding="UTF-8")
    
    return package

def encodeRegisterPackage(userClass):    
    zero, passSize, keySize = 0, 2, 64

    package = bytes("reg", encoding="UTF-8")
    checkPassAuthorization = False
    
    checkPassAuthorization = not userClass.checkName()
            
    if checkPassAuthorization:
        userClass.insert()
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

    package, zero, itemSize, detailSize, receiptSize, noteSize, userSize = 0, 0, 18, 30, 3, 90, 20
    
    package = bytes("acc", encoding='utf-8')
    package += accountClass.get_key().to_bytes(4, 'big')
    package += accountClass.get_money().to_bytes(4, 'big')
    package += accountClass.get_year().to_bytes(4, 'big')
    package += accountClass.get_month().to_bytes(1, 'big')
    package += accountClass.get_day().to_bytes(1,'big')
   
    package += bytes(accountClass.get_item(), encoding = "UTF-8")
    package += zero.to_bytes(itemSize - (len(accountClass.get_item().encode('UTF-8'))), 'big')
    if len(accountClass.get_detail().encode("UTF-8")) > detailSize:
        accountClass.set_detail(accountClass.get_detail()[:int(detailSize/3)])
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
    p_day, p_item, p_detail, p_receipt, p_note, p_status = package[13], package[14:32].decode('utf-8').split('\x00', 1)[0], package[32:62].decode('utf-8').split('\x00', 1)[0], package[62:65].decode('utf-8').split('\x00', 1)[0], package[65:155].decode('utf-8').split('\x00', 1)[0], package[155]
    p_operationCode, p_user = package[156], package[157:177].decode('utf-8').split('\x00', 1)[0]

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

    package, zero, todo_size, operationCodeSize, userSize = 0, 0, 36, 1, 20
    
    package = bytes("sch", encoding='utf-8')
    package += scheduleClass.get_key().to_bytes(4,'big')
    if len(scheduleClass.get_todo().encode('UTF-8')) > todo_size:
        scheduleClass.set_tode(scheduleClass.get_todo()[:int(todo_size/3)])
    package += bytes(scheduleClass.get_todo(), encoding='UTF-8')
    package += zero.to_bytes(todo_size - (len(scheduleClass.get_todo().encode('UTF-8'))), 'big')
    package += scheduleClass.get_year().to_bytes(4, 'big')
    package += scheduleClass.get_month().to_bytes(1, 'big')
    package += scheduleClass.get_day().to_bytes(1, 'big')
    package += scheduleClass.get_start().to_bytes(4, 'big')
    package += scheduleClass.get_end().to_bytes(4, 'big')
    package += scheduleClass.get_operaionCode().to_bytes(operationCodeSize, 'big')
    package += bytes(scheduleClass.get_user(),encoding='UTF-8')
    package += zero.to_bytes(userSize - (len(scheduleClass.get_user().encode("UTF-8"))), 'big')

    return package

def decodeSchedulePackage(package): # return AccountClass
    
    resultSchedule = Schedule()
    
    p_id, p_todo, p_year , p_month= int.from_bytes(package[:4], 'big'), package[4:40].decode('utf-8').split('\x00', 1)[0], int.from_bytes(package[40:44], 'big'), package[44]
    p_day, p_start, p_end = package[45], int.from_bytes(package[46:50], 'big'), int.from_bytes(package[50:54], 'big')
    p_operationCode, p_user = package[54], package[55:75].decode('utf-8').split('\x00', 1)[0]
    
    resultSchedule.set_key(p_id)
    resultSchedule.set_todo(p_todo)
    resultSchedule.set_year(p_year)
    resultSchedule.set_month(p_month)
    resultSchedule.set_day(p_day)
    resultSchedule.set_start(p_start)
    resultSchedule.set_end(p_end)
    resultSchedule.set_operationCode(p_operationCode)
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

    send_package,intent,operate,fulfillment,select_package=0,0,0,'',0
    p_intent,p_operate,p_sentence=int.from_bytes(package[:4], 'big'),int.from_bytes(package[4:8], 'big'),package[8:98].decode('utf-8').split('\x00', 1)[0]
    number=random.randint(0,1000)
    response=detect_texts('life-nxuajt',str(number),p_sentence,'zh-TW')
    originIntent,originOperate=response_judge.originJudge(response)
    fulfillment=response.query_result.fulfillment_text

    if p_intent==0:
        p_intent,p_operate=response_judge.judge(response, p_sentence)
    if p_intent==1:
        # 記帳
        if p_operate==1:
            # 新增
            year,month,day,item,detail,money,status,key,user,errorFlag=response_judge.cutSentenceAccount(p_sentence)
            if errorFlag==False:
                setAccount=Account()
                setAccount.set_year(year)
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
                intent=0
                operate=0
            else:
                intent=originIntent
                operate=originOperate
        elif p_operate==2:
            # 刪除
            year,month,day,key,user,timeDel,errorFlag=response_judge.cutSentence_del(p_sentence)
            if errorFlag==False:
                setAccount=Account()
                setAccount.set_year(year)
                setAccount.set_month(month)
                setAccount.set_day(day)
                setAccount.set_user(user)
                setAccount.deleteByRobot(timeDel)
                fulfillment='已刪除'
                intent=0
                operate=0
            else:
                intent=originIntent
                operate=originOperate
        elif p_operate==4:
            # 查詢
            year,month,day,key,user,money,timeSelect,moneySelect,errorFlag,rangeJudge,operateName=response_judge.cutSentence_select(p_sentence)
            if errorFlag==False:
                setAccount=Account()
                setAccount.set_year(year)
                setAccount.set_month(month)
                setAccount.set_day(day)
                setAccount.set_user(user)
                setAccount.set_money(money)
                if moneySelect==True:
                    setAccount.selectByRobot_money(timeSelect,rangeJudge)
                else:
                    setAccount.selectByRobot(timeSelect)
                select_package=bytes(operateName,encoding='utf-8')
                selectData=Account()
                haveFlag=False
                for data in setAccount.findAll:
                    haveFlag=True
                    selectData.set_money(data[0])
                    selectData.set_year(data[1])
                    selectData.set_month(data[2])
                    selectData.set_day(data[3])
                    selectData.set_item(data[4])
                    selectData.set_detail(data[5])
                    selectData.set_receipt(data[6])
                    selectData.set_note(data[7])
                    selectData.set_status(data[8])
                    selectData.set_key(data[9])
                    selectData.set_user(data[10])
                    select_package+=encodeAccountPackage(selectData)
                if haveFlag==False:
                    select_package+=bytes('null package',encoding='utf-8')
                intent=0
                operate=0
            else:
                select_package=bytes(operateName,encoding='utf-8')
                select_package+=bytes('null package',encoding='utf-8')
                intent=originIntent
                operate=originOperate
    if p_intent==2:
        # 行程
        if p_operate==1:
            # 新增
            todo,key,user,yearList,monthList,dayList,h,m,errorFlag=response_judge.cutSentenceSchedule_add(p_sentence)
            if errorFlag==False:
                setSchedule=Schedule()
                setSchedule.set_todo(todo)
                setSchedule.set_key(key)
                setSchedule.set_user(user)
                setSchedule.set_start_in_format(yearList[0],monthList[0],dayList[0],h[0],m[0])
                setSchedule.set_end_in_format(yearList[len(yearList)-1],monthList[len(monthList)-1],dayList[len(dayList)-1],h[len(h)-1],m[len(m)-1])
                setSchedule.insert()
                fulfillment='已新增'
                intent=0
                operate=0
            else:
                intent=originIntent
                operate=originOperate
        elif p_operate==2:
            # 刪除
            year,month,day,key,user,timeDel,errorFlag=response_judge.cutSentence_del(p_sentence)
            if errorFlag==False:
                setSchedule=Schedule()
                setSchedule.set_year(year)
                setSchedule.set_month(month)
                setSchedule.set_day(day)
                setSchedule.set_user(user)
                setSchedule.deleteByRobot(timeDel)
                fulfillment='已刪除'
                intent=0
                operate=0
            else:
                intent=originIntent
                operate=originOperate
        elif p_operate==4:
            # 查詢
            year,month,day,key,user,money,timeSelect,moneySelect,errorFlag,rangeJudge,operateName=response_judge.cutSentence_select(p_sentence)
            if errorFlag==False:
                setSchedule=Schedule()
                setSchedule.set_year(year)
                setSchedule.set_month(month)
                setSchedule.set_day(day)
                setSchedule.set_user(user)
                setSchedule.selectByRobot(timeSelect)
                select_package=bytes(operateName, encoding='utf-8')
                selectData=Schedule()
                haveFlag=False
                for data in setSchedule.findAll:
                    haveFlag=True
                    selectData.set_todo(data[0])
                    selectData.set_year(data[1])
                    selectData.set_month(data[2])
                    selectData.set_day(data[3])
                    selectData.set_start(data[4])
                    selectData.set_end(data[5])
                    selectData.set_key(data[6])
                    selectData.set_user(data[7])
                    select_package+=encodeSchedulePackage(selectData)
                if haveFlag==False:
                    select_package+=bytes('null package',encoding='utf-8')
                intent=0
                operate=0
            else:
                select_package=bytes(operateName, encoding='utf-8')
                select_package+=bytes('null package',encoding='utf-8')
                intent=originIntent
                operate=originOperate
    if p_intent==3:
        # 猜意圖
        intent=p_intent
        operate=p_operate
    if p_intent==4:
        # 天氣
        errorFlag,distance=response_judge.cutSentence_weather(p_sentence)
        if errorFlag==False:
            fulfillment=str(distance)
            intent=p_intent
            operate=p_operate
        else:
            fulfillment='無法查詢'
            intent=0
            operate=0
    if p_intent==5:
        # 發票
        intent=p_intent
        operate=p_operate

    send_package=bytes("sen", encoding='UTF-8')
    send_package+=intent.to_bytes(4,'big')
    send_package+=operate.to_bytes(4,'big')
    if select_package!=0:
        send_package+=select_package
    else:
        send_package+=bytes(fulfillment ,encoding='UTF-8')
        send_package+=zero.to_bytes(fulfillment_size - (len(fulfillment.encode("UTF-8"))), 'big')
    return send_package

def encodeReceiptPackage(accountClass): # return bytearray

    package = bytes("", encoding="UTF-8")
    zero, detailSize ,receiptSize = 0, 30, 3
    
    package += accountClass.get_key().to_bytes(4, 'big')
    package += accountClass.get_money().to_bytes(4, 'big')
    package += accountClass.get_year().to_bytes(4, 'big')
    package += accountClass.get_month().to_bytes(1, 'big')
    package += accountClass.get_day().to_bytes(1,'big')
    package += bytes(accountClass.get_detail(), encoding = "UTF-8")
    package += zero.to_bytes(detailSize - (len(accountClass.get_detail().encode('UTF-8'))), 'big')
    package += bytes(accountClass.get_receipt(), encoding = "UTF-8")
    package += zero.to_bytes(receiptSize - (len(accountClass.get_receipt().encode('UTF-8'))), 'big')
    package += accountClass.get_status().to_bytes(1, 'big')
    
    # print(package)
    # for i in package:
    #     print(i)

    return package

def encodeReceiptQRPackage(checkNumber):
    package, zero, DATE_SIZE, HIT_NUMBER_SIZE = 0, 0, 8, 56

    package = bytes("", encoding="UTF-8")
    for date, hitNumberList in checkNumber.items():
        package += bytes("rqr", encoding="UTF-8")
        package += bytes(date, encoding="UTF-8")
        package += zero.to_bytes(DATE_SIZE - (len(date.encode("UTF-8"))), 'big')
        currentHitNumberSize = 0
        for hitNumber in hitNumberList:
            package += bytes(hitNumber, encoding="UTF-8")
            currentHitNumberSize += 8
        while currentHitNumberSize < HIT_NUMBER_SIZE:
            package += bytes("xxxxxxxx", encoding="UTF-8")
            currentHitNumberSize += 8

    return package    

# dropped.
def receiptSearch(checkData,package):
    p_user=package[:20].decode('utf-8').split('\x00', 1)[0]
    checkAccount=Account()
    checkAccount.set_user(p_user)
    checkAccount.select()
    send_package=bytes('rec',encoding='utf-8')

    year,month=[],[]
    keys=list(checkData.keys())
    for i in range(len(keys)):
        year.append(keys[i][:4])
    for i in range(len(keys)):
        if keys[i][4]=='0':
            month.append(keys[i][5])
        else:
            month.append(keys[i][4:6])
    numbers=list(checkData.values())
    
    hitAccount=Account()
    for i in range(len(year)):
        for data in checkAccount.findAll:
            if data[1]==year[i]:
                if data[2]==month[i] or data[2]==month[i]+1:
                    for j in range(len(numbers[i])):
                        if data[6]==numbers[i][j][5:8]:
                            hitAccount.set_money(data[0])
                            hitAccount.set_year(data[1])
                            hitAccount.set_month(data[2])
                            hitAccount.set_day(data[3])
                            hitAccount.set_item(data[4])
                            hitAccount.set_detail(data[5])
                            hitAccount.set_receipt(data[6])
                            hitAccount.set_note(data[7])
                            hitAccount.set_status(data[8])
                            hitAccount.set_key(data[9])
                            hitAccount.set_user(data[10])
                            s='#'+str(j)+'#'
                            send_package+=bytes(s,encoding='utf-8')
                            send_package+=encodeReceiptPackage(hitAccount)

    return send_package

def generateNewJson(rcvUserAccount):
    scriptDir = os.path.dirname(__file__)
    dir = "../userTrainingData/"
    filePath = dir + rcvUserAccount.name + ".json"
    defaultFilePath = dir + "detail_default.json"

    try:
        with open(os.path.join(scriptDir, filePath), 'r') as fp:
            print("Error! There has already a json file for this user!")
    except IOError:
        with open(os.path.join(scriptDir, filePath), 'w') as fp:
            dfp = open(os.path.join(scriptDir, defaultFilePath), 'r', encoding = "UTF-8")

            tempDict = json.load(dfp)
            fp.write(json.dumps(tempDict))
        print("The operation of creating user: " + rcvUserAccount.name + " has completed.")
    except Exception:
        print("Error! unexcepted error has occurred.")
        print(Exception)

def SHA256_encode(mes):
    s = hashlib.sha256()

    temp = mes
    s.update(temp.encode("UTF-8"))
    temp = s.hexdigest()
    return temp
                

