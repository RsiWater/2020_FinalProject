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

# test = "a123"

# scriptDir = os.path.dirname(__file__)
# dirP = "../userTrainingData/"
# filePath = test + ".json"

# # tempList = ["a123.json"]

# with open(os.path.join(scriptDir, dirP + filePath),'r',encoding='utf-8') as fp:
#     print("~~~")
#     userDetailBoard=json.load(fp)
#     print("!!!")
# print("...")

temp = UserAccount()
temp.name = 'a123'
temp.versionValidation()