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
current_startDate = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
current_endDate = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# Define Functions
def daily_qualified_pitchers():

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
            daily_qualified_pitchers_df.append(df)
            print("Inserted qualified pitchers for on " + endDate)

        except AttributeError:
            print("No qualified pitchers for on " + endDate)
            continue

    daily_qualified_pitchers_df.to_csv('1_1.csv')

def daily_team_batters():

    endDate = current_endDate
    startDate = current_startDate

    relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=&splitArrPitch=&position=B&autoPt=false&splitTeams=false&statType=team&statgroup=1&startDate=' + startDate + "&enddate=" + endDate + "&players=&filter=&endDate=" + endDate

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
    df['Date'] = endDate
    daily_team_batters_df.append(df)
    print("Inserted team batting stats for " + endDate)

    daily_team_batters_df.to_csv('1_2.csv')

def daily_team_pitchers_basic():

    endDate = current_endDate
    startDate = current_startDate

    relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=42&splitArrPitch=&position=P&autoPt=false&splitTeams=false&statType=team&statgroup=1&startDate=' + startDate + "&enddate=" + endDate + "&players=&filter=&endDate=" + endDate

    # Load URL, Scrap URL
    url = relevant_url
    print("Loading Team Pitchers URL...")
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
    df.columns = ['Date', 'Tm', 'IP', 'TBF', 'ERA', 'H', '2B', '3B', 'R', 'ER', 'HR', 'BB', 'IBB', 'HBP', 'SO', 'AVG', 'OBP', 'SLG', 'wOBA']
    df['Date'] = endDate
    daily_team_pitchers_basic_df.append(df)
    print("Inserted team pitching stats for " + endDate)

    daily_team_pitchers_basic_df.to_csv('1_3.csv')

def daily_team_pitchers_advanced():

    endDate = current_endDate
    startDate = current_startDate

    relevant_url = 'https://www.fangraphs.com/leaders/splits-leaderboards?splitArr=42&splitArrPitch=&position=P&autoPt=false&splitTeams=false&statType=team&statgroup=2&startDate=' + startDate + "&enddate=" + endDate + "&players=&filter=&endDate=" + endDate

    # Load URL, Scrap URL
    url = relevant_url
    print("Loading Team Pitchers Advanced URL...")
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
    df['Date'] = endDate
    daily_team_pitchers_advanced_df.append(df)
    print("Inserted team advanced pitching stats for " + endDate)

    daily_team_pitchers_advanced_df.to_csv('1_4.csv')
############ def daily_splits_R():
############ def daily_splits_L():
############ def daily_lineups():
############ def daily_qualified_batters():

# Create dataset
daily_qualified_pitchers_df = pd.DataFrame()
daily_team_batters_df = pd.DataFrame()
daily_team_pitchers_basic_df = pd.DataFrame()
daily_team_pitchers_advanced_df = pd.DataFrame()


# Run Web Scrape Functions
daily_qualified_pitchers()
daily_team_batters()
daily_team_pitchers_basic()
daily_team_pitchers_advanced()
### daily_splits_R():
### daily_splits_L():
### daily_lineups():
### daily_qualified_batters():

# BaseRuns Scored
daily_team_batters_df['TB'] = (1 * daily_team_batters_df['1B']) + (2 * daily_team_batters_df['2B']) + (3 * daily_team_batters_df['3B']) + (4 * daily_team_batters_df['HR'])
daily_team_batters_df['varA'] = daily_team_batters_df['H'] + daily_team_batters_df['BB'] + daily_team_batters_df['HBP'] - daily_team_batters_df['HR'] - .5 * daily_team_batters_df['IBB']
daily_team_batters_df['varB'] = (1.4 * daily_team_batters_df['TB'] - .6 * daily_team_batters_df['H'] - 3 * daily_team_batters_df['HR'] + .1 * (daily_team_batters_df['BB'] + daily_team_batters_df['HBP'] - daily_team_batters_df['IBB']) + .9 * (daily_team_batters_df['SB'] - daily_team_batters_df['CS'] - daily_team_batters_df['GDP'])) * 1.1
daily_team_batters_df['varC'] = daily_team_batters_df['AB'] - daily_team_batters_df['H'] + daily_team_batters_df['CS'] + daily_team_batters_df['GDP']
daily_team_batters_df['varD'] = daily_team_batters_df['HR']
daily_team_batters_df.drop_duplicates(inplace=True)

# BaseRuns Allowed
daily_team_pitchers_basic_df['varA'] = daily_team_pitchers_basic_df['H'] + daily_team_pitchers_basic_df['BB'] - daily_team_pitchers_basic_df['HR']
daily_team_pitchers_basic_df['varB'] = (1.4 * (1.12 * daily_team_pitchers_basic_df['H'] + 4 * daily_team_pitchers_basic_df['HR']) - .6 * daily_team_pitchers_basic_df['H'] - 3 * daily_team_pitchers_basic_df['HR'] + .1 * daily_team_pitchers_basic_df['BB']) * 1.1
daily_team_pitchers_basic_df['varC'] = 3 * daily_team_pitchers_basic_df['IP']
daily_team_pitchers_basic_df['varD'] = daily_team_pitchers_basic_df['HR']
daily_team_pitchers_basic_df.drop_duplicates(inplace=True)

# Create Calculations Dataset
lines_dataset = pd.DataFrame()
lines_dataset['BsR_Sc_Season'] = ((daily_team_batters_df['varA'] * daily_team_batters_df['varB']) / (daily_team_batters_df['varB'] + daily_team_batters_df['varC'])) + daily_team_batters_df['varD']
lines_dataset['BsR_Al_Season'] = ((daily_team_pitchers_basic_df['varA'] * daily_team_pitchers_basic_df['varB']) / (daily_team_pitchers_basic_df['varB'] + daily_team_pitchers_basic_df['varC'])) + daily_team_pitchers_basic_df['varD']
