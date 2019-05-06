# Scraping MLB Lines, Pitchers, Injuries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np

phantomjs_driver = 'C:\phantomjs\bin\phantomjs'
driver = webdriver.PhantomJS()#executable_path='/Users/hstrohm/Desktop/mlb/node_modules/phantomjs/bin/phantomjs')

url = 'http://www.espn.com/mlb/lines'

driver.get(url)
htmlSource = driver.page_source
soup = BeautifulSoup(htmlSource, 'lxml')

# Beautiful Soup Parsing Data Table
div_table = soup.find_all('div', attrs={'class': 'mod-content'})[1]
table = div_table.find('table')
table_rows = table.find('tbody')
rows = table_rows.find_all('tr')#, attrs={'class':'oddrow'})

# Cleaning Text to Data Elements
data = []
for row in rows:
    cols = row.find_all('td')
    cols = cols[0].find_all('td') + cols[:]
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
    df = pd.DataFrame(data)

# Column Naming and Export
wg_lines = df[1].loc[df[0] == "Westgate"]
wg_lines = wg_lines.str.split("\:", expand=True)
wg_lines['test'] = wg_lines[1].str.slice(1,2)
wg_lines = wg_lines.reset_index(drop=True)
wg_lines.at[wg_lines['test'] != "-", 'Westgate Away Line'] = wg_lines[1].str.slice(0,4)
wg_lines.at[wg_lines['test'] == "-", 'Westgate Away Line'] = wg_lines[1].str.slice(0,5)
wg_lines['Westgate Home Line'] = wg_lines[2]
wg_lines = wg_lines.drop([0,1,2,'test'], axis=1)

pitchers = df[1].loc[df[0] == "Starting Pitchers"]
pitchers = pitchers.reset_index(drop=True)
pitchers = pitchers.str.split(": |\(|\)| vs.", expand=True)
pitchers.columns = ['Away Team', 'Away Pitcher', 'Away pHand', 'Away ERA', 'Home Team', 'Home Pitcher', 'Home pHand', 'Home ERA']
pitchers['Home Team'] = pitchers['Home Team'].str.slice(1,)
pitchers['Home Pitcher'] = pitchers['Home Pitcher'].str.slice(0,-1).astype(str)
pitchers['Away Pitcher'] = pitchers['Away Pitcher'].str.slice(0,-1).astype(str)
pitchers = pitchers.drop(['Away ERA', 'Home ERA'], axis=1)

team_dict = {"Arizona":'ARI', 'Atlanta':'ATL', 'Baltimore':'BAL', 'Boston':'BOS', 'Chi Cubs':'CHC', 'Chi White Sox': 'CHW', 'Cincinnati':'CIN', 'Cleveland':'CLE', 'Colorado':'COL', 'Detroit':'DET', 'Houston':'HOU', 'Kansas City':'KCR', 'LA Angels':'LAA', 'LA Dodgers':'LAD', 'Miami':'MIA', 'Milwaukee':'MIL', 'Minnesota':'MIN', 'NY Mets':'NYM', 'NY Yankees':'NYY', 'Oakland':'OAK', 'Philadelphia':'PHI', 'Pittsburgh':'PIT', 'San Diego':'SDP', 'Seattle':'SEA', 'San Francisco':'SFG', 'St. Louis':'STL', 'Tampa Bay':'TBR', 'Texas':'TEX', 'Toronto':'TOR', 'Washington':'WSN'}

pitchers["Westgate Home Line"] = wg_lines['Westgate Home Line']
pitchers["Westgate Away Line"] = wg_lines['Westgate Away Line']

pitchers['Home Symbol'] = pitchers['Home Team'].map(team_dict)
pitchers['Away Symbol'] = pitchers['Away Team'].map(team_dict)

pitchers.to_csv('daily-lines.csv')

#Injuries Table Cleansing
injuries = df[1].loc[df[0] == "Injuries"]
injuries = injuries.str.split(": |\(|\)|\,", expand=True)
