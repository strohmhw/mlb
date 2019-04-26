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
divisions = [AL_east, AL_central, AL_west, NL_east, NL_central, NL_west]

# Set startDate, endDate
today = datetime.date.today()
current_startDate = (today - datetime.timedelta(days=45)).strftime("%Y-%m-%d")
current_endDate = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# Define Functions
def daily_qualified_pitchers():

    qualified_pitchers = pd.DataFrame()

    for i in divisions:

        endDate = current_endDate
        startDate = current_startDate
        division = i

        relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=42,' + division + '&splitArrPitch=&position=P&autoPt=true&splitTeams=false&statType=player&statgroup=2&startDate=' + startDate + "&endDate=" + endDate + "&players=&filter="

        try:
            # Load URL, Scrap URL
            print("Loading Qualified Pitchers URL ...")
            driver.get(relevant_url)
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
            df.columns = ['Date', 'Name', 'Tm', 'IP', 'TBF', 'K/9', 'BB/9', 'K/BB', 'HR/9', 'K%', 'BB%', 'K-BB%', 'AVG', 'WHIP', 'BABIP', 'LOB%', 'FIP', 'xFIP']
            df['Date'] = endDate
            qualified_pitchers = qualified_pitchers.append(df)
            print("Inserted qualified pitchers for on " + endDate)

        except AttributeError:
            print("No qualified pitchers for on " + endDate)
            continue

    qualified_pitchers.to_csv('daily-test.csv')
def daily_team_batters():

    team_batters_dataset = pd.DataFrame()

    endDate = current_endDate
    startDate = current_startDate

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

# Run Web Scrape Functions
daily_qualified_pitchers()
daily_team_batters()

# BaseRuns Calcs
all_team_batters['TB'] = (1 * all_team_batters['1B']) + (2 * all_team_batters['2B']) + (3 * all_team_batters['3B']) + (4 * all_team_batters['HR'])
all_team_batters['varA'] = all_team_batters['H'] + all_team_batters['BB'] + all_team_batters['HBP'] - all_team_batters['HR'] - .5 * all_team_batters['IBB']
all_team_batters['varB'] = (1.4 * all_team_batters['TB'] - .6 * all_team_batters['H'] - 3 * all_team_batters['HR'] + .1 * (all_team_batters['BB'] + all_team_batters['HBP'] - all_team_batters['IBB']) + .9 * (all_team_batters['SB'] - all_team_batters['CS'] - all_team_batters['GDP'])) * 1.1
all_team_batters['varC'] = all_team_batters['AB'] - all_team_batters['H'] + all_team_batters['CS'] + all_team_batters['GDP']
all_team_batters['varD'] = all_team_batters['HR']

all_team_batters.drop_duplicates(inplace=True)

all_team_batters['BsR_Sc_Season'] = ((all_team_batters['varA'] * all_team_batters['varB']) / (all_team_batters['varB'] + all_team_batters['varC'])) + all_team_batters['varD']
