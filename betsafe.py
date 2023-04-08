from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd


# set up the driver
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# specify the url
url="https://www.betsafe.co.ke/"
driver.get(url)
time.sleep(10)
driver.maximize_window()
# create the soup for the whole page
raw_betsafe=driver.page_source
mod_betsafe=raw_betsafe.encode("utf-8").strip()
content_betsafe=BeautifulSoup(mod_betsafe,"html.parser")
with open("betsafe.html","w") as thisF:
    thisF.seek(0)
    thisF.truncate(0)
    thisF.write(content_betsafe.prettify())
odds_Arr=[]
matches_Arr=[]
home_Arr=[]
away_Arr=[]
bet_Arr=[]
def main():
    cats=content_betsafe.find_all("div",class_="item ng-scope")
    for cat in cats:
        # find all odds
        odds=cat.find_all("div",class_="oddValue ng-binding")
        for odd in odds:
            odds_Arr.append(odd.text)
            # print(odd.text)
            # print("The first six entries")
        bet_Arr.extend(odds_Arr[0:5])
        # find all matches
        # all home matches
        homes=cat.find_all("div",class_="plr_1 ng-binding")
        for home in homes:
            home_Arr.append(home.text)
        # all away matches
        aways=cat.find_all("div",class_="plr_2 ng-binding")
        for away in aways:
            away_Arr.append(away.text)
        odds_Arr.clear()
    # couple the elements of the home and away arrays into the matches array
    print(f"The home array has a length of {len(home_Arr)}")
    print(f"The away array has a length of {len(away_Arr)}")
    for i in range(len(home_Arr)):
        mechi=home_Arr[i]+" vs "+away_Arr[i]
        matches_Arr.append(mechi)
    # print(matches_Arr)
    print(bet_Arr)
    # start the dataframe
    realD=np.array_split(bet_Arr,len(matches_Arr))
    
    # print(realD)
    df=pd.DataFrame(data=realD,index=[matches_Arr],columns=['1','X','2','1or2','Xor2','1orX'])
    print(df)
    df.to_csv("betsafe.csv")
    
main()