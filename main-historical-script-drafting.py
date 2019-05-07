# Main Script Drafting
import datetime, time
import pandas as pd

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
team_batters_vsL_advanced_df_2018 = pd.read_csv('   .csv')
team_batters_vsR_advanced_df_2018 = pd.read_csv('     .csv')
team_batters_vsAll_advanced_df_2018 = pd.read_csv('   .csv')

# Combine CSV Data Files, Add Columns
qualified_pitchers_df_2018 = pd.DataFrame()
qualified_pitchers_df_2018 = qualified_pitchers_df_2018.append([AL_east, AL_central, AL_west, NL_east, NL_central, NL_west])
qualified_pitchers_df_2018 = qualified_pitchers_df_2018.reset_index(drop=True)

qualified_pitchers_df_2018['team_date'] = (qualified_pitchers_df_2018['Tm'] + qualified_pitchers_df_2018['Date']).astype(str)
team_batters_df_2018['team_date'] = (team_batters_df_2018['Tm'] + team_batters_df_2018['Date']).astype(str)
team_pitchers_basic_df_2018['team_date'] = (team_pitchers_basic_df_2018['Tm'] + team_pitchers_basic_df_2018['Date']).astype(str)
team_Spitchers_advanced_df_2018['team_date'] = (team_Spitchers_advanced_df_2018['Tm'] + team_Spitchers_advanced_df_2018['Date']).astype(str)
team_batters_vsL_advanced_df_2018['team_date'] =
team_batters_vsR_advanced_df_2018['team_date'] =
team_batters_vsAll_advanced_df_2018['team_date'] =

# Create 'Pitcher Adjusted Values' in xFIP for Each Day
team_date_xFIP = pd.Series(team_Spitchers_advanced_df_2018.xFIP.values,index=team_Spitchers_advanced_df_2018.team_date).to_dict()
qualified_pitchers_df_2018['team_xFIP'] = qualified_pitchers_df_2018['team_date'].map(team_date_xFIP)
qualified_pitchers_df_2018['xFIP_diff'] = qualified_pitchers_df_2018['xFIP'] - qualified_pitchers_df_2018['team_xFIP']
qualified_pitchers_df_2018['Pitcher_Date'] = qualified_pitchers_df_2018['Name'] + qualified_pitchers_df_2018['Date']
print(qualified_pitchers_df_2018)

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
"""daily_team_batters_vsAll_advanced_df = daily_team_batters_vsAll_advanced_df.merge(daily_team_batters_vsL_advanced_df[['Tm', 'wRC+']], how='left', left_on='Tm', right_on='Tm')
daily_team_batters_vsAll_advanced_df = daily_team_batters_vsAll_advanced_df.merge(daily_team_batters_vsR_advanced_df[['Tm', 'wRC+']], how='left', left_on='Tm', right_on='Tm')
daily_team_batters_vsAll_advanced_df.rename(columns = {'wRC+_x':'wRC+_All','wRC+_y':'wRC+_L','wRC+':'wRC+_R'}, inplace=True)
daily_team_batters_vsAll_advanced_df['vs_L_Adj'] = daily_team_batters_vsAll_advanced_df['wRC+_L'] / daily_team_batters_vsAll_advanced_df['wRC+_All']
daily_team_batters_vsAll_advanced_df['vs_R_Adj'] = daily_team_batters_vsAll_advanced_df['wRC+_R'] / daily_team_batters_vsAll_advanced_df['wRC+_All']
"""

# Creating Model table
"""model_table_batters = team_batters_df_2018[['team_date', 'BsR_Sc_Season']]
model_table_pitchers = team_pitchers_basic_df_2018[['team_date', 'BsR_Al_Season']]
model_table_xFIP = qualified_pitchers_df_2018[['team_date', 'IP', 'xFIP_diff']]

model_table = model_table_batters.merge(model_table_pitchers, on="team_date", how="left")
model_table = model_table.merge(model_table_xFIP, on="team_date", how="left")
"""

# Import Remaining Necessary Packages
historical_lines_2018_file = pd.read_csv('historical-backtest/complete-fixed-odds-2018.csv')

# Model Table Creation
historical_lines_2018 = pd.DataFrame()
historical_lines_2018 = historical_lines_2018_file[['Date_x', 'Team_x', 'Final_x', 'Open_x', 'Close_x', 'qp_x', 'Team_y', 'Final_y', 'Open_y', 'Close_y', 'qp_y']]
historical_lines_2018['Home_Pitcher_Date'] = historical_lines_2018['qp_x'].astype(str) + historical_lines_2018['Date_x']
historical_lines_2018['Away_Pitcher_Date'] = historical_lines_2018['qp_y'].astype(str) + historical_lines_2018['Date_x']

daily_model = historical_lines_2018.merge(daily_qualified_pitchers_df[['Pitcher', 'xFIP']], how='left', left_on='Home Pitcher', right_on='Pitcher')
daily_model = daily_model.merge(daily_qualified_pitchers_df[['Pitcher', 'xFIP']], how='left', left_on='Away Pitcher', right_on='Pitcher')
daily_model = daily_model.drop(['Pitcher_x', 'Pitcher_y'], axis=1)

print(odds)
odds['team_date_1'] = odds['Team Home'] + odds['Date Home']
odds['team_date_2_chg'] = odds['Team'] + odds['Date']
complete = odds.merge(model_table, on="team_date_1", how='left')

model_table['team_date_2'] = model_table['team_date']
model_table_second = model_table
model_table_second.columns = ['team_date_chg', 'BsR_Sc_Season_chg', 'BsR_Al_Season_chg', 'IP_chg', 'xFIP_diff_chg', 'team_date_1_chg', 'team_date_2_chg']
complete = complete.merge(model_table_second, on="team_date_2_chg", how='left')

complete.to_csv('final_model_table.csv')

# Create 'Adjusted Bullpen Values', Controlling for Injuries, Usage, Etc.

# Left vs. Right Splits

# Heat Index for Offense





# For Hitting, we take team stats for last 45 days, adjust based on players in lineup/ performance over that time
# Adjust for new unknown players using their projections
