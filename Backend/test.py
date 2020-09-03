from DB_Classes import *
from UpdateThread import *
import time
import os

# tempClass = Schedule()
# tempClass.set_start_in_format(2020, 7, 63, 12, 0)
# tempClass.set_end_in_format(2020, 7, 64, 12, 0)

# print(tempClass.get_start())
# print(tempClass.get_end())


# 

# temp = UpdateThread()
# print(temp.checkAccountInvoice())

test = "a123"

scriptDir = os.path.dirname(__file__)
dirP = "userTrainingData/"
filePath = dirP + test + ".json"

tempList = ["a123.json"]

for fileName in os.listdir(os.path.join(scriptDir, dirP)):
    if fileName in tempList:
        print("wow!!")
    print(fileName)
