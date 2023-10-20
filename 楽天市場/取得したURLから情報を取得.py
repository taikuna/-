# 1. # 楽天市場から商品名や値段、販売元などを抽出するクローラーツール。　データベースはSQLを使用
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep
import mysql.connector
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import os
options = Options()
# options.binary_location("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
options.add_argument("start-maximized")
options.add_argument("--disable-gpu-vsync")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(executable_path=r'C:\Users\tiknz\AppData\Local\chromedriver.exe', options=options)
session_id = driver.session_id
executor_url = driver.command_executor._url


def log_in():

    driver.get('https://affiliate.rakuten.co.jp/')
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/nav/div/ul[2]/li[1]/a').click()
    sleep(2)
    driver.find_element_by_xpath('/html/body/form/div/div[3]/div/div[2]/div/div[2]/div/div/div[2]/div[3]/div/div/div[1]/div/label/div/input').send_keys('****@gmail.com')
    sleep(2)
    driver.find_element_by_xpath('/html/body/form/div/div[3]/div/div[2]/div/div[2]/div/div/div[2]/div[4]/div/div').click()
    sleep(2)
    driver.find_element_by_xpath('/html/body/form/div/div[3]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/label/div/input').send_keys('****')
    sleep(2)
    driver.find_element_by_xpath('/html/body/form/div/div[3]/div/div[2]/div/div[2]/div/div/div[2]/div[4]/div/div').click()
    sleep(5)

log_in()

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="****",
  database="rakuten_aff"
)
mycursor = mydb.cursor()
while True:
    data = mycursor.execute("SELECT * FROM `table` WHERE `link` IS NULL LIMIT 1;")
    myresult = mycursor.fetchall()
    sql_data = str(myresult).replace('(','').replace(')','').replace('[','').replace(']','').replace("'",'').replace(' ','').replace(',,',',')
    print(sql_data)
    ID = sql_data.split(',')[0]
    url = sql_data.split(',')[4]

    driver.get(url)
    sleep(2)
    try:
        category = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[3]/div[1]/span[2]').text
        percentage = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[3]/div[3]/div[2]/div').text
        link_only_button = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div[1]/div/label[5]')
        link_only_button.click()
        sleep(1)
        link = driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div/textarea').get_attribute("value")

        short_link_only_button = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div[1]/div/label[4]').click()
        sleep(1)
        short_link = driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div/textarea').get_attribute("value")
        text_only_button = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div[1]/div/label[3]').click()
        sleep(1)

        text = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[1]/div/a').text.replace('　',' ').replace("'",'’').replace(',','，')
        image_button = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div[1]/div/label[1]').click()
        sleep(1)
        item_url = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[1]/div/table/tbody/tr/td/div/table/tbody/tr/td[2]/p/a').get_attribute("href")
        affiliatehtml = driver.find_element_by_xpath('/html/body/div[3]/div/div[5]/div/textarea').get_attribute("value").replace('　',' ').replace("'",'’')
        try:
            size_button = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div[4]/div/label[1]').click()
        except NoSuchElementException:
            pass
        sleep(1)
        i = 1
        while True:
            try:
                image = driver.find_element_by_xpath('/html/body/div[3]/div/form/div/div[2]/div[3]/div/div['+str(i)+']/img')
                url = image.get_attribute('src').split('?')[0]
                #print(url)
                response = requests.get(url)
                path = 'D:\\shared\\08.aff\\rakuten\\'+category+'\\'+ ID +'\\'
                isExist = os.path.exists(path)
                if not isExist:
                    # Create a new directory because it does not exist
                    os.makedirs(path)
                    #print("The new directory is created!")
                file = open(path + str(i) + ".jpg", "wb")
                file.write(response.content)
                file.close()
                i += 1
            except NoSuchElementException:
                break
    except NoSuchElementException:
        pass
        link = 'Error'
        short_link = 'Error'
        text = 'Error'
        affiliatehtml = 'Error'
    dy = datetime.today().strftime('%Y-%m-%d')
    sql = "UPDATE IGNORE `table` SET `ID`='"+ ID +"', `category`='"+category+"', `date`='"+dy+"', `html`='"+affiliatehtml+"', `link`='"+link+"',`short_link`='"+short_link+"',`text`='"+text+"',`percentage`='"+percentage+"',`item_url`='"+item_url+"' WHERE 1"
    #print(sql)
    mycursor.execute(sql)
    mydb.commit()

driver.close()
