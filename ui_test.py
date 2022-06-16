import time
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

_username = (By.XPATH,"//input[@id = 'username']")
_password = (By.XPATH,"//input[@id = 'password']")
_loginButton = (By.XPATH,"//button[@type='submit']")
_documents = (By.XPATH,"//span[contains(text(),'Documents')]")
_check_insert = (By.XPATH,"//a[contains(text(),'Check Inserts')]")
_spinnerGear = (By.XPATH,"//i[@class = 'fas fa-cog fa-spin']")
_search = (By.XPATH,"//input[@type='search']")
_insert_id = (By.XPATH,"//table[@id='insertsList']/tbody/tr/td")
_remittancePdfDownloadButton = (By.XPATH,"//button[@id='documentDownload']")

uidList = ['iHguaJJP','igKdHNma','7DAmKmfz']
insert_id_list = []

url = "https://websb.checkissuing.com/"
insert_url = "https://websb.checkissuing.com/inserts/view/"

options = webdriver.ChromeOptions()
profile = {
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
           "download.default_directory": "remittance_pdf/" , 
           "download.extensions_to_open": "applications/pdf",
           "safebrowsing.enabled": False
           }

options.add_experimental_option("prefs", profile)

driver = Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
driver.maximize_window()
driver.get(url)
wait = WebDriverWait(driver,3600)
wait.until(ec.presence_of_element_located(_username))
driver.find_element(*_username).send_keys("raja@centime.com")
driver.find_element(*_password).send_keys("CheckIssuing@123")
driver.find_element(*_loginButton).click()
driver.find_element(*_documents).click()
driver.find_element(*_check_insert).click()

for uid in uidList:
    wait.until(ec.invisibility_of_element_located(_spinnerGear))
    driver.find_element(*_search).send_keys(uid)
    try:
        wait.until(ec.invisibility_of_element_located(_spinnerGear))
    except:
        pass
    insert_id_list.append(driver.find_element(*_insert_id).text)
    driver.find_element(*_search).clear()

print(insert_id_list)

for insert_id in insert_id_list:
    url = insert_url + insert_id
    driver.switch_to.new_window('tab')
    driver.get(url)
    # driver.find_element(*_remittancePdfDownloadButton).click()
    time.sleep(2)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

