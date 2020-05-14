import random
import sqlite3



class Account:
    item,detail,receipt,note,dbfile,query='','','','','',''
    year,month,day,money,number,status,key,con,selectnum=0,0,0,0,0,0,0,0,0

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
    def randomize_number(self):        #set id(insert時使用)
        self.number=random.randint(1,100000)
    def set_number(self, number):
        self.number = number
    def get_number(self):
        return self.number
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
    # def set_query(self,query):        #set要求(修改時使用)
    #     self.query=query
    # def get_query(self):
    #     return self.query
    # def set_selectnum(self,selectnum):  #set選取到的id(查詢時使用)
    #     self.selectnum=selectnum
    # def get_selectnum(self):
    #     return self.selectnum

    def operateAction(self, operationCode):
        if operationCode == 0: # 新增
            self.insert()
            print("insert success.")
        elif operationCode == 1: # 刪除
            self.key = self.number
            self.delete()
            print("delete success.")
        elif operationCode == 2: # 修改
            self.key = self.number
            self.delete()
            self.insert()
            print("modify success.")
        elif operationCode == 3: # 查詢
            self.select()
            print("select success.")
    def DEBUG_printAllAttribute(self):
        print("ID", self.number)
        print("money", self.money)
        print("year", self.year)
        print("month", self.month)
        print("day", self.day)
        print('item', self.item)
        print('detail', self.detail)
        print('receipt', self.receipt)
        print('status', self.status)
        print('note', self.note)


    def __init__(self):
        self.dbfile='life.db'
        self.con=sqlite3.connect(self.dbfile)
    def insert(self):
        self.DEBUG_printAllAttribute()
        self.con.execute('insert into record(金額,年,月,日,分類,細項,發票,備註,收支屬性,id)values({},{},{},{},"{}","{}","{}","{}",{},{});'.format(self.money,self.year,self.month,self.day,self.item,self.detail,self.receipt,self.note,self.status,self.number))
        self.con.commit()
    def delete(self):
        self.con.execute('delete from record where id={};'.format(self.key))
        self.con.commit()
    def update(self):
        self.con.execute('delete from record where id={};'.format(self.key))
        self.con.execute('insert into record(金額,年,月,日,分類,細項,發票,備註,收支屬性,id)values({},{},{},{},"{}","{}","{}","{}",{},{});'.format(self.money,self.year,self.month,self.day,self.item,self.detail,self.receipt,self.note,self.status,self.key))
        self.con.commit()
    def select(self):
        datas=[]
        data=self.con.execute('select * from record where id={};'.format(self.key))
        for i in data:
            for j in i:
                datas.append(j)
        self.set_money(datas[0])
        self.set_year(datas[1])
        self.set_month(datas[2])
        self.set_day(datas[3])
        self.set_item(datas[4])
        self.set_detail(datas[5])
        self.set_receipt(datas[7])
        self.set_note(datas[8])
        self.set_status(datas[9])
        print("select success")
    def close(self):
        self.con.close()
    

        
    
    
    
        
        