from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import base64
import requests
import pytesseract
from PIL import Image
import json


caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

 
account = 'jann7790'
password = 'a60596059A@'

def crackCaptcha(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    captcha = Image.open(path)
    captcha = pytesseract.image_to_string(captcha)
    return captcha.strip('\n\x0c')


#driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps)
driver.get('https://isafeevent.moe.edu.tw/login')
 
time.sleep(5)
element = driver.find_element_by_class_name("loginBtn.b")
element.click()

element = driver.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[3]/div[1]/img')
img_base64 = element.get_attribute("src").split(',', 1)[1]
with open("captcha_login.png", 'wb') as image:
    image.write(base64.b64decode(img_base64))


code = crackCaptcha('./captcha_login.png')

element = driver.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[1]/input')
element.send_keys(account)

element = driver.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[2]/input')
element.send_keys(password)

element = driver.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[3]/div[2]/input')
element.send_keys(code)
time.sleep(3)

element = driver.find_element_by_xpath('/html/body/app-root/div/div/app-login/div/div/div[2]/div/form/div[4]/button[1]')
element.click()
time.sleep(3)
driver.switch_to.alert.accept()


element = driver.find_element_by_xpath('/html/body/app-root/div/div/app-identity/div/div[1]/div/a[2]')
element.click()

time.sleep(3)
logs_raw = driver.get_log("performance")

logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

def log_filter(log_):
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
    )

for log in filter(log_filter, logs):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["response"]["url"]
    print(f"Caught {resp_url}")
    print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
input()
