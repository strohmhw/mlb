# Main Script Drafting
import datetime, time
import pandas as pd

# Import CSV Data Files
AL_east = pd.read_csv('qualified-pitchers/al-east-qualified-pitchers.csv')
AL_central = pd.read_csv('qualified-pitchers/al-central-qualified-pitchers.csv')
AL_west = pd.read_csv('qualified-pitchers/al-west-qualified-pitchers.csv')
NL_east = pd.read_csv('qualified-pitchers/nl-east-qualified-pitchers.csv')
NL_central = pd.read_csv('qualified-pitchers/nl-central-qualified-pitchers.csv')
NL_west = pd.read_csv('qualified-pitchers/nl-west-qualified-pitchers.csv')

all_team_pitchers = pd.read_csv('team-pitchers-dataset-basic.csv')
all_team_batters = pd.read_csv('team-batters-dataset.csv')
all_team_pitchers_adv = pd.read_csv('team-pitchers-dataset.csv')

# Combine CSV Data Files, Add Columns
all_qualified_pitchers = pd.DataFrame()
all_qualified_pitchers = all_qualified_pitchers.append([AL_east, AL_central, AL_west, NL_east, NL_central, NL_west])
all_qualified_pitchers = all_qualified_pitchers.reset_index(drop=True)

all_team_pitchers['Date'] = (pd.to_datetime(all_team_pitchers['Date'])).astype(str)

all_qualified_pitchers['team_date'] = (all_qualified_pitchers['Tm'] + all_qualified_pitchers['Date']).astype(str)
all_team_pitchers['team_date'] = (all_team_pitchers['Tm'] + all_team_pitchers['Date']).astype(str)
all_team_pitchers_adv['team_date'] = (all_team_pitchers_adv['Tm'] + all_team_pitchers_adv['Date']).astype(str)
all_team_batters['team_date'] = (all_team_batters['Tm'] + all_team_batters['Date']).astype(str)

# Create 'Pitcher Adjusted Values' in xFIP for Each Day
team_date_xFIP = pd.Series(all_team_pitchers_adv.xFIP.values,index=all_team_pitchers_adv.team_date).to_dict()
all_qualified_pitchers['team_xFIP'] = all_qualified_pitchers['team_date'].map(team_date_xFIP)
print(all_qualified_pitchers)
all_qualified_pitchers['xFIP_diff'] = all_qualified_pitchers['xFIP'] - all_qualified_pitchers['team_xFIP']
print(all_qualified_pitchers)

# Hitting BaseRuns Calcs
all_team_batters['TB'] = (1 * all_team_batters['1B']) + (2 * all_team_batters['2B']) + (3 * all_team_batters['3B']) + (4 * all_team_batters['HR'])
all_team_batters['varA'] = all_team_batters['H'] + all_team_batters['BB'] + all_team_batters['HBP'] - all_team_batters['HR'] - .5 * all_team_batters['IBB']
all_team_batters['varB'] = (1.4 * all_team_batters['TB'] - .6 * all_team_batters['H'] - 3 * all_team_batters['HR'] + .1 * (all_team_batters['BB'] + all_team_batters['HBP'] - all_team_batters['IBB']) + .9 * (all_team_batters['SB'] - all_team_batters['CS'] - all_team_batters['GDP'])) * 1.1
all_team_batters['varC'] = all_team_batters['AB'] - all_team_batters['H'] + all_team_batters['CS'] + all_team_batters['GDP']
all_team_batters['varD'] = all_team_batters['HR']

all_team_batters.drop_duplicates(inplace=True)

all_team_batters['BsR_Sc_Season'] = ((all_team_batters['varA'] * all_team_batters['varB']) / (all_team_batters['varB'] + all_team_batters['varC'])) + all_team_batters['varD']

# Pitching BaseRuns Calcs
all_team_pitchers['varA'] = all_team_pitchers['H'] + all_team_pitchers['BB'] - all_team_pitchers['HR']
all_team_pitchers['varB'] = (1.4 * (1.12 * all_team_pitchers['H'] + 4 * all_team_pitchers['HR']) - .6 * all_team_pitchers['H'] - 3 * all_team_pitchers['HR'] + .1 * all_team_pitchers['BB']) * 1.1
all_team_pitchers['varC'] = 3 * all_team_pitchers['IP']
all_team_pitchers['varD'] = all_team_pitchers['HR']


all_team_pitchers['BsR_Al_Season'] = ((all_team_pitchers['varA'] * all_team_pitchers['varB']) / (all_team_pitchers['varB'] + all_team_pitchers['varC'])) + all_team_pitchers['varD']

# Creating Model table
model_table_batters = all_team_batters[['team_date', 'BsR_Sc_Season']]
model_table_pitchers = all_team_pitchers[['team_date', 'BsR_Al_Season']]
model_table_xFIP = all_qualified_pitchers[['team_date', 'IP', 'xFIP_diff']]

model_table = model_table_batters.merge(model_table_pitchers, on="team_date", how="left")
model_table = model_table.merge(model_table_xFIP, on="team_date", how="left")

model_table['team_date_1'] = model_table['team_date']

# Import Odds Files
odds = pd.read_csv('complete_fixed_odds.csv')
odds['team_date_1'] = odds['Team Home'] + odds['Date Home']
odds['team_date_2_chg'] = odds['Team'] + odds['Date']
complete = odds.merge(model_table, on="team_date_1", how='left')

model_table['team_date_2'] = model_table['team_date']
model_table_second = model_table
model_table_second.columns = ['team_date_chg', 'BsR_Sc_Season_chg', 'BsR_Al_Season_chg', 'IP_chg', 'xFIP_diff_chg', 'team_date_1_chg', 'team_date_2_chg']
complete = complete.merge(model_table_second, on="team_date_2_chg", how='left')

complete.to_csv('final_model_table.csv')

# Create 'Adjusted Bullpen Values', Controlling for Injuries, Usage, Etc.

# Fade Especially High BP Usage / xFIP Teams

# Left vs. Right Splits

# Heat Index for Offense





# For Hitting, we take team stats for last 45 days, adjust based on players in lineup/ performance over that time
# Adjust for new unknown players using their projections
