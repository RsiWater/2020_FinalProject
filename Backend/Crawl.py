import requests
from selenium import webdriver
from bs4 import BeautifulSoup 
from DB_Classes import *

url = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
driver = webdriver.PhantomJS(executable_path = 'C:/Users/ijn95/OneDrive/桌面/Code/python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver.get(url)
soup = BeautifulSoup(driver.page_source, "lxml")

pageBlock = soup.find('div', class_ = 'weather_data')
cityIndex = list()

weatherData = dict()

for cityBlock in pageBlock:
    print(cityBlock.attrs['name'])
    cityIndex.append(cityBlock.attrs['name'])

for index in cityIndex:
    element = soup.find(attrs={"name" : index})
    targetAddress = url.split('/V8', 1)[0] +  element.get('href')
    print(targetAddress)

    driver.get(targetAddress)
    subSoup = BeautifulSoup(driver.page_source, 'lxml')
    
    city = subSoup.find('h2', class_ = 'main-title').text
    information_day = subSoup.find_all('span', class_ = 'Day')
    information_night = subSoup.find_all('span', class_ = "Night")
    dates = subSoup.find_all('span', class_ = 'date')

    weather, temperature = [], []

    weatherList = list()

    for i in range(len(information_day)):

        data_day = information_day[i].find_all()
        data_night = information_night[i].find_all()
        data_date = dates[i].find_all()

        for element in data_day:
            print(element)
        for element in data_night:
            print(element)
        for element in data_date:
            print(element)

        weather.append(data_day[1].get('alt'))
        temperature.append(data_day[2].string)
        
        for j in range(2):
            temp_d = Weather()
            temp_d.city = city
            if j == 0:
                data = data_day
                temp_d.period = "Day"
            else:
                data = data_night
                temp_d.period = "Night"
            temp_d.situation = data[1].get('alt')
            temp_d.max_temperature = int(data[2].string[:2])
            temp_d.min_temperature = int(data[2].string[5:])
            temp_d.month = int(data_date[1].string[:2])
            temp_d.day = int(data_date[1].string[3:])
            weatherList.append(temp_d)

        
    
        # print(dates[i])
        print('\n\n')

    print(weather)
    print(temperature)
    print(weatherList)

    weatherData[city] = weatherList
print('456')
# for elements in soup.find_all('table', class_ = "table"):
#     print(elements.get('tr')) 
