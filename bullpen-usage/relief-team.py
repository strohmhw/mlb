# Import Libraries
from selenium import webdriver
import datetime, time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

# Load Webdriver, could be replaced by GeckoDriver as PhantomJS is deprecated
phantomjs_driver = 'C:\phantomjs\bin\phantomjs'
driver = webdriver.PhantomJS()

""""
# Set startDate, endDate
today = datetime.date.today()
current_startDate = (today - datetime.timedelta(days=45)).strftime("%Y%m%d")
current_endDate = today.strftime("%Y%m%d")
"""

# Date and Function Function
dates = pd.date_range(pd.datetime(2018,4,5), periods=210)

def relief_team():

    relief_team_dataset = pd.DataFrame()

    for i in dates:
        ### INPUTS FOR DATA SCRAPING ###
        ################################
        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=45)).strftime("%Y-%m-%d")
        #################################
        #################################

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=43&splitArrPitch=&position=P&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&enddate=" + endDate + "&players=&filter=&endDate=" + endDate

        try:
            # Load URL, Scrap URL
            url = relevant_url
            print("Loading Relief Team URL...")
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
            df.columns = ['Date', 'Tm', 'IP', 'TBF', 'K/9', 'BB/9', 'K/BB', 'HR/9', 'K%', 'BB%', 'K-BB%', 'AVG', 'WHIP', 'BABIP', 'LOB%', 'FIP', 'xFIP']
            df['Date'] = (unformat_endDate + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            relief_team_dataset = relief_team_dataset.append(df)
            print("Inserted relief team stats for " + endDate)

        except AttributeError:
            print("No relief team stats for " + endDate)
            continue

    relief_team_dataset.to_csv('relief-team-pitchers.csv')

# Run Functions
relief_team()
