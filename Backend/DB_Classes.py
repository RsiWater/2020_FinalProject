import random
import sqlite3

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

        return package
    def DEBUG_printAllAttribute(self):
        print(self.city)

class UserAccount:
    def __init__(self):
        self.dbfile='life.db'
        self.con=sqlite3.connect(self.dbfile)

        self.name = ''
        self.password = ''
    
    def check(self):
        ifExist = False
        data=self.con.execute('select * from userAccount where Name=? AND Password = ?;', (self.name, self.password))
        for element in data:
            ifExist = True
            break
        return ifExist

class Account:
    item,detail,receipt,note,dbfile,query,user='','','','','','',''
    year,month,day,money,status,key,con,selectnum,operationCode=0,0,0,0,0,0,0,0,0
    findAll=[]

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
            print("insert success.")
        elif self.operationCode == 1: # 刪除
            self.delete()
            print("delete success.")
        elif self.operationCode == 2: # 修改
            self.delete()
            self.insert()
            print("modify success.")
        elif self.operationCode == 3: # 查詢
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
        # self.DEBUG_printAllAttribute()
        self.con.execute('insert into record(金額,年,月,日,分類,細項,發票,備註,收支屬性,id,user)values({},{},{},{},"{}","{}","{}","{}",{},{},"{}");'.format(self.money,self.year,self.month,self.day,self.item,self.detail,self.receipt,self.note,self.status,self.key,self.user))
        self.con.commit()
    def delete(self):
        self.con.execute('delete from record where id={};'.format(self.key))
        self.con.commit()
    def update(self):
        self.con.execute('delete from record where id={};'.format(self.key))
        self.con.execute('insert into record(金額,年,月,日,分類,細項,發票,備註,收支屬性,id,user)values({},{},{},{},"{}","{}","{}","{}",{},{},"{}");'.format(self.money,self.year,self.month,self.day,self.item,self.detail,self.receipt,self.note,self.status,self.key,self.user))
        self.con.commit()
    def select(self):
        data=self.con.execute('select * from record where user="{}";'.format(self.user))
        self.findAll=data
        print("select success")
    def close(self):
        self.con.close()


class Schedule:
    todo,dbfile,query,user='','','',''
    year,month,day,con,key,operationCode=0,0,0,0,0,0
    start,end=0.0,0.0
    findAll=[]


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
        self.con.execute('insert into schedule_record(事情,年,月,日,開始時間,結束時間,id,user)values("{}",{},{},{},{},{},{},"{}");'.format(self.todo,self.year,self.month,self.day,self.start,self.end,self.key,self.user))
        self.con.commit()
    def delete(self):
        self.con.execute('delete from schedule_record where id={};'.format(self.key))
        self.con.commit()
    def update(self):
        self.con.execute('delete from schedule_record where id={};'.format(self.key))
        self.con.execute('insert into schedule_record(事情,年,月,日,開始時間,結束時間,id,user)values("{}",{},{},{},{},{},{},"{}");'.format(self.todo,self.year,self.month,self.day,self.start,self.end,self.key,self.user))
        self.con.commit()
    def select(self):
        data=self.con.execute('select * from schedule_record where user="{}";'.format(self.user))
        self.findAll=data
    def close(self):
        self.con.close()
    