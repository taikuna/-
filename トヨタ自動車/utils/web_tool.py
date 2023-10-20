# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9224 --user-data-dir="D:\github\video_editing_tool\Chrome automation\temp1"

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\github\video_editing_tool\Chrome automation\temp"
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-first-run --incognito --window-size=1920,1080 -default-browser-check --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir')
import requests
import socket as sock
import time
import os
import platform
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
from bs4 import BeautifulSoup
import requests
import subprocess
from fake_useragent import UserAgent

port = 9222
os = platform.system()

ua = UserAgent()
user_agent = ua.random
print(user_agent)


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

def start_webdriver_mac(port):
    cmd = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-first-run --incognito --window-size=1920,1080 -default-browser-check --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir')"
    create_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    destination = ("127.0.0.1", port)
    result = create_socket.connect_ex(destination)
    if result == 0:
        # print("Port is open")
        port1 = 'active'
    else:
        file1 = subprocess.run([cmd])
        print("The exit code was: %d" % file1.returncode)
    create_socket.close()
    service = Service(executable_path=r'/usr/local/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:" + str(port))
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu-vsync")
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=service, options=options)

    return driver

if 'Win' in os:
    driver = start_webdriver(port)
else:

    driver = start_webdriver_mac(port)

action = ActionChains(driver)


