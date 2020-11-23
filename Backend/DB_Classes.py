import random
import sqlite3
import json
import os

class Weather:
    def __init__(self):
        self.month = 0
        self.day = 0
        self.city = ""
        self.period = ""
        self.situation = ""
        self.max_temperature = 0 # (C) 
        self.min_temperature = 0

    def set_day(self, day):
        self.day = day
    def set_month(self, month):
        self.month = month
    def set_city(self, city):
        self.city = city
    def set_period(self, period):
        self.period = period
    def set_situation(self, situation):
        self.situation = situation
    def set_max_temperature(self, max_temperature):
        self.max_temperature = max_temperature
    def set_min_temperature(self, min_temperature):
        self.min_temperature = min_temperature
    def get_day(self):
        return self.day
    def get_month(self):
        return self.month
    def get_city(self):
        return self.city
    def get_period(self):
        return self.period
    def get_situation(self):
        return self.situation
    def get_max_temperature(self):
        return self.max_temperature
    def get_min_temperature(self):
        return self.min_temperature

        # return package
    def DEBUG_printAllAttribute(self):
        print(self.city)

class UserAccount:
    def __init__(self):
        self.dbfile='life.db'
        self.con=sqlite3.connect(self.dbfile)

        self.name = ''
        self.password = ''
        self.key = ''
        self.version = ''
    
    def check(self):
        ifExist = False
        data=self.con.execute('select * from userAccount where Name=? AND Password = ?;', (self.name, self.password))
        for element in data:
            ifExist = True
            break
        return ifExist

    def checkKey(self):
        ifExist = False
        data = self.con.execute('SELECT * FROM userAccount WHERE Key = "{}";'.format(self.password))
        for ele in data:
            ifExist = True
            break
        return ifExist

    def checkName(self):
        ifExist = False
        data = self.con.execute('SELECT * FROM userAccount WHERE Name = "{}";'.format(self.name))
        for ele in data:
            ifExist = True
            break
        return ifExist    

    def insert(self):
        if (self.checkName()):
            print("register account fail.")
            return
        self.con.execute('insert into userAccount(Name, Password)values("{}", "{}");'.format(self.name, self.password))
        self.con.commit()

    def updateKey(self, key):
        self.con.execute("UPDATE userAccount SET key = ? WHERE Name = ?", (key, self.name))
        self.con.commit()

    def selectAll(self):
        data = self.con.execute("SELECT * FROM userAccount")
        return data

    def selectByName(self):
        data = self.con.execute('SELECT * FROM userAccount WHERE Name = "{}";'.format(self.name))
        result = ''
        for ele in data:
            result = ele
        self.name = result[0]
        self.password = result[1]
        self.key = result[2]
        self.version = result[3]

    def updateVersion(self, versionCode):
        self.con.execute('UPDATE userAccount SET Version = "{}" WHERE Name = "{}"'.format(versionCode, self.name))
        self.con.commit()
        

class Account:
    item,detail,receipt,note,dbfile,query,user='','','','','','',''
    year,month,day,money,status,key,con,selectnum,operationCode=0,0,0,0,0,0,0,0,0
    findAll ,idList = list(), list()

    PACKAGE_SIZE = 180

    def set_item(self, item):  #set分類
        self.item=item
    def get_item(self):
        return self.item
    def set_year(self, year):  #set年
        self.year=year
    def get_year(self):
        return self.year
    def set_month(self, month):  #set月
        self.month=month
    def get_month(self):
        return self.month
    def set_day(self, day):  #set日
        self.day=day
    def get_day(self):
        return self.day
    def set_money(self, money):  #set金額
        self.money=money
    def get_money(self):
        return self.money
    def set_detail(self, detail):  #set細項
        self.detail=detail
    def get_detail(self):
        return self.detail
    def set_receipt(self, receipt):  #set發票
        self.receipt=receipt
    def get_receipt(self):
        return self.receipt
    def set_note(self, note):        #set備註
        self.note=note
    def get_note(self):
        return self.note
    def set_status(self, status):    #set收支屬性
        self.status=status
    def get_status(self):
        return self.status
    def set_key(self,key):            #set id(刪除、修改、查詢時使用)
        self.key=key
    def get_key(self):
        return self.key
    def set_operationCode(self, code): #set 指令碼
        self.operationCode = code
    def get_operaionCode(self):
        return self.operationCode
    def set_user(self, user):          #set 使用者
        self.user = user
    def get_user(self):
        return self.user
    # def set_query(self,query):        #set要求(修改時使用)
    #     self.query=query
    # def get_query(self):
    #     return self.query
    # def set_selectnum(self,selectnum):  #set選取到的id(查詢時使用)
    #     self.selectnum=selectnum
    # def get_selectnum(self):
    #     return self.selectnum

    def operateAction(self):
        if self.operationCode == 0: # 新增
            self.insert()

            self.selectForDetail()
            for data in self.findAll:
                findData=data
            self.renewDetailBoard(findData)
            
            print("insert success.")
        elif self.operationCode == 1: # 刪除
            # When id = 0, database delete by user rather than id.
            if self.key == 0:
                self.delete_by_user()
            else:
                self.delete()
            print("delete success.")
        elif self.operationCode == 2: # 修改
            # When id = 0, database
            if self.key == 0:
                pass
            else:
                self.delete()
                self.insert()

                self.selectForDetail()
                for data in self.findAll:
                    findData=data
                self.renewDetailBoard(findData)

            print("modify success.")
        elif self.operationCode == 3: # 查詢
            # when id = 0, database select all of record rather than select by user.
            if self.key == 0:
                self.select_all()
            else:
                self.select()
            print("select success.")
        elif self.operationCode == 4:
            self.DEBUG_printAllAttribute()
            print('debug mode.')

    def DEBUG_printAllAttribute(self):
        print("ID", self.key)
        print("money", self.money)
        print("year", self.year)
        print("month", self.month)
        print("day", self.day)
        print('item', self.item)
        print('detail', self.detail)
        print('receipt', self.receipt)
        print('status', self.status)
        print('note', self.note)
        print('operateAction', self.operationCode)
        print('user', self.user)

    def __init__(self):
        self.dbfile='life.db'
        self.con=sqlite3.connect(self.dbfile)
    def insert(self):
        while(not self.checkKey()):
            self.key = random.randint(1, 100000)
        correctedDate = dealWithDate(self.year, self.month, self.day)
        self.year = correctedDate[0]
        self.month = correctedDate[1]
        self.day = correctedDate[2]

        self.con.execute('insert into record(金額,年,月,日,分類,細項,發票,備註,收支屬性,id,user)values({},{},{},{},"{}","{}","{}","{}",{},{},"{}");'.format(self.money,self.year,self.month,self.day,self.item,self.detail,self.receipt,self.note,self.status,self.key,self.user))
        self.con.commit()
    def delete(self):
        self.con.execute('delete from record where id={};'.format(self.key))
        self.con.commit()
    def delete_by_user(self):
        self.con.execute('delete from record where user="{}";'.format(self.user))
        self.con.commit()
    def update(self):
        self.con.execute('delete from record where id={};'.format(self.key))
        self.con.execute('insert into record(金額,年,月,日,分類,細項,發票,備註,收支屬性,id,user)values({},{},{},{},"{}","{}","{}","{}",{},{},"{}");'.format(self.money,self.year,self.month,self.day,self.item,self.detail,self.receipt,self.note,self.status,self.key,self.user))
        self.con.commit()
    def select(self):
        data=self.con.execute('select * from record where user="{}";'.format(self.user))
        self.findAll=data
        print("select success")
    def select_all(self):
        data = self.con.execute('SELECT * from record')
        self.findAll = data
        print("select all success")
    def selectForDetail(self):
        data=self.con.execute('select * from record where user="{}" and id={};'.format(self.user,self.key))
        self.findAll=data
    def checkKey(self):
        ifExist = False
        data = self.con.execute('SELECT * FROM record WHERE id = {}'.format(self.key))
        for ele in data:
            ifExist = True
            break

        return not ifExist
    def close(self):
        self.con.close()
    def deleteByRobot(self,timeDel):
        if timeDel!=True:
            self.con.execute('delete from record where user="{}";'.format(self.user))
            self.con.commit()
        else:
            if self.year!=0 and self.month!=0 and self.day!=0:
                self.con.execute('delete from record where 年={} and 月={} and 日={} and user="{}";'.format(self.year,self.month,self.day,self.user))
                self.con.commit()
            elif self.year!=0 and self.month!=0 and self.day==0:
                self.con.execute('delete from record where 年={} and 月={} and user="{}";'.format(self.year,self.month,self.user))
                self.con.commit()
            elif self.year!=0 and self.month==0 and self.day==0:
                self.con.execute('delete from record where 年={} and user="{}";'.format(self.year,self.user))
                self.con.commit()
    def selectByRobot_money(self,timeSelect,rangeJudge):
        equalWords=['以']
        upWords=['上','大','多']
        downWords=['下','小','少']
        data=[]
        equalFlag,upFlag,downFlag=False,False,False

        for word in equalWords:
            if len(rangeJudge)>=len(word):
                if rangeJudge.find(word)!=-1:
                    equalFlag=True
                    break
            else:
                if word.find(rangeJudge)!=-1:
                    equalFlag=True
                    break
        for word in upWords:
            if len(rangeJudge)>=len(word):
                if rangeJudge.find(word)!=-1:
                    upFlag=True
                    break
            else:
                if word.find(rangeJudge)!=-1:
                    upFlag=True
                    break
        for word in downWords:
            if len(rangeJudge)>=len(word):
                if rangeJudge.find(word)!=-1:
                    downFlag=True
                    break
            else:
                if word.find(rangeJudge)!=-1:
                    downFlag=True
                    break


        if timeSelect==True:
            if equalFlag==True:
                if upFlag==True and downFlag==False:
                    if self.year!=0 and self.month!=0 and self.day!=0:
                        data=self.con.execute('select * from record where 年={} and 月={} and 日={} and user="{}" and 金額>={};'.format(self.year,self.month,self.day,self.user,self.money))
                    elif self.year!=0 and self.month!=0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and 月={} and user="{}" and 金額>={};'.format(self.year,self.month,self.user,self.money))
                    elif self.year!=0 and self.month==0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and user="{}" and 金額>={};'.format(self.year,self.user,self.money))
                elif upFlag==False and downFlag==True:
                    if self.year!=0 and self.month!=0 and self.day!=0:
                        data=self.con.execute('select * from record where 年={} and 月={} and 日={} and user="{}" and 金額<={};'.format(self.year,self.month,self.day,self.user,self.money))
                    elif self.year!=0 and self.month!=0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and 月={} and user="{}" and 金額<={};'.format(self.year,self.month,self.user,self.money))
                    elif self.year!=0 and self.month==0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and user="{}" and 金額<={};'.format(self.year,self.user,self.money))
                else:
                    if self.year!=0 and self.month!=0 and self.day!=0:
                        data=self.con.execute('select * from record where 年={} and 月={} and 日={} and user="{}" and 金額={};'.format(self.year,self.month,self.day,self.user,self.money))
                    elif self.year!=0 and self.month!=0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and 月={} and user="{}" and 金額={};'.format(self.year,self.month,self.user,self.money))
                    elif self.year!=0 and self.month==0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and user="{}" and 金額={};'.format(self.year,self.user,self.money))
            else:
                if upFlag==True and downFlag==False:
                    if self.year!=0 and self.month!=0 and self.day!=0:
                        data=self.con.execute('select * from record where 年={} and 月={} and 日={} and user="{}" and 金額>{};'.format(self.year,self.month,self.day,self.user,self.money))
                    elif self.year!=0 and self.month!=0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and 月={} and user="{}" and 金額>{};'.format(self.year,self.month,self.user,self.money))
                    elif self.year!=0 and self.month==0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and user="{}" and 金額>{};'.format(self.year,self.user,self.money))
                elif upFlag==False and downFlag==True:
                    if self.year!=0 and self.month!=0 and self.day!=0:
                        data=self.con.execute('select * from record where 年={} and 月={} and 日={} and user="{}" and 金額<{};'.format(self.year,self.month,self.day,self.user,self.money))
                    elif self.year!=0 and self.month!=0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and 月={} and user="{}" and 金額<{};'.format(self.year,self.month,self.user,self.money))
                    elif self.year!=0 and self.month==0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and user="{}" and 金額<{};'.format(self.year,self.user,self.money))
                else:
                    if self.year!=0 and self.month!=0 and self.day!=0:
                        data=self.con.execute('select * from record where 年={} and 月={} and 日={} and user="{}" and 金額={};'.format(self.year,self.month,self.day,self.user,self.money))
                    elif self.year!=0 and self.month!=0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and 月={} and user="{}" and 金額={};'.format(self.year,self.month,self.user,self.money))
                    elif self.year!=0 and self.month==0 and self.day==0:
                        data=self.con.execute('select * from record where 年={} and user="{}" and 金額={};'.format(self.year,self.user,self.money))
        else:
            if equalFlag==True:
                if upFlag==True and downFlag==False:
                    data=self.con.execute('select * from record where user="{}" and 金額>={};'.format(self.user,self.money))
                elif upFlag==False and downFlag==True:
                    data=self.con.execute('select * from record where user="{}" and 金額<={};'.format(self.user,self.money))
                else:
                    data=self.con.execute('select * from record where user="{}" and 金額={};'.format(self.user,self.money))
            else:
                if upFlag==True and downFlag==False:
                    data=self.con.execute('select * from record where user="{}" and 金額>{};'.format(self.user,self.money))
                elif upFlag==False and downFlag==True:
                    data=self.con.execute('select * from record where user="{}" and 金額<{};'.format(self.user,self.money))
                else:
                    data=self.con.execute('select * from record where user="{}" and 金額={};'.format(self.user,self.money))
        
        self.findAll=data
    def selectByRobot(self,timeSelect):
        data=[]
        if timeSelect==True:
            if self.year!=0 and self.month!=0 and self.day!=0:
                data=self.con.execute('select * from record where 年={} and 月={} and 日={} and user="{}";'.format(self.year,self.month,self.day,self.user))
            elif self.year!=0 and self.month!=0 and self.day==0:
                data=self.con.execute('select * from record where 年={} and 月={} and user="{}";'.format(self.year,self.month,self.user))
            elif self.year!=0 and self.month==0 and self.day==0:
                data=self.con.execute('select * from record where 年={} and user="{}";'.format(self.year,self.user))
        else:
            data=self.con.execute('select * from record where user="{}";'.format(self.user))
        
        self.findAll=data
    def renewDetailBoard(self,findData):
        stableDetail=['游泳','健身房','遊樂園','展覽','電影','點卡','點數','遊戲','玩具','模型','球','漫畫','車','車票','火車','高鐵','坐','搭','公車','交通','運輸','捷運','大眾','書','講義','補習','教材','課','病','醫','療','護','健康','保健','藥','保','保險','險','股票','股','吃','喝','吃飯','飲料','飯','早餐','午餐','晚餐','餐','宵夜','點心','水','酒','食','餐廳']
        stableFlag,findFlag=False,False
        userDetailBoard=dict()

        for i in stableDetail:
            if len(findData[5])>=len(i):
                check=findData[5].find(i)
            else:
                check=i.find(findData[5])
            if check!=-1:
                stableFlag=True
                break
        if stableFlag!=True:
            scriptDir = os.path.dirname(__file__)
            folderDir = "../userTrainingData/"
            f=self.get_user()+'.json'
            try:
                with open(os.path.join(scriptDir, folderDir + f),'r',encoding='utf-8') as fp:
                    userDetailBoard=json.load(fp)
                keyName=list(userDetailBoard.keys())
                for key in keyName:
                    for i in userDetailBoard[key]:
                        if len(findData[5])>=len(i):
                            check=findData[5].find(i)
                        else:
                            check=i.find(findData[5])

                        if check!=-1:
                            if findData[4]==key:
                                findFlag=True
                                break
                            else:
                                userDetailBoard[key].remove(i)
                                try:
                                    userDetailBoard[findData[4]].append(findData[5])
                                except:
                                    userDetailBoard.setdefault(findData[4],[findData[5]])
                                findFlag=True
                                break  
                    if findFlag==True:
                        break
                if findFlag==False:
                    try:
                        userDetailBoard[findData[4]].append(findData[5])
                    except:
                        userDetailBoard.setdefault(findData[4],[findData[5]])
                
                changeUserDetailBoard=json.dumps(userDetailBoard)
                with open(os.path.join(scriptDir, folderDir + f),'w',encoding='utf-8') as fp:
                    fp.write(changeUserDetailBoard)
            except:
                print('no file!')


                
class Schedule:
    todo,dbfile,query,user='','','',''
    year,month,day,con,key,operationCode=0,0,0,0,0,0
    start,end=0.0,0.0
    findAll=[]

    PACKAGE_SIZE = 78

    def set_todo(self, todo):  #set事情
        self.todo=todo
    def get_todo(self):
        return self.todo
    def set_year(self, year):  #set年
        self.year=year
    def get_year(self):
        return self.year
    def set_month(self, month):  #set月
        self.month=month
    def get_month(self):
        return self.month
    def set_day(self, day):  #set日
        self.day=day
    def get_day(self):
        return self.day
    def set_start(self, start):  #set開始時間
        self.start=start
    def get_start(self):
        return self.start
    def set_end(self, end):  #set結束時間
        self.end=end
    def get_end(self):
        return self.end
    def set_start_in_format(self, year, month, day, hour, minute):
        correctedDate = dealWithDate(year, month, day)
        
        self.start = (hour * 100) + minute
        self.day = correctedDate[2]
        self.month = correctedDate[1]
        self.year = correctedDate[0]

    def set_end_in_format(self, year, month, day, hour, minute):
        correctedDate = dealWithDate(year, month, day)
        year = correctedDate[0]
        month = correctedDate[1]
        day = correctedDate[2]

        detTime = 0
        monthDay = [31,28,31,30,31,30,31,31,30,31,30,31]

        detTime += hour
        detTime += (day - self.day) * 24

        if month != self.month:
            if month > self.month:
                if (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0):
                    monthDay[1] += 1
                for ptr in range(self.month - 1, month - 1):
                    detTime += (monthDay[ptr] * 24)
            else:
                if ((self.year + 1) % 4 == 0 and (self.year + 1) % 100 != 0) or ((self.year + 1) % 400 == 0):
                    monthDay[1] += 1
                for ptr in range(month - 1, self.month - 1):
                    detTime -= (monthDay[ptr] * 24)
        
        if year > self.year:
            for ptr in range(self.year, year):
                if ((ptr % 4 == 0 and ptr % 100 != 0) or (ptr % 400 == 0)):
                    if (ptr == self.year and self.month <= 2) or (ptr == year and month > 2):
                        detTime += 366 * 24
                    elif ptr != self.year and ptr != year:
                        detTime += 366 * 24
                    else:
                        detTime += 365 * 24
                else:
                    detTime += 365 * 24
        elif year < self.year:
            self.end = -1
            print("Set Time Error! You need to set StartDate before set EndDate")
            return
        
        detTime = detTime * 100 + minute

        self.end = detTime

    def set_relative_end_time(self, year, month, day, hour, minute):
        detTime = self.start
        monthDay = [31,28,31,30,31,30,31,31,30,31,30,31]


        detTime += hour
        detTime += day * 24
        for i in range(month):
            ptr = (self.month - 1 + i) % 12
            detTime += monthDay[ptr]
        
        for i in range(year):
            ptr = self.year + i
            if ((ptr % 4 == 0 and ptr % 100 != 0) or (ptr % 400 == 0)):
                if (ptr == self.year and self.month >= 3):
                    detTime += 365 * 24
                else:
                    detTime += 366 * 24
            else:
                detTime += 365 * 24

        detTime = detTime * 100 + minute

        self.end = detTime

    # def set_query(self,query):        #set要求(修改時使用)
    #     self.query=query
    # def get_query(self):
    #     return self.query
    def set_key(self,key):            #set id(刪除、修改、查詢時使用)
        self.key=key
    def get_key(self):
        return self.key
    def set_operationCode(self, code):
        self.operationCode = code
    def get_operaionCode(self):
        return self.operationCode
    def set_user(self,user):
        self.user=user
    def get_user(self):
        return self.user

    def operateAction(self):
        if self.operationCode == 0: # 新增
            self.insert()
            print("insert success.")
        elif self.operationCode == 1: # 刪除
            # When id = 0, delete by user.
            if self.key == 0:
                self.delete_by_user()
            else:
                self.delete()

            print("delete success.")
        elif self.operationCode == 2: # 修改
            self.delete()
            self.insert()
            print("modify success.")
        elif self.operationCode == 3: # 查詢
            self.select()
            print("select success.")


    def __init__(self):
        self.dbfile='life.db'
        self.con=sqlite3.connect(self.dbfile)
    def insert(self):
        while(not self.checkKey()):
            self.key = random.randint(1, 100000)
        self.con.execute('insert into schedule_record(事情,年,月,日,開始時間,結束時間,id,user)values("{}",{},{},{},{},{},{},"{}");'.format(self.todo,self.year,self.month,self.day,self.start,self.end,self.key,self.user))
        self.con.commit()
    def delete(self):
        self.con.execute('delete from schedule_record where id={};'.format(self.key))
        self.con.commit()
    def delete_by_user(self):
        try:
            self.con.execute('delete from schedule_record where user = "{}"'.format(self.user))
            self.con.commit()
        except sqlite3.OperationalError as e:
            print("there is no data of", self.user)
        except Exception as e:
            raise Exception(e)
    def update(self):
        self.con.execute('delete from schedule_record where id={};'.format(self.key))
        self.con.execute('insert into schedule_record(事情,年,月,日,開始時間,結束時間,id,user)values("{}",{},{},{},{},{},{},"{}");'.format(self.todo,self.year,self.month,self.day,self.start,self.end,self.key,self.user))
        self.con.commit()
    def select(self):
        data=self.con.execute('select * from schedule_record where user="{}";'.format(self.user))
        self.findAll=data
    def close(self):
        self.con.close()
    def checkKey(self):
        ifExist = False
        data = self.con.execute('SELECT * FROM schedule_record WHERE id = {}'.format(self.key))
        for ele in data:
            ifExist = True
            break

        return not ifExist
    def deleteByRobot(self,timeDel):
        if timeDel!=True:
            self.con.execute('delete from schedule_record where user="{}";'.format(self.user))
            self.con.commit()
        else:
            if self.year!=0 and self.month!=0 and self.day!=0:
                self.con.execute('delete from schedule_record where 年={} and 月={} and 日={} and user="{}";'.format(self.year,self.month,self.day,self.user))
                self.con.commit()
            elif self.year!=0 and self.month!=0 and self.day==0:
                self.con.execute('delete from schedule_record where 年={} and 月={} and user="{}";'.format(self.year,self.month,self.user))
                self.con.commit()
            elif self.year!=0 and self.month==0 and self.day==0:
                self.con.execute('delete from schedule_record where 年={} and user="{}";'.format(self.year,self.user))
                self.con.commit()
    def selectByRobot(self,timeSelect):
        data=[]
        if timeSelect==True:
            if self.year!=0 and self.month!=0 and self.day!=0:
                data=self.con.execute('select * from schedule_record where 年={} and 月={} and 日={} and user="{}";'.format(self.year,self.month,self.day,self.user))
            elif self.year!=0 and self.month!=0 and self.day==0:
                data=self.con.execute('select * from schedule_record where 年={} and 月={} and user="{}";'.format(self.year,self.month,self.user))
            elif self.year!=0 and self.month==0 and self.day==0:
                data=self.con.execute('select * from schedule_record where 年={} and user="{}";'.format(self.year,self.user))
        else:
            data=self.con.execute('select * from schedule_record where user="{}";'.format(self.user))
            
        self.findAll=data


def dealWithDate(year, month, day):
    monthDay = [31,28,31,30,31,30,31,31,30,31,30,31]
    resultYear, resultMonth, resultDay = year, month, day

    if (resultYear % 4 == 0 and resultYear % 100 != 0) or (resultYear % 400 == 0):
        monthDay[1] = 29

    while resultDay > monthDay[month - 1]:
        resultDay -= monthDay[month - 1]
        resultMonth += 1
        if resultMonth > 12:
            resultYear += 1
            if (resultYear % 4 == 0 and resultYear % 100 != 0) or (resultYear % 400 == 0):
                monthDay[1] = 29
            else:
                monthDay[1] = 28
            resultMonth -= 12
    
    while resultMonth > 12:
        resultYear += 1
        resultMonth -= 12

    return (resultYear, resultMonth, resultDay)
