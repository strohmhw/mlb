# Import Libraries
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

# Specify URL, Run Webdriver
url = 'https://www.fangraphs.com/standings/playoff-odds/fg/mlb?date=2018-10-18&dateDelta='
phantomjs_driver = 'C:\phantomjs\bin\phantomjs'
driver = webdriver.PhantomJS()
driver.get(url)
time.sleep(30)

# Convert to Beautiful Soup
htmlSource = driver.page_source
soup = BeautifulSoup(htmlSource, 'lxml')

# Testing Environment w/ Saved HTML Doc
"""
example = open('example_fangraphs.txt', 'r')
content = example.read()
soup = BeautifulSoup(content)
"""

# Beautiful Soup Parsing Data Table
table = soup.find('table', attrs={'class': 'playoff-odds-table'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')

# Cleaning Text to Data Elements
data = []
for row in rows:
    cols = row.find_all('td')
    cols = cols[0].find_all('span', attrs={'class':'fullName'}) + cols[1:]
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
    df = pd.DataFrame(data)

# Column Naming and Export
df.columns = ['Team', 'W', 'L', 'W%', 'Proj W', 'Proj L', 'ROS W%', 'SOS', 'Win Div%',
    'Win WC', 'Make Playoffs', 'Make LDS', 'Win LDS', 'Win LCS', 'Win WS']
df.to_csv('july142018.csv')
print("Complete!")
