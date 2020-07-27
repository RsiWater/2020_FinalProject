from DB_Classes import *

tempClass = Schedule()
tempClass.set_start_in_format(2020, 2, 1, 12, 0)
tempClass.set_end_in_format(2021, 2, 1, 12, 0)

print(tempClass.get_start())
print(tempClass.get_end())