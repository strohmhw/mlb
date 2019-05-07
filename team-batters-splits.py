# Import Libraries
from selenium import webdriver
import datetime, time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import numpy as np

# Load Webdriver, could be replaced by GeckoDriver as PhantomJS is deprecated
phantomjs_driver = 'C:\phantomjs\bin\phantomjs'
driver = webdriver.PhantomJS()#executable_path='/Users/hstrohm/Desktop/mlb/node_modules/phantomjs/bin/phantomjs')

# Set startDate, endDate
dates = pd.date_range(pd.datetime(2018,3,28), periods=225)

def team_batters_vsL_advanced():

    team_batters_vsL_df = pd.DataFrame()

    for i in dates:

        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=45)).strftime("%Y-%m-%d")

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=1&splitArrPitch=&position=B&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&players=&filter=&endDate=" + endDate

        try:
            # Load URL, Scrap URL
            url = relevant_url
            print("Loading Team Batters vs. L URL...")
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
            df.columns = ['Date', 'Tm', 'PA', 'BB%', 'K%', 'BB/K', 'AVG', 'OBP', 'SLG', 'OPS', 'ISO', 'BABIP', 'wRC', 'wRAA', 'wOBA', 'wRC+']
            df['Date'] = endDate
            df['Handedness'] = 'Vs. L'
            team_batters_vsL_df = team_batters_vsL_df.append(df)
            print("Inserted team batting stats vs. L for " + endDate)

        except AttributeError:
            print("No team batting stats for " + endDate)
            continue

    team_batters_vsL_df.to_csv('team_batters_vsL.csv')

def team_batters_vsR_advanced():

    team_batters_vsR_df = pd.DataFrame()

    for i in dates:

        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=45)).strftime("%Y-%m-%d")

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=2&splitArrPitch=&position=B&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&enddate=" + endDate + "&players=&filter=&endDate=" + endDate

        try:
            # Load URL, Scrap URL
            url = relevant_url
            print("Loading Team Batters vs. R URL...")
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
            df.columns = ['Date', 'Tm', 'PA', 'BB%', 'K%', 'BB/K', 'AVG', 'OBP', 'SLG', 'OPS', 'ISO', 'BABIP', 'wRC', 'wRAA', 'wOBA', 'wRC+']
            df['Date'] = endDate
            df['Handedness'] = 'Vs. R'
            team_batters_vsR_df = team_batters_vsR_df.append(df)
            print("Inserted team batting stats vs. R for " + endDate)

        except AttributeError:
            print("No team batting stats for " + endDate)
            continue

    team_batters_vsR_df.to_csv('team_batters_vsR.csv')

def team_batters_vsAll_advanced():

    team_batters_vsAll_df = pd.DataFrame()

    for i in dates:

        unformat_endDate = i
        endDate = unformat_endDate.strftime("%Y-%m-%d")
        startDate = (unformat_endDate - datetime.timedelta(days=45)).strftime("%Y-%m-%d")

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=&splitArrPitch=&position=B&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&enddate=" + endDate + "&players=&filter=&endDate=" + endDate

        try:
            # Load URL, Scrap URL
            url = relevant_url
            print("Loading Team Batters vs. All URL...")
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
            df.columns = ['Date', 'Tm', 'PA', 'BB%', 'K%', 'BB/K', 'AVG', 'OBP', 'SLG', 'OPS', 'ISO', 'BABIP', 'wRC', 'wRAA', 'wOBA', 'wRC+']
            df['Date'] = endDate
            df['Handedness'] = 'Vs. All'
            team_batters_vsAll_df = team_batters_vsAll_df.append(df)
            print("Inserted team batting stats vs. All for " + endDate)

        except AttributeError:
            print("No team batting stats for " + endDate)
            continue

    team_batters_vsAll_df.to_csv('team_batters_vsAll.csv')

team_batters_vsL_advanced()
team_batters_vsR_advanced()
team_batters_vsAll_advanced()
