import requests
from selenium import webdriver
from bs4 import BeautifulSoup 

url = 'https://www.cwb.gov.tw/V8/C/W/County/index.html'
driver = webdriver.PhantomJS(executable_path = 'C:/Users/ijn95/OneDrive/桌面/Code/python/phantomjs-2.1.1-windows/bin/phantomjs.exe')
driver.get(url)
soup = BeautifulSoup(driver.page_source, "lxml")

element = soup.find(attrs={"name" : "C64"})
targetAddress = url.split('/V8', 1)[0] +  element.get('href')
print(targetAddress)

driver.get(targetAddress)
soup = BeautifulSoup(driver.page_source, 'lxml')

information_day = soup.find_all('span', class_ = 'Day')
information_night = soup.find_all('span', class_ = "Night")
dates = soup.find_all('span', class_ = 'date')

wheather, temperature = [], []

for i in range(len(information_day)):
    data_day = information_day[i].find_all()
    data_night = information_night[i].find_all()
    for element in data_day:
        print(element)
    for element in data_night:
        print(element)

    wheather.append(data_day[1].get('alt'))
    temperature.append(data_day[2].get('alt'))

    # print(dates[i])
    print('\n\n')

print(wheather)

# for elements in soup.find_all('table', class_ = "table"):
#     print(elements.get('tr')) 
