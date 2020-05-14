import sqlite3
import random

new_dbfile='life.db'
new_con=sqlite3.connect(new_dbfile)




def check(count):
    unsame=False
    rows=new_con.execute('select id from schedule_record;')
    while unsame==False:
        for row in rows:
            for item in row:
                if item==count :
                    count=random.randint(0,100000)
                    unsame==False
                    break
                else:
                    unsame=True
            if unsame==False:
                break
        if unsame==True:
            return count
            break

def check_del(count):
    same=False
    rows=new_con.execute('select id from schedule_record;')
    while same==False:
        for row in rows:
            for item in row:
                if item==count:
                    same=True
                    break
                else:
                    same=False
            if same==True:
                break
        return same
        break
