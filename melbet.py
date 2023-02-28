# import all packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import time

# set up the driver
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# get the url
url="https://melbetke.com/"
driver.get(url=url)

time.sleep(5)
driver.maximize_window()

# get the contents of the pagesource
raw_source=driver.page_source
new_source=raw_source.encode("utf-8").strip()

# create the Beautifulsoup
supuMrembo=BeautifulSoup(new_source,"html.parser")

print(supuMrembo.prettify())
# save the file in a html page for viewing
with open("melbet.html","w+",encoding="utf-8") as melbet:
    melbet.seek(0)
    melbet.truncate(0)
    melbet.write(supuMrembo.prettify())

try:
    # get the football tab and click it
    football=WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,"(//a[@id='curLoginForm'])"))
    )
    print("The element was found")
    football.click()
    time.sleep(5)
    # get the login details from the ENV file
    cell=os.getenv("NUMBER")
    password=os.getenv("PASSWORD")
    # put in the login details
    phone=driver.find_element((By.XPATH,"(//input[@id='reg_tel'])"))
    phone.send_keys(cell)
    passTextBox=driver.find_element((By.XPATH,"(//input[@id='userPassword'])"))
    passTextBox.send_keys(password)
    
    print(football.page_source)
    time.sleep(5)
    driver.close()

except:
    print("The element was not found")
    driver.close()


