import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait 
from selenium.webdriver.common.by import By 
from openpyxl import load_workbook
import os

# Get each site data
def get_data(driver):
    page = 15
    while page != 16:
        url = 'https://carsandbids.com/past-auctions/?page={page}'.format(page=page)
        driver.get(url)
        element_present= EC.presence_of_element_located((By.CLASS_NAME, 'hero'))
        wait(driver,20).until(element_present)
        content = driver.page_source
        soup = BeautifulSoup(content)
        #print(content)
        for d in soup.find_all('li',attrs={'class':'auction-item'})[25]:
            get_car_data(d)
        try:
            page += 1
        except TimeoutException as ex:
            driver.close()
            os.exit(1)

#Get car data
def get_car_data(i):
    URL = 'https://carsandbids.com' + i.find("a",href=True).get("href")
    title = i.find("a").get('title')
    driver.get(URL)
    ele = EC.presence_of_element_located((By.CLASS_NAME, 'quick-facts'))
    wait(driver,20).until(ele)
    content_page = driver.page_source
    soup_page = BeautifulSoup(content_page)
    pr = soup_page.find("span",attrs={'class':'bid-value'}).text
    if pr is None:
        price = '$0'
    else:
        price = pr
    print(price)
    pdata = soup_page.find("div",attrs={'class':'quick-facts'})
    dd_data = pdata.find_all('dd')
    make = dd_data[0].text
    model = dd_data[1].find("a").text
    year = title.split(" ")[0]
    body = dd_data[-4].text
    fuel = 'Gasoline'
    transm = dd_data[-5].text
    mileage = dd_data[2].text
    condition='Used'
    country='US'
    cdata = dd_data[5].text
    cdata = cdata.replace(', ',";").split(";")
    region = cdata[1].split(" ")[0]
    city = dd_data[5].text.split(", ")[0]
    zipd = cdata[-1].split(" ")[-1]
    picdata = soup_page.find("div",attrs={"id":"gallery-preview-ref"})
    mainpic = picdata.find("img").get("src")
    otpicdata = soup_page.find("div",attrs={'class':'draggable'}) 
    images = []
    for img in otpicdata.find_all("img"):
        images.append(img.get('src'))
    desc = get_desc_data(soup_page)
    lst = [URL,title,price,make,model,year,body,fuel,transm,mileage,condition,country,region,city,zipd,mainpic,str(images[1:]),desc]
    save_data(lst)

#get description data
def get_desc_data(page):
    lst = []
    data = page.find_all("div",attrs={'class':'detail-section'})
    for d in data[1:len(data)]:
        a = d.text
        lst.append(a)
    return "\n".join(lst[0:len(lst)-1])

# Save data
def save_data(lst):
    wb = load_workbook('answer.xlsx')
    work_sheet = wb.active # Get active sheet
    work_sheet.append(lst)
    wb.save('answer.xlsx')

if __name__ == "__main__":
    chrome_path = "C://Users//SVP//IgnisTech task//chromedriver"
    driver = webdriver.Chrome(chrome_path)
    get_data(driver)