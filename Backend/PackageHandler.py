from db_class_account import *
from db_class_schedule import *

def encodeAccountPackage(accountClass): # return bytearray

    package, zero, itemSize = 0, 0, 18
    
    package = bytes("acc", encoding='utf-8')
    package += accountClass.get_number().to_bytes(4, 'big')
    package += accountClass.get_money().to_bytes(4, 'big')
    package += accountClass.get_year().to_bytes(1, 'big')
    package += accountClass.get_month().to_bytes(1, 'big')
    package += accountClass.get_day().to_bytes(1,'big')
   
    package += bytes(accountClass.get_item(), encoding = "UTF-8")
    package += zero.to_bytes(itemSize - (len(accountClass.get_item() * 3)), 'big')
    package += bytes(accountClass.get_detail(), encoding = "UTF-8")
    package += zero.to_bytes(itemSize - (len(accountClass.get_detail()) * 3), 'big')
    package += accountClass.get_status().to_bytes(1, 'big')
    
    # print(package)
    # for i in package:
    #     print(i)

    return package

def decodeAccountPackage(package): # return AccountClass
    
    resultAccount = Account()
    
    p_id, p_money, p_year , p_month= int.from_bytes(package[:4], 'big'), int.from_bytes(package[4:8],'big'), package[8], package[9]
    p_day, p_item, p_detail, p_status = package[10], package[11:29].decode('utf-8'), package[29:47].decode('utf-8'), package[47]
    p_operationCode = package[48]

    resultAccount.set_number(p_id)
    resultAccount.set_money(p_money)
    resultAccount.set_year(p_year)
    resultAccount.set_month(p_month)
    resultAccount.set_day(p_day)
    resultAccount.set_item(p_item)
    resultAccount.set_detail(p_detail)
    resultAccount.set_status(p_status)
    
    #
    resultAccount.set_receipt("898")
    resultAccount.set_note("testest")
    #

    resultAccount.operateAction(p_operationCode)
    # update resultAccount.

    return resultAccount


def encodeSchedulePackage(scheduleClass): # return bytearray

    package, zero, todo_size = 0, 0, 36
    
    package = bytes("sch", encoding='utf-8')
    package += scheduleClass.get_number().to_bytes(4,'big')
    package += bytes(scheduleClass.get_todo(), encoding='UTF-8')
    package += zero.to_bytes(todo_size - (len(scheduleClass.get_todo() * 3)), 'big')
    package += scheduleClass.get_year().to_bytes(1, 'big')
    package += scheduleClass.get_month().to_bytes(1, 'big')
    package += scheduleClass.get_day().to_bytes(1, 'big')
    package += scheduleClass.get_start().to_bytes(4, 'big')
    package += scheduleClass.get_end().to_bytes(4, 'big')

    return package

def decodeSchedulePackage(package): # return AccountClass
    
    resultSchedule = Schedule()
    
    p_id, p_todo, p_year , p_month= int.from_bytes(package[:4], 'big'), package[4:40].decode('utf-8'), package[40], package[41]
    p_day, p_start, p_end = package[42], int.from_bytes(package[43:47], 'big'), int.from_bytes(package[47:51], 'big')
    
    resultSchedule.set_number(p_id)
    resultSchedule.set_todo(p_todo)
    resultSchedule.set_year(p_year)
    resultSchedule.set_month(p_month)
    resultSchedule.set_day(p_day)
    resultSchedule.set_start(p_start)
    resultSchedule.set_end(p_end)

    # update resultAccount

    return resultSchedule
