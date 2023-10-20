# 楽天市場から商品名や値段、販売元などを抽出するクローラーツール。　データベースはSQLを使用
import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from time import sleep
mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="****",
  database="rakuten_aff"
)

mycursor = mydb.cursor()

print(mycursor.rowcount, "record inserted.")
url = 'https://affiliate.rakuten.co.jp/search?v=2&l-id=affiliate_PC_top_g%3D555089&g=110734'
prep = '&v=2&gl=5&p='

i = 1
last_page = 0
page = requests.get(url + prep + str(i))
soup = BeautifulSoup(page.text, "html.parser")
# print(category1)
for b in soup.find_all("a", class_='page-link'):
    if b.text.isdigit():
        num = int(b.text)
        # print(b.text)
        if num >= last_page:
            last_page = num
print('Last page: ' + str(last_page))

while i <= last_page:
    print('page '+str(i)+'/'+str(last_page)+ ' scraping...')
    sleep(3)
    page = requests.get(url+prep+str(i))
    soup = BeautifulSoup(page.text, "html.parser")
    category1 = soup.findAll('option', selected=True)[0].text
    #print(category1)
    for b in soup.find_all("a",class_= 'page-link'):
        if b.text.isdigit():
            num = int(b.text)
            #print(b.text)
            if num >= last_page:
                last_page = num
    for a in soup.find_all("a", href=re.compile("https://affiliate.rakuten.co.jp/link/pc/item")):
        link = str(a['href']).split('&me_url')[0]
        ID = int(str(a['href']).split('&item_id=')[1].split('&')[0])
        shopid = int(str(link.split('me_id=')[1].split('&')[0]))
        #print(ID)
        #print(link)
        sql = "REPLACE INTO `table` (`ID`, `url`, `category1`, `shopid`, `page`) VALUES (%s, %s, %s, %s, %s)"
        #sql = "UPDATE `table` SET `ID`='"+str(ID)+"',`shopid`='"+str(shopid)+"',`url`='"+link+"',`category`='[value-4]',`category1`='"+category1+"',`link`='[value-6]',`short_link`='[value-7]',`image`='[value-8]',`text`='[value-9]'  WHERE `table`.`ID` = "+ str(ID)
        val = (ID,link,category1,shopid,i)
        #print(sql)
        mycursor.execute(sql,val)
        mydb.commit()
    i += 1

#for a in soup.find_all("a", href=lambda href: href and "https://affiliate.rakuten.co.jp/link/pc/item" in href):
#    print('Found the URL:', a['href'].split('&')[0])
