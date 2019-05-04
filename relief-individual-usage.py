# Import Libraries
from selenium import webdriver
import datetime, time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

# Load Webdriver, could be replaced by GeckoDriver as PhantomJS is deprecated
phantomjs_driver = 'C:\phantomjs\bin\phantomjs'
driver = webdriver.PhantomJS()

# League Groupings
AL_east = '164,163,177,175,172'
AL_west = '174,176,173,170,168'
AL_central = '165,166,167,169,171'
NL_east = '193,188,187,185,180'
NL_central = '181,182,186,189,190'
NL_west = '179,183,184,191,192'
divisions = ['AL_east', 'AL_central', 'AL_west', 'NL_east', 'NL_central', 'NL_west']

""""
# Set startDate, endDate
today = datetime.date.today()
current_startDate = (today - datetime.timedelta(days=45)).strftime("%Y%m%d")
current_endDate = today.strftime("%Y%m%d")
"""

# Date and Function Function
dates = pd.date_range(pd.datetime(2018,4,5), periods=10)

def relief_individual_usage():

    relief-individual-usage-dataset = pd.DataFrame()

    for i in dates:
        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

        for x in divisions:
            division = x

            relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=43,' + division + '&splitArrPitch=&position=P&autoPt=true&splitTeams=false&statType=player&statgroup=2&startDate=' + startDate + "&players=&endDate=" + endDate + '&filter=IP%7Cgt%7C0'

            try:
                # Load URL, Scrap URL
                url = relevant_url
                print("Loading Relief Individual Usage URL...")
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
                relief-individual-usage-dataset = relief-individual-usage-dataset.append(df)
                print("Inserted relief individual usage stats for " + endDate)

            except AttributeError:
                print("No relief indivdual usage stats for " + endDate)
                continue

    relief-individual-usage-dataset.to_csv('relief-individual-usage-dataset.csv')

# Run Functions
relief_individual_usage()
