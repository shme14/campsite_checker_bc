from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from datetime import datetime
import os
import requests
import json 

#Important stuff
url=os.environ.get('ENV_URL')
TOKEN = os.environ.get('ENV_TOKEN')
chat_id = os.environ.get('ENV_CHATID')
delay = os.environ.get('ENV_DELAY')
port = os.environ.get('ENV_PORT')
apiURL = os.environ.get('ENV_APIURL')



def open_browser(url: str, headless=False):
    driver = webdriver.Firefox()
    driver.get(url)

    
    WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.ID, 'list-view-button-button')))
    time.sleep(2)
    element = driver.find_element(by=By.ID, value='list-view-button-button')
    driver.execute_script("$(arguments[0]).click();", element)
    #result.click()
    time.sleep(5)
    #check if the list populates with anything
    listResults = driver.find_element(By.CSS_SELECTOR, "#resource-name-0")
    print("Sites Found!")
    #Select the first list item
    firstSite = driver.find_element(By.CSS_SELECTOR, "mat-expansion-panel.mat-expansion-panel:nth-child(1)")
    firstSite.click()
    time.sleep(1)
    #Site number
    firstSiteName = driver.find_element(By.CSS_SELECTOR, ".site-details-wrapper > div:nth-child(2) > div:nth-child(1) > h2:nth-child(1)")
    print(firstSiteName.text)
    alertMe(driver,firstSiteName.text)
    #Select Reserve
    reserveButton = driver.find_element(By.CSS_SELECTOR, "#reserveButton-0")
    reserveButton.click()
    input("Press Enter to continue...")
    # try:
    # except:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - No Sites Found or Error")

    return driver

def alertMe(driver, siteNumber):
    message = "BC Site number "+ siteNumber + " found! Remote in using tailscale and avnc at http://192.168.1.50:" + port + " !"
    url2 = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url2).json()) # this sends the message

if __name__ == '__main__':
    print(url)
    print(TOKEN)
    print(chat_id)
    print(delay)
    reqcount=0
    while (1):
        count=0
        x = requests.get(apiURL)
        d = x.json()
        for i, obj in d['resourceAvailabilities'].items():
            for y in obj:
                    if (y['availability'] == 0):
                        count = count + 1
        reqcount = reqcount + 1
        curdate = datetime.now()
        print (curdate, " - How Many Sites Available: ", count, " How Many Requests: ", reqcount)
        if (count>0):
            try:
                driver = open_browser(url, headless=False)
                time.sleep(4)
                driver.quit()
            except:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - Something went wrong")
        time.sleep(int(delay))
