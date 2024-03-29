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
import numpy as np
import pandas as pd




def main():
    # set up the driver
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # get the url
    url="https://1xbet.co.ke/line/football"
    driver.get(url)

    time.sleep(10)
    driver.maximize_window()

    # get the contents of the pagesource
    raw_source=driver.page_source
    new_source=raw_source.encode("utf-8").strip()

    # print(new_source)

    # create the Beautifulsoup
    supuMrembo=BeautifulSoup(new_source,"html.parser")

    # print(supuMrembo.prettify())
    # save the file in a html page for viewing
    with open("1XBet.html","w",encoding='utf-8') as melbet:        
        melbet.write(supuMrembo.prettify())
        melbet.close()

    matches_array=[]
    home_array=[]
    away_array=[]
    comprehensive_MatchesArr=[]

    # oddsArrays
    odd_Arr=[]
    bet_Arr=[]

    # iterator for home and away arrays
    i=0
    divAll=supuMrembo.findAll("div",class_="dashboard-champ-content")
    # in each div find all sub-lists that contain the football data
    for div in divAll:
        match_names=div.findAll("span",class_="c-events__teams")
        # for all matches name find the caption span that has the match names
        for match_name in match_names:
            indi_matchNames=match_name.findAll("span",class_="c-events__team")
            for indi_match in indi_matchNames:
                match_=indi_match.text
                matches_array.append(match_.strip())
        # find all divs that have odds information
        odd_Divs=div.findAll("div",class_="c-bets")
        # for each get the odd text info
        for odd_Div in odd_Divs:
            odds=odd_Div.findAll("span",class_="c-bets__inner")
            # clean the array for the next iteration
            odd_Arr=[]
            for odd in odds:
                oddText=odd.text
                odd_Arr.append(oddText.strip())
            bet_Arr.extend(odd_Arr[0:6])

                
    # since we havae the matches, lets break them down to home and away teams
    for i in range(len(matches_array)):
        # append to the home if i is divisible by 2 and away array if not
        if(i%2==0):
            home_array.append(matches_array[i])
        else:
            away_array.append(matches_array[i])
        i=i+1

    # get the comprehensive match array from the the home and away arrays
    for x in range(len(home_array)):
        match_text=home_array[x]+" vs "+away_array[x]
        comprehensive_MatchesArr.append(match_text)





    print("******************")
    print(matches_array)
    print("The home array")
    print(home_array)
    print("The away array")
    print(away_array)
    print("The comprehensive match array")
    print(comprehensive_MatchesArr)
    print("The bet array")
    print(bet_Arr)
    # split the bet array into a 2d array by the length of the matches array
    realD=np.array_split(bet_Arr,len(comprehensive_MatchesArr))
    print("The 2D array")
    print('******************')
    print(realD)
    df=pd.DataFrame(data=realD,index=[comprehensive_MatchesArr],columns=['1','X','2','1or2','Xor2','1orX'])
    
    print("The comprehensive dataframe")
    print(df)
    # save to csv
    df.to_csv("1XBet.csv")
    return df

main()