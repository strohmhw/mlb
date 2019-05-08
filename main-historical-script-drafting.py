# Main Script Drafting
import datetime, time
import pandas as pd
import numpy as np

# Import CSV Data Files
AL_east = pd.read_csv('historical-backtest/qualified-pitchers/al-east-qualified-pitchers.csv')
AL_central = pd.read_csv('historical-backtest/qualified-pitchers/al-central-qualified-pitchers.csv')
AL_west = pd.read_csv('historical-backtest/qualified-pitchers/al-west-qualified-pitchers.csv')
NL_east = pd.read_csv('historical-backtest/qualified-pitchers/nl-east-qualified-pitchers.csv')
NL_central = pd.read_csv('historical-backtest/qualified-pitchers/nl-central-qualified-pitchers.csv')
NL_west = pd.read_csv('historical-backtest/qualified-pitchers/nl-west-qualified-pitchers.csv')

team_batters_df_2018 = pd.read_csv('historical-backtest/team-batters-dataset-2018.csv')
team_pitchers_basic_df_2018 = pd.read_csv('historical-backtest/team-pitchers-dataset-2018.csv')
team_Spitchers_advanced_df_2018 = pd.read_csv('historical-backtest/team-Spitchers-advanced-dataset-2018.csv')
team_batters_vsL_advanced_df_2018 = pd.read_csv('historical-backtest/team-batters-vsL.csv')
team_batters_vsR_advanced_df_2018 = pd.read_csv('historical-backtest/team-batters-vsR.csv')
team_batters_vsAll_advanced_df_2018 = pd.read_csv('historical-backtest/team-batters-vsAll.csv')

# Combine CSV Data Files, Add Columns
qualified_pitchers_df_2018 = pd.DataFrame()
qualified_pitchers_df_2018 = qualified_pitchers_df_2018.append([AL_east, AL_central, AL_west, NL_east, NL_central, NL_west])
qualified_pitchers_df_2018 = qualified_pitchers_df_2018.reset_index(drop=True)

qualified_pitchers_df_2018['team_date'] = (qualified_pitchers_df_2018['Tm'] + qualified_pitchers_df_2018['Date']).astype(str)
team_batters_df_2018['team_date'] = (team_batters_df_2018['Tm'] + team_batters_df_2018['Date']).astype(str)
team_pitchers_basic_df_2018['team_date'] = (team_pitchers_basic_df_2018['Tm'] + team_pitchers_basic_df_2018['Date']).astype(str)
team_Spitchers_advanced_df_2018['team_date'] = (team_Spitchers_advanced_df_2018['Tm'] + team_Spitchers_advanced_df_2018['Date']).astype(str)
team_batters_vsL_advanced_df_2018['team_date'] = (team_batters_vsL_advanced_df_2018['Tm'] + team_batters_vsL_advanced_df_2018['Date']).astype(str)
team_batters_vsR_advanced_df_2018['team_date'] = (team_batters_vsR_advanced_df_2018['Tm'] + team_batters_vsR_advanced_df_2018['Date']).astype(str)
team_batters_vsAll_advanced_df_2018['team_date'] = (team_batters_vsAll_advanced_df_2018['Tm'] + team_batters_vsAll_advanced_df_2018['Date']).astype(str)

# Create 'Pitcher Adjusted Values' in xFIP for Each Day
team_date_xFIP = pd.Series(team_Spitchers_advanced_df_2018.xFIP.values,index=team_Spitchers_advanced_df_2018.team_date).to_dict()
qualified_pitchers_df_2018['team_xFIP'] = qualified_pitchers_df_2018['team_date'].map(team_date_xFIP)
qualified_pitchers_df_2018['xFIP_diff'] = qualified_pitchers_df_2018['xFIP'] - qualified_pitchers_df_2018['team_xFIP']
qualified_pitchers_df_2018['Pitcher_Date'] = qualified_pitchers_df_2018['Name'] + qualified_pitchers_df_2018['Date']

# Hitting BaseRuns Calcs
team_batters_df_2018['TB'] = (1 * team_batters_df_2018['1B']) + (2 * team_batters_df_2018['2B']) + (3 * team_batters_df_2018['3B']) + (4 * team_batters_df_2018['HR'])
team_batters_df_2018['varA'] = team_batters_df_2018['H'] + team_batters_df_2018['BB'] + team_batters_df_2018['HBP'] - team_batters_df_2018['HR'] - .5 * team_batters_df_2018['IBB']
team_batters_df_2018['varB'] = (1.4 * team_batters_df_2018['TB'] - .6 * team_batters_df_2018['H'] - 3 * team_batters_df_2018['HR'] + .1 * (team_batters_df_2018['BB'] + team_batters_df_2018['HBP'] - team_batters_df_2018['IBB']) + .9 * (team_batters_df_2018['SB'] - team_batters_df_2018['CS'] - team_batters_df_2018['GDP'])) * 1.1
team_batters_df_2018['varC'] = team_batters_df_2018['AB'] - team_batters_df_2018['H'] + team_batters_df_2018['CS'] + team_batters_df_2018['GDP']
team_batters_df_2018['varD'] = team_batters_df_2018['HR']
team_batters_df_2018.drop_duplicates(inplace=True)
team_batters_df_2018['BsR_Sc_Season'] = ((team_batters_df_2018['varA'] * team_batters_df_2018['varB']) / (team_batters_df_2018['varB'] + team_batters_df_2018['varC'])) + team_batters_df_2018['varD']

# Pitching BaseRuns Calcs
team_pitchers_basic_df_2018['varA'] = team_pitchers_basic_df_2018['H'] + team_pitchers_basic_df_2018['BB'] - team_pitchers_basic_df_2018['HR']
team_pitchers_basic_df_2018['varB'] = (1.4 * (1.12 * team_pitchers_basic_df_2018['H'] + 4 * team_pitchers_basic_df_2018['HR']) - .6 * team_pitchers_basic_df_2018['H'] - 3 * team_pitchers_basic_df_2018['HR'] + .1 * team_pitchers_basic_df_2018['BB']) * 1.1
team_pitchers_basic_df_2018['varC'] = 3 * team_pitchers_basic_df_2018['IP']
team_pitchers_basic_df_2018['varD'] = team_pitchers_basic_df_2018['HR']
team_pitchers_basic_df_2018.drop_duplicates(inplace=True)
team_pitchers_basic_df_2018['BsR_Al_Season'] = ((team_pitchers_basic_df_2018['varA'] * team_pitchers_basic_df_2018['varB']) / (team_pitchers_basic_df_2018['varB'] + team_pitchers_basic_df_2018['varC'])) + team_pitchers_basic_df_2018['varD']

# Create Team Specific L vs. R Splits
team_batters_vsAll_advanced_df_2018 = team_batters_vsAll_advanced_df_2018.merge(team_batters_vsL_advanced_df_2018[['team_date', 'wRC+']], how='left', left_on='team_date', right_on='team_date')
team_batters_vsAll_advanced_df_2018 = team_batters_vsAll_advanced_df_2018.merge(team_batters_vsR_advanced_df_2018[['team_date', 'wRC+']], how='left', left_on='team_date', right_on='team_date')
team_batters_vsAll_advanced_df_2018.rename(columns = {'wRC+_x':'wRC+_All','wRC+_y':'wRC+_L','wRC+':'wRC+_R'}, inplace=True)
team_batters_vsAll_advanced_df_2018['vs_L_Adj'] = team_batters_vsAll_advanced_df_2018['wRC+_L'] / team_batters_vsAll_advanced_df_2018['wRC+_All']
team_batters_vsAll_advanced_df_2018['vs_R_Adj'] = team_batters_vsAll_advanced_df_2018['wRC+_R'] / team_batters_vsAll_advanced_df_2018['wRC+_All']

# Creating Model table
model_table_batters = team_batters_df_2018[['team_date', 'BsR_Sc_Season']]
model_table_pitchers = team_pitchers_basic_df_2018[['team_date', 'BsR_Al_Season']]
model_table_xFIP = qualified_pitchers_df_2018[['team_date', 'IP', 'xFIP_diff']]

model_table = model_table_batters.merge(model_table_pitchers, on="team_date", how="left")
model_table = model_table.merge(model_table_xFIP, on="team_date", how="left")

# Import Remaining Necessary Packages
historical_lines_2018_file = pd.read_csv('historical-backtest/complete-fixed-odds-2018.csv')

# Model Table Creation
historical_lines_2018 = pd.DataFrame()
historical_lines_2018 = historical_lines_2018_file[['Date_x', 'Team_x', 'Final_x', 'Open_x', 'Close_x', 'qp_x', 'Team_y', 'Final_y', 'Open_y', 'Close_y', 'qp_y']]
historical_lines_2018['Home_Pitcher_Date'] = historical_lines_2018['qp_x'] + historical_lines_2018['Date_x']
historical_lines_2018['Away_Pitcher_Date'] = historical_lines_2018['qp_y'] + historical_lines_2018['Date_x']
historical_lines_2018['Home_Team_Date'] = historical_lines_2018['Team_x'] + historical_lines_2018['Date_x']
historical_lines_2018['Away_Team_Date'] = historical_lines_2018['Team_y'] + historical_lines_2018['Date_x']

historical_lines_2018 = historical_lines_2018.merge(qualified_pitchers_df_2018[['Pitcher_Date', 'xFIP', 'team_xFIP']], how='left', left_on='Home_Pitcher_Date', right_on='Pitcher_Date')
historical_lines_2018 = historical_lines_2018.merge(qualified_pitchers_df_2018[['Pitcher_Date', 'xFIP', 'team_xFIP']], how='left', left_on='Away_Pitcher_Date', right_on='Pitcher_Date')
historical_lines_2018 = historical_lines_2018.drop(['Pitcher_Date_x', 'Pitcher_Date_y'], axis=1)

historical_lines_2018 = historical_lines_2018.merge(model_table[['team_date', 'BsR_Sc_Season', 'BsR_Al_Season']], how='left', left_on='Home_Team_Date', right_on='team_date')
historical_lines_2018 = historical_lines_2018.merge(model_table[['team_date', 'BsR_Sc_Season', 'BsR_Al_Season']], how='left', left_on='Away_Team_Date', right_on='team_date')

# Daily Win % Calculation
historical_lines_2018['Exp_Win_%_Home'] = np.power(historical_lines_2018['BsR_Sc_Season_x'],1.83) / (np.power(historical_lines_2018['BsR_Sc_Season_x'],1.83) + np.power(historical_lines_2018['BsR_Al_Season_x'],1.83))
historical_lines_2018['Exp_Win_%_Away'] = np.power(historical_lines_2018['BsR_Sc_Season_y'],1.83) / (np.power(historical_lines_2018['BsR_Sc_Season_y'],1.83) + np.power(historical_lines_2018['BsR_Al_Season_y'],1.83))

# Pitcher Split Adjustment ######## FIX ODDS File to include pitcher hand
historical_lines_2018['BsR_Sc_Season_Home_Split'] = (historical_lines_2018['BsR_Sc_Season_x'] * (historical_lines_2018['vs_L_Adj_x']).where(historical_lines_2018['Home pHand'] == 'L', (historical_lines_2018['BsR_Sc_Season_x'] * historical_lines_2018['vs_R_Adj_x']) * .60))
historical_lines_2018['BsR_Sc_Season_Away_Split'] = (historical_lines_2018['BsR_Sc_Season_y'] * (historical_lines_2018['vs_L_Adj_y']).where(historical_lines_2018['Away pHand'] == 'L', (historical_lines_2018['BsR_Sc_Season_y'] * historical_lines_2018['vs_R_Adj_y']) * .60))

# XFIP Adjustments
historical_lines_2018['xFIP_adj_Home'] = ((historical_lines_2018['xFIP_x'] - historical_lines_2018['team_xFIP_x']) * .60 + historical_lines_2018['team_xFIP_x']) / historical_lines_2018['team_xFIP_x']
historical_lines_2018['xFIP_adj_Away'] = ((historical_lines_2018['xFIP_y'] - historical_lines_2018['team_xFIP_y']) * .60 + historical_lines_2018['team_xFIP_y']) / historical_lines_2018['team_xFIP_y']
historical_lines_2018['BsR_Al_Season_Home'] = historical_lines_2018['BsR_Al_Season_x'] * historical_lines_2018['xFIP_adj_Home']
historical_lines_2018['BsR_Al_Season_Away'] = historical_lines_2018['BsR_Al_Season_y'] * historical_lines_2018['xFIP_adj_Away']

###### FIX FROM HERE
# Down AFTER SPLIT ADJUSTMENT

# Daily Win% With xFIP Adjustments & L/R Split Adjustments
historical_lines_2018['Exp_Win_%_Home_Final'] = np.power(historical_lines_2018['BsR_Sc_Season_Home_Split'],1.83) / (np.power(historical_lines_2018['BsR_Sc_Season_Home_Split'],1.83) + np.power(historical_lines_2018['BsR_Al_Season_Home'],1.83))
historical_lines_2018['Exp_Win_%_Away_Final'] = np.power(historical_lines_2018['BsR_Sc_Season_Away_Split'],1.83) / (np.power(historical_lines_2018['BsR_Sc_Season_Away_Split'],1.83) + np.power(historical_lines_2018['BsR_Al_Season_Away'],1.83))

# Game Specific Win% w/ Home Field Advantage
historical_lines_2018['Exp_Win_%_Home_Driver'] = (historical_lines_2018['Exp_Win_%_Home_Final'] / (historical_lines_2018['Exp_Win_%_Home_Final'] + historical_lines_2018['Exp_Win_%_Away_Final'])) * 1.08
historical_lines_2018['Exp_Win_%_Away_Driver'] = (historical_lines_2018['Exp_Win_%_Away_Final'] / (historical_lines_2018['Exp_Win_%_Away_Final'] + historical_lines_2018['Exp_Win_%_Home_Final'])) * .92
historical_lines_2018['Model_Win_%_Home'] = (historical_lines_2018['Exp_Win_%_Home_Driver'] + (1-historical_lines_2018['Exp_Win_%_Away_Driver']))/2
historical_lines_2018['Model_Win_%_Away'] = (historical_lines_2018['Exp_Win_%_Away_Driver'] + (1-historical_lines_2018['Exp_Win_%_Home_Driver']))/2

## Calculate Line % Implication
historical_lines_2018['Implied Win % Home'] = (abs(historical_lines_2018['Westgate Home Line']) / (abs(historical_lines_2018['Westgate Home Line']) + 100)).where(historical_lines_2018['Westgate Home Line'] < 0, (100 / (historical_lines_2018['Westgate Home Line'] + 100)))
historical_lines_2018['Implied Win % Away'] = (abs(historical_lines_2018['Westgate Away Line']) / (abs(historical_lines_2018['Westgate Away Line']) + 100)).where(historical_lines_2018['Westgate Away Line'] < 0, (100 / (historical_lines_2018['Westgate Away Line'] + 100)))

## Calculate EDGE Per Games
historical_lines_2018['EDGE % Home'] = historical_lines_2018['Model_Win_%_Home'] - historical_lines_2018['Implied Win % Home']
historical_lines_2018['EDGE % Away'] = historical_lines_2018['Model_Win_%_Away'] - historical_lines_2018['Implied Win % Away']

# Left vs. Right Splits





# Heat Index for Offense
# Create 'Adjusted Bullpen Values', Controlling for Injuries, Usage, Etc.
# For Hitting, we take team stats for last 45 days, adjust based on players in lineup/ performance over that time
# Adjust for new unknown players using their projections
