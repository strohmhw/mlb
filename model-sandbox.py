# Model Sandbox 2018
# Import packages
import pandas as pd
import datetime, time
import numpy as np

# Import files
odds_file = pd.read_csv('complete-fixed-odds-2018.csv')

AL_east = pd.read_csv('qualified-pitchers/al-east-qualified-pitchers.csv')
AL_central = pd.read_csv('qualified-pitchers/al-central-qualified-pitchers.csv')
AL_west = pd.read_csv('qualified-pitchers/al-west-qualified-pitchers.csv')
NL_east = pd.read_csv('qualified-pitchers/nl-east-qualified-pitchers.csv')
NL_central = pd.read_csv('qualified-pitchers/nl-central-qualified-pitchers.csv')
NL_west = pd.read_csv('qualified-pitchers/nl-west-qualified-pitchers.csv')

# Combine CSV Data Files, Add Columns
all_qualified_pitchers = pd.DataFrame()
all_qualified_pitchers = all_qualified_pitchers.append([AL_east, AL_central, AL_west, NL_east, NL_central, NL_west])
all_qualified_pitchers = all_qualified_pitchers.reset_index(drop=True)

# Create Pitcher-Date
all_qualified_pitchers['date_pitcher'] = all_qualified_pitchers['Date'] + all_qualified_pitchers['Name']
odds_file['date_pitcher_x'] = odds_file['Date_x'] + odds_file['qp_x']
odds_file['xFIP_x'] = ""
odds_file['date_pitcher_y'] = odds_file['Date_x'] + odds_file['qp_y']
odds_file['xFIP_y'] = ""
odds_file_list = odds_file['date_pitcher_x'].append(odds_file['date_pitcher_y'])

for i in odds_file_list:
    try:
        xFIP = all_qualified_pitchers.loc[all_qualified_pitchers['date_pitcher'] == i, 'xFIP'].values[0]
        odds_file.at[odds_file['date_pitcher_x'] == i, 'xFIP_x'] = xFIP
        odds_file.at[odds_file['date_pitcher_y'] == i, 'xFIP_y'] = xFIP
    except IndexError:
        continue

odds_file['xFIP_x'] = pd.to_numeric(odds_file['xFIP_x'])
odds_file['xFIP_y'] = pd.to_numeric(odds_file['xFIP_y'])
odds_file['combined_xFIP'] = odds_file['xFIP_x'] + odds_file['xFIP_y']

change_odds_file = odds_file.loc[odds_file['xFIP_x'] > 0]
qualified_games = change_odds_file.loc[change1_odds_file['xFIP_y'] > 0]
qg = qualified_games.reset_index(drop=True)

qg['Final_z'] = qg['Final_x'] + qg['Final_y']
qg['Result_diff'] = qg['Final_z'] - qg['Open OU_x']



qg.to_csv('test.csv')
