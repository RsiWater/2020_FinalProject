from DB_Classes import *
from UpdateThread import *
import time

# tempClass = Schedule()
# tempClass.set_start_in_format(2019, 2, 1, 12, 0)
# tempClass.set_end_in_format(2021, 2, 1, 12, 0)

# print(tempClass.get_start())
# print(tempClass.get_end())

# tempClass.set_relative_end_time(1,0,0,0,0)

# print(tempClass.get_end())

print(Crawl.receiptCrawler())

