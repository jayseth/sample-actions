from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys
import time

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
website = sys.argv[1]
driver.get(website)
pause = int(sys.argv[2])
time.sleep(pause) #For pages that may take time to fully load

#Useful for verifying the page and for driver instance
#More properties available at https://github.com/SeleniumHQ/selenium/blob/trunk/py/selenium/webdriver/remote/webdriver.py
print('Current URL = ' + driver.current_url)
print('Title = ' + driver.title)
print('Name = ' + driver.name)

#Printout page source in the logs - toggle control in repo variables
if sys.argv[3] == 'true':
    print('Page Source = ' + driver.page_source)

#Sample command for accessing webdriver objects to scrape for particular page elements
tag_name = sys.argv[4]
elements = driver.find_elements(By.TAG_NAME,tag_name)
for e in elements:
    print('H1 = ' + e.text)
