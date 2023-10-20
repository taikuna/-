# 全国の正規トヨタディーラー情報を取得するツール
from utils.web_tool import *
import pandas as pd
csv = "data/url1.csv"
dfu = pd.read_csv(csv)
#print(dfu)
counter = 0
error_counter = 0
while True:
    if error_counter >= 1000:
        print('error +1000 times')
        break
    try:
        url = dfu.iloc[counter,0]
        HP = dfu.iloc[counter,1]
        if (pd.isnull(HP)):
            driver.get(url)
            print(url)
            sleep(1)
            company_url = str(driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div[3]/div/div[2]/div/dl[3]/dd/a').get_attribute('href').split('/?'))
            print(company_url)
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            table = soup.find_all('table')
            com_info1 = pd.read_html(str(table))[0]
            com_info = pd.read_html(str(table))[1]
            # print(com_info)
            daihyo = ''
            seturitu = ''
            sihon = ''
            uriage = ''
            tempo = ''
            employee = ''
            jigyo = ''
            kanren = ''

            company = com_info1.iloc[0, 0].replace('/',' ')
            honsha_address = driver.find_element(By.ID, 'shop_address').text
            honsha_tel = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div/div[2]/div/dl[2]/dd').text
            honsha_hp = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[3]/div/div[2]/div/dl[3]/dd/a').text
            sleep(1)

            soup = BeautifulSoup(driver.page_source, 'html5lib')
            info = soup.find_all('tr',class_='branch-info')
            result_list = []

            for i in info:
                store = i.find('span',class_='store-name').text
                phone = i.find('span',class_='is-phone-num').text
                adress = i.find('dd').text
                options = []
                for ii in i.find_all('img',class_='tjp-pc'):
                    alt = str(ii).split('"')[1]
                    options.append(alt)
                new_car = ''
                used = ''
                kei = ''
                service = ''
                disability = ''
                disability_station = ''
                if '新車' in options:
                    new_car = '●'
                if '中古車（U-Car）' in options:
                    used = '●'
                if '軽自動車' in options:
                    kei = '●'
                if '福祉車両（ウェルキャブ）' in options:
                    disability = '●'
                if 'ウェルキャブステーション' in options:
                    disability_station = '●'
                if 'サービス' in options:
                    service = '●'

                dict = {'会社名': company, '本社所在地': honsha_address, '本社電話番号': honsha_tel ,'本社HP': honsha_hp , '代表者': daihyo,'設立': seturitu, '資本金': sihon, '売上高': uriage, '従業員数': employee,'事業内容': jigyo,'関連会社': kanren,
                        '店舗': store, '所在地': adress, '電話番号': phone,  '新車': new_car, '中古車': used,
                        '軽自動車': kei, 'サービス': service, '福祉車両': disability, 'ウェルキャブステーション': disability_station}
                result_list.append(dict)

            df = pd.DataFrame(result_list)
            df.to_csv('data/toyota/'+str(counter)+' '+company+'.csv')
            dfu.iloc[counter, 1] = company
            dfu.to_csv("data/url1.csv", index=False)
        else:
            pass
        counter +=1
    except Exception:
        error_counter += 1
        pass