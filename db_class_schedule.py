
import sqlite3
import random



class Schedule:
    todo,dbfile,query='','',''
    year,month,day,con,number,key=0,0,0,0,0,0
    start,end=0.0,0.0


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
    def set_number(self):        #set id(insert時使用)
        self.number=random.randint(1,100000)
    def get_number(self):
        return self.number
    def set_key(self,key):            #set id(刪除、修改、查詢時使用)
        self.key=key
    def get_key(self):
        return self.key


    def __init__(self):
        self.dbfile='life.db'
        self.con=sqlite3.connect(self.dbfile)
    def insert(self):
        self.con.execute('insert into schedule_record(事情,年,月,日,開始時間,結束時間,id)values("{}",{},{},{},{},{},{});'.format(self.todo,self.year,self.month,self.day,self.start,self.end,self.number))
        self.con.commit()
    def delete(self):
        self.con.execute('delete from schedule_record where id={};'.format(self.key))
        self.con.commit()
    def update(self):
        self.con.execute('delete from schedule_record where id={};'.format(self.key))
        self.con.execute('insert into schedule_record(事情,年,月,日,開始時間,結束時間,id)values("{}",{},{},{},{},{},{});'.format(self.todo,self.year,self.month,self.day,self.start,self.end,self.key))
        self.con.commit()
    def select(self):
        datas=[]
        data=self.con.execute('select * from schedule_record where id={};'.format(self.key))
        for i in data:
            for j in i:
                datas.append(j)
        self.set_todo(datas[0])
        self.set_year(datas[1])
        self.set_month(datas[2])
        self.set_day(datas[3])
        self.set_start(datas[4])
        self.set_end(datas[5])
        #self.set_key(datas[6])
    def close(self):
        self.con.close()
    