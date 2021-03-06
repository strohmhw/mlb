# Import Libraries
from selenium import webdriver
import datetime, time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

# Load Webdriver, could be replaced by GeckoDriver as PhantomJS is deprecated
phantomjs_driver = 'C:\phantomjs\bin\phantomjs'
driver = webdriver.PhantomJS(executable_path='/Users/hstrohm/Desktop/mlb/node_modules/phantomjs/bin/phantomjs')

""""
# Set startDate, endDate
today = datetime.date.today()
current_startDate = (today - datetime.timedelta(days=45)).strftime("%Y%m%d")
current_endDate = today.strftime("%Y%m%d")
"""

# Date and Function Function
dates = pd.date_range(pd.datetime(2018,4,5), periods=210)

def team_batters():

    team_batters_dataset = pd.DataFrame()

    for i in dates:
        ### INPUTS FOR DATA SCRAPING ###
        ################################
        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=45)).strftime("%Y-%m-%d")
        #################################
        #################################

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=&splitArrPitch=&position=B&autoPt=false&splitTeams=false&statType=team&statgroup=1&startDate=' + startDate + "&enddate=" + endDate + "&players=&filter=&endDate=" + endDate

        try:
            # Load URL, Scrap URL
            url = relevant_url
            print("Loading Team Batters URL...")
            driver.get(url)
            time.sleep(10)

            # Convert to Beautiful Soup
            htmlSource = driver.page_source
            soup = BeautifulSoup(htmlSource, 'lxml')

            # Beautiful Soup Parsing Data Table
            div_table = soup.find('div', attrs={'class': 'fg-data-grid undefined'})
            table = div_table.find('table')
            table_rows = table.find('tbody')
            rows = table_rows.find_all('tr')

            # Cleaning Text to Data Elements
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = cols[0].find_all('td', attrs={'data-stat':'Name'}) + cols[1:]
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
                df = pd.DataFrame(data)

            # Column Naming and Export
            df.columns = ['Date', 'Tm', 'G', 'PA', 'AB', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 'IBB', 'SO', 'HBP', 'SF', 'SH', 'GDP', 'SB', 'CS', 'AVG']
            df['Date'] = (unformat_endDate + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            team_batters_dataset = team_batters_dataset.append(df)
            print("Inserted team batting stats for " + endDate)

        except AttributeError:
            print("No team batting stats for " + endDate)
            continue

    team_batters_dataset.to_csv('team-batters-dataset-all.csv')

# Run Functions
team_batters()
