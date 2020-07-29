import threading
import time
import Crawl
from datetime import datetime as dt

class UpdateThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.updateClockAtMinute = 30 # at 30 min, update.

    def run(self):
        print("Update Thread ready.")
        updateInterval = 0

        Crawl.checkDate()

        while True:            
            if dt.now().minute > self.updateClockAtMinute:
                updateInterval = self.updateClockAtMinute * 2 - dt.now().minute
            else:
                updateInterval = self.updateClockAtMinute - dt.now().minute
            updateInterval *= 60
            time.sleep(updateInterval)

            

            Crawl.writeData()
            print("server data updated.")

