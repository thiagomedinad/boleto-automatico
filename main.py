from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import locale
import smtplib
import ssl
from email.message import EmailMessage
import time
import glob
import os.path
import os
import sys
import shutil


EMAIL = 'tmd@cesar.school'
CURRENT_MONTH = datetime.now().strftime('%B')
EMAIL_SENDER = 'boletoautomaticoinsta@gmail.com'
EMAIL_SENDER_PASSWORD = 'ziguqknssboygxir'
PASSWORD = '#Thelordoftherings2014'
FOLDER_PATH = r'/home/thiagomedinad/Downloads'
FILE_TYPE = r'/*.pdf'

# def move_file(month):
#     DESTINY_DIR = rf'/home/thiagomedinad/Documents/boletos-CESARSCHOOL/{month}'
#     files = glob.glob(FOLDER_PATH + FILE_TYPE)
#     max_file = max(files, key=os.path.getctime)
#     if (os.path.exists(DESTINY_DIR)):
#         shutil.move(max_file, DESTINY_DIR)
#     else: 
#         os.mkdir(DESTINY_DIR)
#         shutil.move(max_file, DESTINY_DIR)

def send_email(destination):
    files = glob.glob(FOLDER_PATH + FILE_TYPE)
    max_file = max(files, key=os.path.getctime)   

    ticket_name = 'SeuBoleto-{month}.pdf'.format(month = CURRENT_MONTH)

    os.rename(max_file, f'SeuBoleto-{CURRENT_MONTH}.pdf')
    
    subject = 'O seu boleto desse mês está aqui. Não ia esquecer, né? ;)'
    em = EmailMessage()
    em['From'] = EMAIL_SENDER
    em['To'] = destination
    em['Subject'] = subject

    with open(ticket_name, 'rb') as f:
        file_data = f.read()
        file_name = f.name
        em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_SENDER_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, destination, em.as_string())


def download_boleto(school):
    service = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=service)

    if (school == '1'):
        PAGE = 'https://www.cesar.school/'
        nav.get(PAGE)
        time.sleep(3)
        nav.find_element('xpath', '//*[@id="onetrust-reject-all-handler"]').click()
        nav.find_element('xpath', '//*[@id="masthead"]/div[1]/div/div/div/div/div[1]/div/div/span/a[3]/span').click()
        time.sleep(1)
        nav.find_element('xpath', '//*[@id="identifierId"]').send_keys(EMAIL)
        nav.find_element('xpath', '//*[@id="identifierNext"]/div/button/span').click()
        time.sleep(2)
        nav.find_element('xpath', '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(PASSWORD)
        nav.find_element('xpath', '//*[@id="passwordNext"]/div/button/span').click()
        time.sleep(7)
        nav.maximize_window()
        time.sleep(2.7)
        nav.find_element('xpath', '//*[@id="ion-side-menu"]/menu-left/ion-content/div[1]/ion-list/div/div[4]/div/ion-item[8]/a[1]').click()
        nav.find_element('xpath', '//*[@id="ion-side-menu"]/menu-left/ion-content/div[1]/ion-list/div/div[4]/div/ion-item[8]/div[3]/a').click()
        time.sleep(2.7)
        nav.find_element('xpath', '//*[@id="ion-side-menu-content"]/ion-nav-view/ion-view/ion-content/div[1]/div/boleto-deck/div/div/div[2]/boleto-detail/div/div/div/a[1]/span').click()
        time.sleep(4.5)
        nav.close()

    elif (school == '2'):
        PAGE = 'https://www.fps.edu.br/area-estudante'
        nav.get(PAGE)
        nav.maximize_window()
        time.sleep(2)
        nav.find_element('xpath', '//*[@id="acesso-estudante-fps"]/div[2]/div/div[3]/div/div[2]/div/div/a/img').click()

        # Mudar para a janela que abriu ao clicar no link
        nav.switch_to.window(nav.window_handles[1])

        nav.find_element(By.XPATH, '/html/body/ion-nav-view/div/div/div[2]/div/form/div/label[1]/input').click()
        nav.find_element('xpath', '//*[@id="username"]').send_keys(EMAIL)
        nav.find_element('xpath', '//*[@id="password"]').click()
        time.sleep(1)
        nav.find_element('xpath', '//*[@id="password"]').send_keys(PASSWORD)
        nav.find_element('xpath', '//*[@id="button-login"]').click()
        time.sleep(2.5)
        nav.find_element('xpath', '//*[@id="ion-side-menu"]/menu-left/ion-content/div[1]/ion-list/div/div[4]/div/ion-item[7]/a[1]').click()
        nav.find_element('xpath', '//*[@id="ion-side-menu"]/menu-left/ion-content/div[1]/ion-list/div/div[4]/div/ion-item[7]/div[1]/a/span').click()
        time.sleep(2.2)
        nav.find_element('xpath', '//*[@id="ion-side-menu-content"]/ion-nav-view/ion-view/ion-content/div[1]/div/boleto-deck/div/div/div[2]/boleto-detail/div/div/div/a[1]/span').click()
        time.sleep(4)
        nav.close()

def main(email, school):

    download_boleto(school)
    send_email(email)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])