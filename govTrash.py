from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import base64
import requests
import pytesseract
from PIL import Image
 
account = 'jann7790'
password = 'a60596059A@'

def crackCaptcha(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    captcha = Image.open(path)
    captcha = pytesseract.image_to_string(captcha)
    return captcha.strip('\n\x0c')


browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://isafeevent.moe.edu.tw/login')
 
time.sleep(5)
element = browser.find_element_by_class_name("loginBtn.b")
element.click()

element = browser.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[3]/div[1]/img')
img_base64 = element.get_attribute("src").split(',', 1)[1]
with open("captcha_login.png", 'wb') as image:
    image.write(base64.b64decode(img_base64))


code = crackCaptcha('./captcha_login.png')

element = browser.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[1]/input')
element.send_keys(account)

element = browser.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[2]/input')
element.send_keys(password)

element = browser.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[3]/div[2]/input')
element.send_keys(code)

element = browser.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[4]/button[1]')
element.click()

browser.switchTo().alert().accept()




