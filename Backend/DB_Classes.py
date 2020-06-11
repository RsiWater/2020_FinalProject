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


    def generate_package(self):
        package, zero = "", 0
        CITY_SIZE, PERIOD_SIZE, SITUATION_SIZE = 12, 12, 30

        package += bytes("wea", encoding='utf-8')
        package += self.month.to_bytes(1, 'big')
        package += self.day.to_bytes(1, 'big')
        package += bytes(self.city, encoding='utf-8')
        package += zero.to_bytes(CITY_SIZE - (len(self.city) * 3 ), 'big')
        package += bytes(self.period, encoding='utf-8')
        package += zero.to_bytes(PERIOD_SIZE - (len(self.period) * 3), 'big')
        package += bytes(self.situation, encoding='utf-8')
        package += zero.to_bytes(SITUATION_SIZE - (len(self.situation) * 3), 'big')
        package += self.max_temperature.to_bytes(1, 'big')
        package += self.min_temperature.to_bytes(1, 'big')

        return package

class UserAccount:
    def __init__(self):
        self.dbfile='life.db'
        self.con=sqlite3.connect(self.dbfile)

        self.name = ''
        self.password = ''
    
    def check(self):
        ifExist = False
        data=self.con.execute('select * from userAccount where Name={} AND Password = {};'.format(self.name, self.password))
        for element in data:
            ifExist = True
            break
        return ifExist
