import threading
import time
import Crawl
from datetime import datetime as dt
from DB_Classes import *

class UpdateThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.updateClockAtMinute = 30 # at 30 min, update.
        self.currentDay = 0

    def run(self):
        self.currentDay = dt.now().day
        updateInterval = 0

        print("Update Thread ready.")

        Crawl.checkDate()

        while True:
            if dt.now().minute > self.updateClockAtMinute:
                updateInterval = self.updateClockAtMinute * 2 - dt.now().minute
            else:
                updateInterval = self.updateClockAtMinute - dt.now().minute
            updateInterval *= 60
            time.sleep(updateInterval)

            Crawl.writeData()

            if self.currentDay != dt.now().day:
                self.currentDay = dt.now().day
                Crawl.writeReceiptData()


            print("server data updated.")

    def checkAccountInvoice(self):
        receiptData = Crawl.readReceiptData()

        accountClass = Account()
        accountClass.select_all()
        accountList = accountClass.findAll

        hitList = dict()
        # key for account id, value for invoice code.
        for key, value in receiptData.items():
            # check date.
            
            if not (int(key[4:6]) == dt.now().month or int(key[6:8]) == dt.now().month or int(key[4:6]) == dt.now().month - 2 or int(key[6:8]) == dt.now().month - 2):
                continue

            for account in accountList:
                for ele in value:
                    if account[6] == ele:
                        hitList[account[9]] = account[6]
                        break
        
        return hitList
            






