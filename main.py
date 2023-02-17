from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import glob
import os.path
import os
import sys
import shutil

PAGE = 'https://www.cesar.school/'
EMAIL = 'seu_email@cesar.school'
PASSWORD = 'sua_senha'
FOLDER_PATH = r'path/para/local/de_download/da_sua_maquina'
FILE_TYPE = r'/*.pdf'

def move_file(month):
    DESTINY_DIR = rf'/path/para/onde/o_boleto/vai/ser/baixado/{month}'
    files = glob.glob(FOLDER_PATH + FILE_TYPE)
    max_file = max(files, key=os.path.getctime)
    if (os.path.exists(DESTINY_DIR)):
        shutil.move(max_file, DESTINY_DIR)
    else: 
        os.mkdir(DESTINY_DIR)
        shutil.move(max_file, DESTINY_DIR)

def download_boleto():
    service = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=service)
    nav.get(PAGE)
    nav.find_element('xpath', '//*[@id="onetrust-reject-all-handler"]').click()
    nav.find_element('xpath', '//*[@id="masthead"]/div[1]/div/div/div/div/div[1]/div/div/span/a[3]/span').click()
    nav.find_element('xpath', '//*[@id="identifierId"]').send_keys(EMAIL)
    nav.find_element('xpath', '//*[@id="identifierNext"]/div/button/span').click()
    time.sleep(2)
    nav.find_element('xpath', '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(PASSWORD)
    nav.find_element('xpath', '//*[@id="passwordNext"]/div/button/span').click()
    time.sleep(10)
    nav.maximize_window()
    # nav.find_element('xpath', '//*[@id="globalNavbar"]/div[2]/ion-header-bar/div[1]/span/button').click()
    time.sleep(1)
    nav.find_element('xpath', '//*[@id="ion-side-menu"]/menu-left/ion-content/div[1]/ion-list/div/div[4]/div/ion-item[8]/a[1]').click()
    nav.find_element('xpath', '//*[@id="ion-side-menu"]/menu-left/ion-content/div[1]/ion-list/div/div[4]/div/ion-item[8]/div[3]/a').click()
    time.sleep(5)
    nav.find_element('xpath', '//*[@id="ion-side-menu-content"]/ion-nav-view/ion-view/ion-content/div[1]/div/boleto-deck/div/div/div[2]/boleto-detail/div/div/div/a[1]/span').click()
    time.sleep(10)
    nav.close()

def main(argv):
    
    download_boleto()
    move_file(argv)


if __name__ == "__main__":
    main(sys.argv[1])