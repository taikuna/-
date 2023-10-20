# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9224 --user-data-dir="D:\github\video_editing_tool\Chrome automation\temp1"

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\github\video_editing_tool\Chrome automation\temp"
import requests
import socket as sock
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import requests

port = 9222


def start_webdriver(port):
    cmd = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=' + str(
        port) + ' --user-data-dir="D:\\github\\video_editing_tool\\Chrome automation\\temp"'
    create_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    destination = ("127.0.0.1", port)
    result = create_socket.connect_ex(destination)
    if result == 0:
        # print("Port is open")
        port1 = 'active'
    else:
        os.popen(cmd)
        print(cmd)
    create_socket.close()
    service = Service(executable_path='C:\\Users\\tiknz\\AppData\\Local\\chromedriver.exe')
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + str(port))
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu-vsync")
    driver = webdriver.Chrome(service=service, options=options)

    return driver


driver = start_webdriver(port)
action = ActionChains(driver)

if port == 9222:
    team = 'Sarajishivili'
elif port == 9224:
    team = 'Saigon FC'


def send_to_telegram(message, team):
    apiToken = '***'
    chatID = '5053481276'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        txt = message + ' (' + team + ')'
        requests.post(apiURL, json={'chat_id': chatID, 'text': txt})
        print(txt)
    except Exception as e:
        print(e)


def reset_search_query_builder(driver):
    counter = 9
    for x in range(counter):
        try:
            driver.find_element(By.XPATH,
                                '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[' + str(
                                    counter) + ']/div/div/button').click()
        except ElementNotInteractableException:
            pass
        except ElementClickInterceptedException:
            pass

        counter -= 1
    sleep(.5)


def reset_search_query(driver):
    counter1 = 9
    for x in range(counter1):
        try:
            driver.find_element(By.XPATH,
                                '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[' + str(
                                    counter1) + ']/div/div/button').click()
        except ElementNotInteractableException:
            pass
        counter1 -= 1
    sleep(.5)


def remove_bench_players(driver):
    driver.find_element(By.XPATH, "//*[contains(text(), 'WORK AREA')]").click()
    sleep(.5)
    i = 11
    while i <= 23:
        driver.find_elements(By.CLASS_NAME, 'ut-squad-slot-view')[i].click()
        try:
            send_back = driver.find_element(By.XPATH, "//*[contains(text(), 'Send to My Club')]")
            send_back.click()
        except ElementNotInteractableException:
            pass
        i += 1
        if i == 23:
            break


def select_sbc(target, driver):
    home = driver.find_element(By.CLASS_NAME, "icon-home")
    sbc = driver.find_element(By.CLASS_NAME, "icon-sbc")
    home.click()
    sleep(.5)
    sbc.click()
    sleep(1)
    all_tab = driver.find_element(By.XPATH, '/html/body/main/section/section/div[2]/div/div[1]/div/button[1]')
    all_tab.click()
    sleep(.5)

    soup = BeautifulSoup(driver.page_source, 'html5lib')
    sbcs = soup.find_all('div', class_='content-container')

    i = 0
    for sbc in sbcs:
        sbcb = sbc.find('h1', class_='tileHeader').text
        progress = sbc.find('div', class_='ut-progress-bar').text.split(' ')[0]
        son = int(progress.split('/')[0])
        mum = int(progress.split('/')[1])
        if sbcb == target and son / mum != 1:
            driver.find_elements(By.CLASS_NAME, 'content-container')[i].click()
            found = True
            break

        else:
            found = False

        i += 1

    if found:
        sleep(3)
        print(target, ' open')
        if driver.find_elements(By.CLASS_NAME, 'ut-sbc-challenge-tile-view'):
            sleep(1)
            i = 0
            while True:
                box = driver.find_elements(By.CLASS_NAME, 'ut-sbc-challenge-tile-view')[i]
                if 'disabled' not in box.get_attribute('class'):
                    box.click()
                    print(box.text, 'clicked')
                    sleep(5)
                    break
                i += 1
                if i == 50:
                    break
        else:
            sleep(0)
            pass
        if driver.find_elements(By.CLASS_NAME, 'call-to-action'):
            driver.find_element(By.CLASS_NAME, 'call-to-action').click()
        else:
            pass
        sleep(2)
        challenge = driver.find_elements(By.CLASS_NAME,'rewards-container')[0].text
        print(challenge)
        driver.find_element(By.XPATH, "//*[contains(text(), 'Clear Squad')]").click()

        sleep(1)
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'Ok')]").click()
        except NoSuchElementException:
            pass
        return found

    else:
        print(target, ' not avilable')
        return found


def search_with_condition(sort_by, quality, rarity, driver):
    sleep(.5)
    reset_search_query(driver)
    sleep(.5)
    select = driver.find_element(By.CLASS_NAME, 'ut-drop-down-control')
    select.click()
    sleep(1)
    sort = driver.find_element(By.XPATH, "//*[contains(text(), '" + sort_by + "')]")
    sort.click()
    sleep(.5)
    try:
        first = driver.find_element(By.XPATH,
                                    "/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[3]/div/div/span")
        print(first)
    except NoSuchElementException:
        pass
        first = driver.find_element(By.XPATH,
                                    "/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[3]/div/div/span")
    if quality.upper() in first.text:
        pass
    else:
        first.click()
        sleep(.5)
        if quality == 'Gold':
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[3]/div/ul/li[4]'
        elif quality == 'Silver':
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[3]/div/ul/li[3]'

        elif quality == 'Special':
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[3]/div/ul/li[5]'

        elif quality == 'Bronze':
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[3]/div/ul/li[2]'
        else:
            first.click()
            sleep(.5)
            select_path = driver.find_element(By.XPATH,
                                              '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[3]/div/div/button')
        driver.find_element(By.XPATH, select_path).click()

    rarity_button = driver.find_element(By.XPATH,
                                        '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[4]')
    rarity_button.click()
    sleep(.5)
    if rarity != '':
        driver.find_element(By.XPATH, "//*[contains(text(), '" + rarity + "')]").click()
        sleep(.5)
    # exclude = driver.find_element(By.XPATH,'/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[1]/div[1]/div[2]/div')
    # exclude.click()
    sleep(.5)
    search = driver.find_element(By.XPATH,
                                 '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[3]/button[2]')
    search.click()
    close_requrements_box(driver)
    sleep(.5)


def use_squad_builder(driver, rarity, quality, sort_by, remove_bench):
    try:
        players = driver.find_elements(By.CLASS_NAME, 'ut-squad-slot-view')[10]
        coodinate = players.location
        # perform the operation
        sleep(1)
        action.move_by_offset(coodinate['y'], coodinate['x']).click().perform()
        sleep(.5)
    except MoveTargetOutOfBoundsException or IndexError:
        try:
            driver.find_element(By.XPATH,
                                '/html/body/main/section/section/div[2]/div/div/section/div[1]/button').click()
        except NoSuchElementException:
            pass

        except NoSuchWindowException:
            pass
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Use Squad Builder')]").click()
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH,
                                '/html/body/main/section/section/div[2]/div/div/section/div[1]/button').click()
        except NoSuchElementException:
            pass

        pass
        sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(), 'Use Squad Builder')]").click()

    reset_search_query_builder(driver)
    sleep(.5)

    select = driver.find_element(By.CLASS_NAME, 'ut-drop-down-control')
    select.click()
    sleep(1)
    sort = driver.find_element(By.XPATH, "//*[contains(text(), '" + sort_by + "')]")
    sort.click()

    driver.find_element(By.XPATH,
                        "/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[3]/div/div/span").click()
    sleep(.5)
    if quality != '':
        if quality == 'Gold':
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[3]/div/ul/li[4]'
        elif quality == 'Silver':
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[3]/div/ul/li[3]'

        elif quality == 'Special':
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[3]/div/ul/li[5]'

        else:
            select_path = '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[3]/div/ul/li[2]'
        driver.find_element(By.XPATH, select_path).click()

    if rarity != '':
        driver.find_element(By.XPATH, "//*[contains(text(), '" + rarity + "')]").click()
        sleep(.5)
    driver.find_element(By.XPATH,
                        "/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[3]/button[2]").click()
    sleep(1)
    submit = driver.find_element(By.CLASS_NAME, 'call-to-action').get_attribute('class')
    if 'disable' in submit and remove_bench != 'disabled':
        remove_bench_players(driver)
    return 'None'
    try:
        close_requrements_box(driver)
    except ElementClickInterceptedException:
        pass
        error = driver.find_element(By.CLASS_NAME, 'ea-dialog-view--title').text
        return error


def exchange_players(driver):
    try:
        driver.find_element(By.CLASS_NAME, 'call-to-action').click()
    except ElementClickInterceptedException:
        pass
        driver.find_element(By.XPATH, "//*[contains(text(), 'WORK AREA')]").click()
        sleep(.5)
        driver.find_element(By.CLASS_NAME, 'call-to-action').click()

    sleep(1)
    if driver.find_elements(By.XPATH, "//*[contains(text(), 'Claim Rewards')]"):
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'Claim Rewards')]").click()
            sleep(1)
            driver.find_element(By.XPATH, "//*[contains(text(), 'Claim Rewards')]").click()
        except NoSuchElementException:
            pass

        sleep(1)
        pause = False
        print('SBC submit complete!')
        # driver.refresh()
        # sleep(7)

    else:
        pause = True

    return pause


def swap_players(sort_by, quality, rarity, rating_between, driver, team):
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Swap Player')]").click()
    except NoSuchElementException:
        pass
        driver.find_element(By.XPATH, "//*[contains(text(), 'Add Player')]").click()

    reset_search_query(driver)
    search_with_condition(sort_by, quality, rarity, driver)

    sleep(.5)

    player_found = False
    ctp = 0
    while not player_found:
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        players = soup.find_all('div', class_='entityContainer')
        i = 0
        for player in players:
            if i != 0:
                name = player.find('div', class_='name').text
                rating = player.find('div', class_='rating').text
                position = player.find('div', class_='position').text
                vert = str(rating) + ' ' + position + ' ' + name
                type1 = str(player.find('div', class_='ut-item-loaded')).split('ut-item-loaded"><')[0].replace(
                    '<div class="small player item ', '')

                if int(rating) in rating_between:
                    print('player added: ', vert)
                    add = driver.find_element(By.XPATH,
                                              '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[3]/ul/li[' + str(
                                                  i) + ']/button')
                    add.click()
                    player_found = True
                    break
            i += 1

        if not player_found:
            try:
                driver.find_element(By.CLASS_NAME, 'next').click()
                # print('click next page')
                ctp += 1
                if ctp > 50:
                    break
            except ElementNotInteractableException:
                print('player not found')
                peform_quick_sell(driver=driver, limit=3)
                # club_player_list = count_club_players(driver)
                # send_to_telegram('not enough player in the club ' + club_player_list, team)


def remove_players(hm, driver):
    i = 0
    for ii in range(hm):
        requirement = driver.find_element(By.CLASS_NAME, 'ut-popover--top')
        if 'show' in requirement.get_attribute('class'):
            requirement.click()
        driver.find_elements(By.CLASS_NAME, 'ut-squad-slot-view')[i].click()
        driver.find_element(By.XPATH, "//*[contains(text(), 'Send to My Club')]").click()
        i += 1


def open_pack(pack, qs, driver, team):
    sleep(2)
    home = driver.find_element(By.CLASS_NAME, "icon-home")
    home.click()
    sleep(.5)
    store = driver.find_element(By.CLASS_NAME, "icon-store")
    store.click()
    sleep(.5)
    driver.find_element(By.XPATH, "//*[contains(text(), 'PACKS')]").click()
    sleep(.5)
    if 'display: none;' in driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').get_attribute('style'):
        sleep(0)
    else:
        driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').click()
        sleep(.5)

    if driver.find_elements(By.XPATH, "//*[contains(text(), 'Store All in Club')]"):
        driver.find_element(By.XPATH, "//*[contains(text(), 'Store All in Club')]").click()
        sleep(1.5)
    else:
        pass

    store.click()
    sleep(.5)
    driver.find_element(By.XPATH, "//*[contains(text(), 'PACKS')]").click()
    sleep(2)
    if 'display: none;' in driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').get_attribute('style'):
        i = 0
        try:
            while True:
                pack_name = driver.find_elements(By.CLASS_NAME, 'ut-store-pack-details-view--title')[i]

                if pack.upper() == pack_name.text.upper():
                    driver.find_elements(By.CLASS_NAME, 'call-to-action')[i].click()
                    print(pack, ' opened')
                    sleep(10)
                    # sleep(7)
                    break
                i += 1
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            section = soup.find('section', class_='sectioned-item-list')
            players = section.find_all('div', class_='entityContainer')
            for player in players:
                name = player.find('div', class_='name').text
                rating = player.find('div', class_='rating').text
                position = player.find('div', class_='position').text
                vert = str(rating) + ' ' + position + ' ' + name
                if int(rating) >= 96:
                    send_to_telegram('Yeah EA! thanks for juice!\n' + vert, team)

            driver.find_element(By.XPATH, "//*[contains(text(), 'Store All in Club')]").click()
        except IndexError:
            print(pack, 'not found')
            return 'not found'
            pass
    else:
        pass
        driver.find_element(By.CLASS_NAME, 'tile').click()
        sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        players = soup.find_all('div', class_='entityContainer')
        ct = 0
        for player in players:
            name = player.find('div', class_='name').text
            rating = player.find('div', class_='rating').text
            position = player.find('div', class_='position').text
            type1 = str(player.find('div', class_='ut-item-loaded')).split('ut-item-loaded"><')[0].replace(
                '<div class="small player item ', '')
            vertification = rating + ' ' + position + ' ' + name
            driver.find_elements(By.CLASS_NAME, 'entityContainer')[ct].click()
            sleep(1)
            if int(rating) in range(40, 80):
                driver.find_element(By.XPATH, "//*[contains(text(), 'Quick Sell')]").click()
                sleep(1)
                driver.find_element(By.XPATH, "//*[contains(text(), 'Ok')]").click()
                print('Quicksold: ', vertification)
                break

        store = driver.find_element(By.CLASS_NAME, "icon-store")
        store.click()
        sleep(.5)
        driver.find_element(By.XPATH, "//*[contains(text(), 'PACKS')]").click()
        sleep(.5)
        if 'display: none;' in driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').get_attribute('style'):
            pass
        else:
            print('start 85+ to remove dublicate')
            Eightyfourplusten_x10_upgrade(dubs_limit=11, rating_req=88, target='86+ x10 Upgrade',
                                          pack=pack, driver=driver, team=team, open_after=False,sub_target='85+ x10 Upgrade')


def swap_dubes_and_reg(dubs_limit, driver):
    dubs_limit = dubs_limit
    driver.find_element(By.CLASS_NAME, 'icon-store').click()
    sleep(.5)
    driver.find_element(By.XPATH, "//*[contains(text(), 'PACKS')]").click()
    sleep(.5)
    dubs = driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view')
    if 'none' not in dubs.get_attribute('style'):
        dubs.click()
        sleep(.5)
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        players = soup.find_all('div', class_='entityContainer')
        dub_list = []
        ct = 0
        for player in players:
            name = player.find('div', class_='name').text
            rating = player.find('div', class_='rating').text
            position = player.find('div', class_='position').text
            type1 = str(player.find('div', class_='ut-item-loaded')).split('ut-item-loaded"><')[0].replace(
                '<div class="small player item ', '')
            vertification = rating + ' ' + position + ' ' + name
            # print('dubes: ', vertification)
            driver.find_elements(By.CLASS_NAME, 'entityContainer')[ct].click()
            sleep(1)
            try:
                driver.find_element(By.XPATH, "//*[contains(text(), 'Store All in Club')]").click()
            except NoSuchElementException:
                pass
            try:
                driver.find_element(By.XPATH, "//*[contains(text(), 'Swap Duplicate Item from Club')]").click()
            except NoSuchElementException:
                pass

            sleep(1)
            dub_list.append(vertification)
            if ct == dubs_limit - 1:
                break
            ct += 1
        print(dub_list)
        return dub_list


def search_dublicate_player(dubs, i, driver):
    reset_search_query(driver)
    sleep(.5)
    try:
        driver.find_element(By.XPATH,
                            '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[2]/div[3]/div/div/button').click()
    except NoSuchElementException:
        pass
    select = driver.find_element(By.CLASS_NAME, 'ut-drop-down-control')
    select.click()
    sleep(1)
    most_recent = driver.find_element(By.XPATH, "//*[contains(text(), 'Most Recent')]")
    most_recent.click()
    driver.find_element(By.XPATH,
                        '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[2]/div[2]/div[5]').click()
    # sleep(.5)
    # dub_position = dubs[i].split(' ')[1]
    # driver.find_element(By.XPATH, "//li[contains(text(), '" + dub_position + "')]").click()
    sleep(.5)
    search = driver.find_element(By.XPATH,
                                 '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div/div/div[3]/button[2]')
    search.click()
    sleep(1)
    player_found = False
    while player_found == False:
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        players = soup.find_all('div', class_='entityContainer')
        ii = 0
        for player in players:
            name = player.find('div', class_='name').text
            rating = player.find('div', class_='rating').text
            position = player.find('div', class_='position').text
            vert = str(rating) + ' ' + position + ' ' + name
            type1 = str(player.find('div', class_='ut-item-loaded')).split('ut-item-loaded"><')[0].replace(
                '<div class="small player item ', '')
            player_name = dubs[i]
            if player_name in vert:
                print('dub player added: ', vert)
                add = driver.find_element(By.XPATH,
                                          '/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[3]/ul/li[' + str(
                                              ii) + ']/button')
                # print('row added:'+str(ii))
                add.click()
                player_found = True
                break
            ii += 1
        #print(ii)
        try:
            driver.find_element(By.CLASS_NAME, 'next').click()
        except NoSuchElementException:
            pass

        # sleep(1)


def search_playerbyname(dubs, limit, driver):
    i = 0
    for x in dubs:
        sleep(1)
        p = driver.find_elements(By.CLASS_NAME, 'ut-squad-slot-view')[i]
        p.click()
        sleep(.5)
        driver.find_element(By.XPATH, "//*[contains(text(), 'Add Player')]").click()
        sleep(.5)
        search_dublicate_player(dubs, i, driver)
        i += 1
        sleep(1)
        if i >= limit:
            break


def close_requrements_box(driver):
    requirement_box = driver.find_element(By.CLASS_NAME, 'ut-popover')
    if 'show' in requirement_box.get_attribute('class'):
        driver.find_element(By.CLASS_NAME, 'ut-squad-summary-value').click()


def ultimate_bronze_upgrade(qs, driver, team):
    found = select_sbc(target='Ultimate Bronze Upgrade', driver=driver)
    if found:
        use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High', remove_bench='disabled',
                          driver=driver)
        player = fill_empty_players(sort_by='Rating Low to High', quality='', rarity='', rating_between=range(50, 65),
                                    driver=driver)
        exchange_players(driver)
        sleep(5)
        # open_pack('ULTIMATE BRONZE UPGRADE PACK', qs, driver, team)
        return player
    return found


def ultimate_silver_upgrade(qs, driver, team):
    found = select_sbc(target='Ultimate Silver Upgrade', driver=driver)
    if found:
        use_squad_builder(rarity='', quality='Silver', sort_by='Rating Low to High', remove_bench='disabled',
                          driver=driver)
        player = fill_empty_players(sort_by='Rating Low to High', quality='', rarity='', rating_between=range(65, 74),
                                    driver=driver)
        exchange_players(driver)
        sleep(5)
        # open_pack('ULTIMATE SILVER UPGRADE PACK', qs, driver, team)
        return player
    return found


def daily_bronze_upgrade(qs, driver, team):
    found = select_sbc(target='Daily Bronze Upgrade', driver=driver)
    if found:
        use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High', remove_bench='disabled',
                          driver=driver)
        player = fill_empty_players(sort_by='Rating Low to High', quality='', rarity='', rating_between=range(40, 64),
                                    driver=driver)
        exchange_players(driver)
        # open_pack('JUMBO PREMIUM BRONZE PLAYERS PACK', qs, driver, team)
        return player
    return found


def daily_silver_upgrade(qs, driver, team):
    found = select_sbc(target='Daily Silver Upgrade', driver=driver)
    if found:
        use_squad_builder(rarity='', quality='Silver', sort_by='Rating Low to High', remove_bench='disabled',
                          driver=driver)
        player = fill_empty_players(sort_by='Rating Low to High', quality='', rarity='', rating_between=range(65, 75),
                                    driver=driver)
        exchange_players(driver)
        # open_pack('JUMBO PREMIUM SILVER PLAYERS PACK', qs, driver, team)
        return player
    return found


def daily_gold_upgrade(qs, driver, team):
    found = select_sbc(target='Daily Gold Upgrade', driver=driver)
    if found:
        ran = random.choice([1, 2])
        if ran == 1:
            use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High', remove_bench='disabled',
                              driver=driver)
            player = fill_empty_players(sort_by='Rating Low to High', quality='', rarity='',
                                        rating_between=range(40, 65),
                                        driver=driver)
            remove_players(hm=5, driver=driver)
            use_squad_builder(rarity='', quality='Silver', sort_by='Rating Low to High', remove_bench='disabled',
                              driver=driver)
            fill_empty_players(sort_by='Rating Low to High', quality='Silver', rarity='', rating_between=range(65, 75),
                               driver=driver)
        else:
            use_squad_builder(rarity='', quality='Silver', sort_by='Rating Low to High', remove_bench='disabled',
                              driver=driver)
            player = fill_empty_players(sort_by='Rating Low to High', quality='Silver', rarity='',
                                        rating_between=range(65, 75),
                                        driver=driver)
            remove_players(hm=6, driver=driver)
            use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High', remove_bench='disabled',
                              driver=driver)
            fill_empty_players(sort_by='Rating Low to High', quality='', rarity='', rating_between=range(40, 65),
                               driver=driver)
        exchange_players(driver)
        return player
        # open_pack('ELEVEN GOLD PLAYERS PACK', qs, driver, team)
    return found


def peform_quick_sell(driver, limit):
    driver.find_element(By.CLASS_NAME, 'icon-club').click()
    sleep(2)
    store = driver.find_element(By.CLASS_NAME, "icon-store")
    store.click()
    sleep(.5)
    driver.find_element(By.XPATH, "//*[contains(text(), 'PACKS')]").click()
    sleep(.5)
    if 'display: none;' in driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').get_attribute('style'):
        sleep(0)
    else:
        driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').click()
        sleep(.5)

    if driver.find_elements(By.XPATH, "//*[contains(text(), 'Store All in Club')]"):
        driver.find_element(By.XPATH, "//*[contains(text(), 'Store All in Club')]").click()
        sleep(1.5)
    dubs = swap_dubes_and_reg(dubs_limit=11, driver=driver)
    if len(dubs) <= limit:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Quick Sell')]").click()
        sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(), 'Ok')]").click()


def read_result(sort_by, quality, rarity, rating_between, driver):
    search_with_condition(sort_by, quality, rarity, driver)
    sleep(2)
    stop = False
    pg = 1
    bronze = 0
    silver = 0
    gold = 0
    specials = 0
    while not stop:
        print('finding..')
        i = 0
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        players = soup.find_all('div', class_='has-tap-callback')
        for player in players:
            name = player.find('div', class_='name').text
            rating = player.find('div', class_='rating').text
            position = player.find('div', class_='position').text
            vert = str(rating) + ' ' + position + ' ' + name
            type1 = str(player.find('div', class_='ut-item-loaded')).split('ut-item-loaded"><')[0].replace(
                '<div class="small player item ', '')
            version = str(player.find('div', class_='ut-item-loaded')).split('ut-item-loaded"><')[0].replace(
                '<div class="small player item ', '').replace(' ', '')
            info = rating + ' ' + position + ' ' + name
            # print(info, version)
            # print(i)
            if version == 'specials':
                specials += 1
            elif int(rating) in range(75, 91):
                gold += 1
            elif int(rating) in range(65, 75):
                silver += 1
            elif int(rating) in range(40, 65):
                bronze += 1
            # print(vert,'row:', i, 'page:', pg)

            if int(rating) in rating_between:
                print('rr player added: ', vert)
                add = driver.find_elements(By.CLASS_NAME, 'add')[i]
                add.click()
                stop = True
                break

            elif i == 19:
                pg += 1
                driver.find_element(By.CLASS_NAME, 'next').click()
                print('next click')
                i = 0
                sleep(1)

            elif int(len(players)) - 1 == i and 'display: none;' in driver.find_element(By.CLASS_NAME,
                                                                                        'next').get_attribute('style'):
                print('len==i No player found')
                stop = True
                send_to_telegram('Bot stopped because not enough players to run', team=team)
                exit()
                break

            elif i == 20:
                print('i reached 20')
                stop = True
                break

            elif pg > 50:
                print('pg > 50 No player found')
                stop = True
                break

            elif int(rating) == 99:
                print('reached 99')
                stop = True
                send_to_telegram('Bot stopped because not enough players to run', team=team)
                player_enough = False
                return player_enough
                exit()
                break

            i += 1
        try:
            if driver.find_element(By.XPATH, "//*[contains(text(), 'No results found')]"):
                print('No results found')
                stop = True
                send_to_telegram('Bot stopped because not enough players to run', team=team)
                exit()
                break
        except NoSuchElementException:
            pass

        i = 0
        sleep(1)
        # print('last No player found')
        # exit()

        ###

    cards = bronze, silver, gold, specials

    return cards


def fill_empty_players(sort_by, quality, rarity, rating_between, driver):
    global cards
    i = 0
    cards = 'full'
    for x in range(11):
        try:
            driver.find_elements(By.CLASS_NAME, 'player')[x].click()
        except ElementClickInterceptedException:
            pass
            driver.find_element(By.XPATH, "//*[contains(text(), 'WORK AREA')]").click()
            sleep(.5)
            driver.find_elements(By.CLASS_NAME, 'player')[x].click()
        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'Add Player')]").click()
        except NoSuchElementException:
            x += 1
        else:
            cards = read_result(sort_by, quality, rarity, rating_between, driver)
            x += 1
        submit = driver.find_element(By.CLASS_NAME, 'call-to-action').get_attribute('class')
        if 'disable' not in submit:
            break

    return cards


def Eightyfourplusten_x10_upgrade(dubs_limit, rating_req, target, pack, driver, team, open_after,sub_target):
    global pack_grind
    open_packs = False
    ctta = 0
    if driver.find_elements(By.ID, 'Login'):
        driver.find_element(By.CLASS_NAME, 'call-to-action').click()
        sleep(20)
    remove_bench = ''
    sleep(5)
    home = driver.find_element(By.CLASS_NAME, "icon-home")
    home.click()
    sleep(.5)
    store = driver.find_element(By.CLASS_NAME, "icon-store")
    store.click()
    sleep(.5)
    driver.find_element(By.XPATH, "//*[contains(text(), 'PACKS')]").click()
    sleep(.5)
    if 'display: none;' in driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').get_attribute('style'):
        sleep(0)
    else:
        driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').click()
        sleep(.5)

    if driver.find_elements(By.XPATH, "//*[contains(text(), 'Store All in Club')]"):
        driver.find_element(By.XPATH, "//*[contains(text(), 'Store All in Club')]").click()
        sleep(1.5)
    else:
        pass

    dubs = swap_dubes_and_reg(dubs_limit, driver)
    def pack_loop():
        while True:
            op = open_pack(pack, qs=False, driver=driver, team=team)
            if op == 'not found':
                open_pack(pack='85+ x10 PLAYERS PACK', qs=False, driver=driver, team=team)
            dubs = swap_dubes_and_reg(dubs_limit, driver)
            # print(dubs)
            if dubs is not None:
                break

        return dubs



    if dubs is None:
        dubs = pack_loop()
    i = 0
    rating_list = []

    if len(dubs) == 1:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Quick Sell')]").click()
        sleep(1)
        driver.find_element(By.XPATH, "//*[contains(text(), 'Ok')]").click()
        print('Quicksold one dube')
        dubs = pack_loop()

    def average(rate):
        return sum(rate) / len(rate)

    for x in dubs:
        rate = int(dubs[i].split(' ')[0])
        # print(rate)
        rating_list.append(rate)
        i += 1
    average = average(rating_list)
    # print(average)
    if len(dubs) >= 3 and average >= 90:
        pass
    else:
        if sub_target is None:
            pass
        else:
            target = sub_target
            pack = '85+ x10 Players Pack'

    # print(target)
    try:
        select_sbc(target, driver)
    except NoSuchElementException:
        pass
        driver.refresh()
        sleep(15)
        select_sbc(target, driver)

    search_playerbyname(dubs, dubs_limit, driver)
    try:
        driver.find_element(By.XPATH,
                            '/html/body/main/section/section/div[2]/div/div/section/div[1]/button').click()
        sleep(1)
        driver.find_element(By.XPATH,
                            '/html/body/main/section/section/div[2]/div/div/section/div[1]/button').click()
        sleep(1)
    except NoSuchElementException:
        pass
    sleep(1)
    top = driver.find_element(By.CLASS_NAME, 'ut-popover--top')

    if 'show' in top.get_attribute('class'):

        rating_req = int(
            driver.find_element(By.XPATH, "//*[contains(text(), 'Min. Team Rating:')]").text.text.split(': ')[1])
        driver.find_element(By.CLASS_NAME, 'ut-squad-summary-info').click()
        sleep(.5)
    else:
        driver.find_element(By.CLASS_NAME, 'ut-squad-summary-info').click()
        sleep(.5)
        rating_req = int(
            driver.find_element(By.XPATH, "//*[contains(text(), 'Min. Team Rating:')]").text.split(': ')[1])
        driver.find_element(By.CLASS_NAME, 'ut-squad-summary-info').click()
    print('requirement:', str(rating_req))

    sbc = use_squad_builder(rarity='', quality='Gold', sort_by='Rating Low to High', remove_bench='', driver=driver)
    if 'NO PLAYERS FOUND' in sbc:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Ok')]").click()
        sleep(1)
        use_squad_builder(rarity='', quality='Silver', sort_by='Rating High to Low', remove_bench='', driver=driver)

    driver.find_element(By.XPATH, "//*[contains(text(), 'WORK AREA')]").click()

    cards = fill_empty_players(sort_by='Rating Low to High', quality='Gold', rarity='', rating_between=range(74, 90),
                               driver=driver)

    gold_less = False
    pack_grind = False
    if cards != 'full':
        if cards[0] <= 30 or cards[1] <= 30:
            pack_grind = True
        else:
            pack_grind = False
        if cards[3] <= 50:
            gold_less = True
        else:
            gold_less = False

    print(cards)
    if cards != 'full':
        gold_less = True

    added_counter = 0
    i = 10
    while True:
        players = driver.find_elements(By.CLASS_NAME, 'ut-squad-slot-view')[i]
        try:
            players.click()
            sleep(.5)
            cr = driver.find_element(By.XPATH,
                                     '/html/body/main/section/section/div[2]/div/div/div/div[2]/div[1]/div[' + str(
                                         i + 1) + ']/div[3]/div[5]/div[2]/div[1]').text
            # print(cr)
        except ElementClickInterceptedException:
            pass

        rating = driver.find_element(By.XPATH,
                                     '/html/body/main/section/section/div[2]/div/div/div/div[1]/div[2]/div['
                                     '1]/div/span').text
        requirement = driver.find_element(By.XPATH,
                                          '/html/body/main/section/section/div[2]/div/div/div/div[1]/div['
                                          '1]/div/span').text
        if '3/3' in requirement and int(rating) == rating_req:
            break

        elif '3/3' in requirement and int(rating) <= rating_req + 1:
            break

        elif '1/3' in requirement and int(rating) < rating_req:
            quality = 'Special'
            rarity = 'Team of the Season'
            search = 'Rating Low to High'
            rating_between = range(85, 96)

        elif '2/3' in requirement and int(rating) <= rating_req:
            quality = ''
            rarity = ''
            search = 'Rating High to Low'
            rating_between = range(80, 96)

        elif '2/3' in requirement and int(rating) >= rating_req:
            quality = 'Special'
            rarity = 'Team of the Season'
            search = 'Rating Low to High'
            rating_between = range(85, 96)

        elif int(rating) <= rating_req:
            quality = ''
            rarity = ''
            search = 'Rating High to Low'
            rating_between = range(80, 96)

        elif int(rating) >= rating_req:
            quality = ''
            rarity = ''
            search = 'Rating Low to High'
            rating_between = range(60, 80)

        else:
            quality = ''
            rarity = ''
            search = 'Rating Low to High'
            rating_between = range(74, 85)

        swap_players(search, quality, rarity, rating_between, driver, team)
        added_counter += 1
        i -= 1

        score = driver.find_element(By.XPATH,
                                    '/html/body/main/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/span').text
        sleep(1)
        if int(score) >= rating_req and int(score) <= rating_req + 1 and '3/3' in rating:
            break
        elif int(score) >= rating_req and int(score) <= rating_req + 1 and 'disabled' not in driver.find_element(
                By.CLASS_NAME, 'call-to-action').get_attribute('class'):
            break

        if i == 0:
            i += 10
        if added_counter >= 20:
            driver.find_element(By.CLASS_NAME, 'icon-club').click()
            sleep(2)
            store = driver.find_element(By.CLASS_NAME, "icon-store")
            store.click()
            sleep(.5)
            driver.find_element(By.XPATH, "//*[contains(text(), 'PACKS')]").click()
            sleep(.5)
            if 'display: none;' in driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').get_attribute('style'):
                sleep(0)
            else:
                driver.find_element(By.CLASS_NAME, 'ut-unassigned-tile-view').click()
                sleep(.5)

            if driver.find_elements(By.XPATH, "//*[contains(text(), 'Store All in Club')]"):
                driver.find_element(By.XPATH, "//*[contains(text(), 'Store All in Club')]").click()
                sleep(1.5)

            # driver.find_element(By.XPATH, "//*[contains(text(), 'Quick Sell')]").click()
            sleep(1)
            # driver.find_element(By.XPATH, "//*[contains(text(), 'Ok')]").click()

            break

    pause = exchange_players(driver)
    pack_grind = False
    if pause:
        send_to_telegram(message='SBC limit reached. pausing SBC', team=team)
        driver.refresh()
        #exit()
    if gold_less:

        open_pack(pack='Eleven Gold Players Pack', qs=True, driver=driver, team=team)
        open_pack(pack='Ultimate Silver Upgrade Pack', qs=True, driver=driver, team=team)
        #pack_grind = True

    if open_packs:
        open_pack(pack='Eleven Gold Players Pack', qs=True, driver=driver, team=team)
        open_pack(pack='Ultimate Bronze Upgrade Pack', qs=True, driver=driver, team=team)
        open_pack(pack='Ultimate Silver Upgrade Pack', qs=True, driver=driver, team=team)
        open_pack(pack='Jumbo Premium Silver Players Pack', qs=True, driver=driver, team=team)
        open_pack(pack='Jumbo Premium Bronze Players Pack', qs=True, driver=driver, team=team)


    if pack_grind:
        pack_grinding(qs=True, driver=driver, team=team, open=True)

    if open_after:
        open_pack(pack=pack, qs=False, driver=driver, team=team)
    sleep(2)
    return dubs


def pack_grinding(qs, driver, team, open):
    db = select_sbc(target='Daily Bronze Upgrade', driver=driver)
    if db:
        use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High', remove_bench='disabled',
                          driver=driver)
        fill_empty_players(sort_by='Rating Low to High', quality='', rarity='', rating_between=range(40, 65),
                           driver=driver)
        exchange_players(driver)
        if open:
            open_pack('JUMBO PREMIUM BRONZE PLAYERS PACK', qs, driver, team)

    ds = select_sbc(target='Daily Silver Upgrade', driver=driver)
    if ds:
        use_squad_builder(rarity='', quality='Silver', sort_by='Rating Low to High', remove_bench='disabled',
                          driver=driver)
        fill_empty_players(sort_by='Rating Low to High', quality='', rarity='', rating_between=range(65, 75),
                           driver=driver)
        exchange_players(driver)
        if open:
            open_pack('JUMBO PREMIUM SILVER PLAYERS PACK', qs, driver, team)

    dg = select_sbc(target='Daily Gold Upgrade', driver=driver)
    if dg:
        ran = random.choice([1, 2])
        if ran == 1:
            use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High',
                              remove_bench='disabled',
                              driver=driver)
            fill_empty_players(sort_by='Rating Low to High', quality='', rarity='',
                               rating_between=range(40, 65),
                               driver=driver)
            remove_players(hm=5, driver=driver)
            use_squad_builder(rarity='', quality='Silver', sort_by='Rating Low to High',
                              remove_bench='disabled',
                              driver=driver)
            fill_empty_players(sort_by='Rating Low to High', quality='Silver', rarity='',
                               rating_between=range(65, 75),
                               driver=driver)
        else:
            use_squad_builder(rarity='', quality='Silver', sort_by='Rating Low to High',
                              remove_bench='disabled',
                              driver=driver)
            fill_empty_players(sort_by='Rating Low to High', quality='Silver', rarity='',
                               rating_between=range(65, 75),
                               driver=driver)
            remove_players(hm=6, driver=driver)
            use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High',
                              remove_bench='disabled',
                              driver=driver)
            fill_empty_players(sort_by='Rating Low to High', quality='', rarity='',
                               rating_between=range(40, 65),
                               driver=driver)
        exchange_players(driver)
        if open:
            open_pack('ELEVEN GOLD PLAYERS PACK', qs, driver, team)
    ub = select_sbc(target='Ultimate Bronze Upgrade', driver=driver)
    if ub:
        use_squad_builder(rarity='', quality='Bronze', sort_by='Rating Low to High',
                          remove_bench='disabled', driver=driver)
        fill_empty_players(sort_by='Rating Low to High', quality='', rarity='',
                           rating_between=range(40, 64),
                           driver=driver)
        exchange_players(driver)
        sleep(5)
        if open:
            open_pack('ULTIMATE BRONZE UPGRADE PACK', qs, driver, team)
    us = select_sbc(target='Ultimate Silver Upgrade', driver=driver)
    if us:

        use_squad_builder(rarity='', quality='', sort_by='Rating Low to High',

                          remove_bench='disabled', driver=driver)

        fill_empty_players(sort_by='Rating Low to High', quality='', rarity='',

                           rating_between=range(65, 74),

                           driver=driver)

        exchange_players(driver)
        sleep(5)

        if open:
            open_pack('ULTIMATE BRONZE UPGRADE PACK', qs, driver, team)


def count_club_players(driver):
    driver.find_element(By.CLASS_NAME, 'icon-club').click()
    sleep(.5)
    driver.find_element(By.CLASS_NAME, 'players-tile').click()
    sleep(3)
    i = 0
    bronze = 0
    silver = 0
    gold = 0
    specials = 0

    while True:
        sleep(.5)
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        players = soup.find_all('div', class_='entityContainer')
        for player in players:
            name = player.find('div', class_='name').text
            rating = player.find('div', class_='rating').text
            position = player.find('div', class_='position').text
            version = str(player.find('div', class_='ut-item-loaded')).split('ut-item-loaded"><')[0].replace(
                '<div class="small player item ', '').replace(' ', '')
            info = rating + ' ' + position + ' ' + name
            # print(info, version)

            if version == 'specials':
                specials += 1
            elif int(rating) in range(75, 91):
                gold += 1
            elif int(rating) in range(65, 75):
                silver += 1
            elif int(rating) in range(40, 65):
                bronze += 1
            i += 1

        try:
            driver.find_element(By.CLASS_NAME, 'next').click()
        except ElementNotInteractableException:
            break

    club_player_list = '\nBronze: ' + str(bronze) + '\nSilver: ' + str(silver) + '\nGold: ' + str(
        gold) + '\nSpecials: ' + str(specials)
    print(club_player_list)
    return club_player_list
