import requests
import json
import copy
from datetime import datetime as dt
from selenium import webdriver
from bs4 import BeautifulSoup 
from DB_Classes import *

def crawlWeather():
    url = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
    driver = webdriver.PhantomJS(executable_path = 'C:/Users/ijn95/OneDrive/桌面/Code/python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    pageBlock = soup.find('div', class_ = 'weather_data')
    cityIndex = list()

    weatherData = dict()

    for cityBlock in pageBlock:
        # print(cityBlock.attrs['name'])
        cityIndex.append(cityBlock.attrs['name'])

    for index in cityIndex:
        element = soup.find(attrs={"name" : index})
        targetAddress = url.split('/V8', 1)[0] +  element.get('href')
        # print(targetAddress)

        driver.get(targetAddress)
        subSoup = BeautifulSoup(driver.page_source, 'lxml')
        
        city = subSoup.find('h2', class_ = 'main-title').text
        information_day = subSoup.find_all('span', class_ = 'Day')
        information_night = subSoup.find_all('span', class_ = "Night")
        dates = subSoup.find_all('span', class_ = 'date')

        weather, temperature = [], []

        weatherList = list()
        weatherList_unpack = list()

        for i in range(len(information_day)):

            data_day = information_day[i].find_all()
            data_night = information_night[i].find_all()
            data_date = dates[i].find_all()

            # for element in data_day:
            #     print(element)
            # for element in data_night:
            #     print(element)
            # for element in data_date:
            #     print(element)

            weather.append(data_day[1].get('alt'))
            temperature.append(data_day[2].string)
            
            for j in range(2):
                temp_d = Weather()
                temp_d.city = city
                if j == 0:
                    data = data_day
                    temp_d.period = "早上"
                else:
                    data = data_night
                    temp_d.period = "晚上"
                temp_d.situation = data[1].get('alt')
                temp_d.min_temperature = int(data[2].string[:2])
                temp_d.max_temperature = int(data[2].string[5:])
                temp_d.month = int(data_date[1].string[:2])
                temp_d.day = int(data_date[1].string[3:])
                weatherList.append(temp_d)
                weatherList_unpack.append({'city': temp_d.city, 'period': temp_d.period, 'situation': temp_d.situation, 'max_temperature': temp_d.max_temperature, 'min_temperature': temp_d.min_temperature, 'month': temp_d.month, 'day': temp_d.day})

            
        
            # print(dates[i])
            # print('\n\n')

        # print(weather)
        # print(temperature)
        # print(weatherList)

        weatherData[city] = weatherList_unpack

    return weatherData
    # for elements in soup.find_all('table', class_ = "table"):
    #     print(elements.get('tr')) 

def checkDate():
    try:
        with open('weatherData.json', 'r') as fp:
            weatherData = json.load(fp)
            if weatherData['date'] != dt.now().day:
                writeData()
    except:
        writeData()

def writeData():
    WEATHER_DATA_LENGTH = 14 # the length of certain city's weather data

    dictData = crawlWeather()
    buf_dictData = copy.deepcopy(dictData)
    crawlDone = False

    while not crawlDone:
        crawlDone = True
        for key, value in dictData.items():
            if len(value) != WEATHER_DATA_LENGTH:
                if len(buf_dictData[key]) == WEATHER_DATA_LENGTH:
                    dictData[key] = buf_dictData[key]
                else:
                    crawlDone = False
                    break
        if not crawlDone:
            buf_dictData = crawlWeather()
            print("Crawl failed. restart crawling data. ")
        else:
            print("Crawl success.")
                

    dictData["date"] = dt.now().day
    ret = json.dumps(dictData)

    with open('weatherData.json', 'w') as fp:
        fp.write(ret)
    print('update success')

def dictData2WeatherClass(dictData):
    newDict = dict()

    for city, eleList in dictData.items():
        tempList = list()
        if city != "date":
            for ele in eleList:
                temp_d = Weather()
                temp_d.city = ele['city']
                temp_d.period = ele['period']
                temp_d.situation = ele['situation']
                temp_d.max_temperature = ele['max_temperature']
                temp_d.min_temperature = ele['min_temperature']
                temp_d.month = ele['month']
                temp_d.day = ele['day']
                tempList.append(temp_d)
            newDict[city] = tempList
    
    return newDict

def getWeatherData():
    weatherData = dict()
    try:
        with open('weatherData.json', 'r') as fp:
            weatherData = json.load(fp)
    except:
        writeData()
        with open('weatherData.json', 'r') as fp:
            weatherData = json.load(fp)

    result = dictData2WeatherClass(weatherData)
    return result

def receiptCrawler():
    main_url='https://www.etax.nat.gov.tw'
    url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W1'
    driver = webdriver.PhantomJS(executable_path = 'C:/Users/ijn95/OneDrive/桌面/Code/python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "lxml")
    data = soup.select('tbody tr td a')
    #print(data)

    count=0
    tstr='ETW183W2'
    web=[]
    for i in data:
        if i['href'].find(tstr)!=-1:
            web.append(i['href'])
            count=count+1
        if count==2: 
            break
    # print(web)  #length=28

    checkNumber=[]
    year,month=0,0
    for w in web:
        sub_url=main_url+w
        driver.get(sub_url)
        soup = BeautifulSoup(driver.page_source, "lxml")
        firstPrize = soup.select('tbody tr td.number p')
        additional=soup.select('tbody tr td.number')
        # print(firstPrize)
        # print(additional)

        subCheckNumber=[]
        for i in range(2):
            subCheckNumber.append(additional[i].text.split('、')[0].strip())
        for i in range(3):
            subCheckNumber.append(firstPrize[i].text.strip())
        for i in additional[3].text.split('、'):
            subCheckNumber.append("00000"+i.strip())
        year=int(str(int(w[23:28][:3])+1911)[2:4])
        subCheckNumber.append(year)
        if w[23:28][3]=='0':
            month=int(w[23:28][4])
        else:
            month=int(w[23:28][3:5])
        subCheckNumber.append(month)  #最後兩個是年、月

        checkNumber.append(subCheckNumber)
    # print(checkNumber)
    return checkNumber  

def writeReceiptData():
    checkNumberList = receiptCrawler()
    resultDict = dict()

    for eleList in checkNumberList:
        dictKey = ("20%02d" % eleList[-2]) + ("%02d%02d" % (eleList[-1], eleList[-1] + 1))
        tempList = list()
        for i in range(len(eleList) - 2):
            tempList.append(eleList[i])
        resultDict[dictKey] = tempList

    ret = json.dumps(resultDict)
    with open('receiptData.json', 'w') as fp:
        fp.write(ret)
    
    print("update receipt data success.")

def readReceiptData():
    receiptData = dict()
    try:
        with open('receiptData.json', 'r') as fp:
            receiptData = json.load(fp)
    except:
        writeReceiptData()
        with open('receiptData.json', 'r') as fp:
            receiptData = json.load(fp)

    return receiptData