import threading
import time
import Crawl
import DB_Classes
import os
import json
from datetime import datetime as dt
from DB_Classes import *

class UpdateThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.updateClockAtMinute = 30 # at 30 min, update.
        self.currentDay = 0

    def run(self):
        # Crawl.writeReceiptData()
        self.currentDay = dt.now().day
        updateInterval = 0

        print("Update Thread starting.")

        print("Start checking weather data.")
        Crawl.checkDate()
        print("Weather data updated.")

        print("Update operation has already completed..")

        self.checkUserTrainingData()

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

    def checkUserTrainingData(self):
        scriptDir = os.path.dirname(__file__)
        folderDir = "../userTrainingData/"

        userAccountClass = DB_Classes.UserAccount()
        accoutDataList = userAccountClass.selectAll()

        print("Start checking user training data.")

        relFilePath = os.path.join(scriptDir, folderDir)
        fileNameList = os.listdir(relFilePath)

        for accountData in accoutDataList:
            accountFileName = accountData[0] + ".json"
            if accountFileName in fileNameList:
                print("User: " + accountData[0] + " Exists.")
                fileNameList.remove(accountFileName)
            else:
                print("User: " + accountData[0] + " does not exist. Recreating the user's training data.")
                with open(os.path.join(scriptDir, folderDir + accountFileName), 'w') as fp:
                    dfp = open(os.path.join(scriptDir, folderDir + "detail_default.json"), 'r', encoding = "UTF-8")
                    tempDict = json.load(dfp)
                    fp.write(json.dumps(tempDict))
    
        fileNameList.remove("detail_default.json")

        for fileName in fileNameList:
            print(fileName + " is redundant. Deleting the file.")
            os.remove(os.path.join(scriptDir, folderDir + fileName))
                
        print("The operation of checking user training data has completed. ")        
            






