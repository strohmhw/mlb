# Import Libraries
from selenium import webdriver
import datetime, time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

# Load Webdriver, could be replaced by GeckoDriver as PhantomJS is deprecated
phantomjs_driver = 'C:\phantomjs\bin\phantomjs'
driver = webdriver.PhantomJS()

# Set Dates and Empty Dataframe
dates = pd.date_range(pd.datetime(2018,5,2), periods=31)

def three_day_usage():

    three_day_usage = pd.DataFrame()

    for i in dates:
        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        #
        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=43&splitArrPitch=&position=P&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&players=&endDate=" + endDate + '&filter='
        #
        try:
            # Load URL, Scrap URL
            print("Loading 3 Day Trailing...")
            driver.get(relevant_url)
            time.sleep(5)

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
            three_day_usage = three_day_usage.append(df)
            print("Inserted 3 day bullpen usage for " + endDate)

        except AttributeError:
            print("No bullpen usage for " + endDate)
            continue

    three_day_usage.to_csv('three_day_usage.csv')

def seven_day_usage():

    seven_day_usage = pd.DataFrame()

    for i in dates:
        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=43&splitArrPitch=&position=P&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&players=&endDate=" + endDate + '&filter='

        try:
            # Load URL, Scrap URL
            print("Loading 7 Day Trailing...")
            driver.get(relevant_url)
            time.sleep(5)

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
            seven_day_usage = seven_day_usage.append(df)
            print("Inserted 7 day bullpen usage for " + endDate)

        except AttributeError:
            print("No bullpen usage for " + endDate)
            continue

    seven_day_usage.to_csv('seven_day_usage.csv')

def thirty_day_usage():

    thirty_day_usage = pd.DataFrame()

    for i in dates:
        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=43&splitArrPitch=&position=P&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&players=&endDate=" + endDate + '&filter='

        try:
            # Load URL, Scrap URL
            print("Loading Thirty Day Trailing...")
            driver.get(relevant_url)
            time.sleep(5)

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
            thirty_day_usage = thirty_day_usage.append(df)
            print("Inserted 30 day bullpen usage for " + endDate)

        except AttributeError:
            print("No bullpen usage for " + endDate)
            continue

    thirty_day_usage.to_csv('thirty_day_usage.csv')

def current_day_result():

    current_day_result = pd.DataFrame()

    for i in dates:
        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate).strftime("%Y-%m-%d")
        #
        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=43&splitArrPitch=&position=P&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&players=&endDate=" + endDate + '&filter='
        #
        try:
            # Load URL, Scrap URL
            print("Loading Current Day Result...")
            driver.get(relevant_url)
            time.sleep(5)

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
            df['Date'] = (unformat_endDate).strftime("%Y-%m-%d")
            current_day_result = current_day_result.append(df)
            print("Inserted Current Day Result for " + endDate)

        except AttributeError:
            print("No current day result for " + endDate)
            continue

    current_day_result.to_csv('current_day_result.csv')

# Run Scripts
#three_day_usage()
#seven_day_usage()
#thirty_day_usage()
current_day_result()
