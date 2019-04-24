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

all_team_pitchers = pd.read_csv('team-pitchers-dataset.csv')

all_team_batters = pd.read_csv('team-batters-dataset-all.csv')

# Combine CSV Data Files, Add Columns
all_qualified_pitchers = pd.DataFrame()
all_qualified_pitchers = all_qualified_pitchers.append([AL_east, AL_central, AL_west, NL_east, NL_central, NL_west])
all_qualified_pitchers = all_qualified_pitchers.reset_index(drop=True)

all_qualified_pitchers['team_date'] = all_qualified_pitchers['Tm'] + all_qualified_pitchers['Date']
all_team_pitchers['team_date'] = all_team_pitchers['Tm'] + all_team_pitchers['Date']
team_date_xFIP = pd.Series(all_team_pitchers.xFIP.values,index=all_team_pitchers.team_date).to_dict()

# Create 'Pitcher Adjusted Values' in xFIP for Each Day
all_qualified_pitchers['team_xFIP'] = all_qualified_pitchers['team_date'].map(team_date_xFIP)
all_qualified_pitchers['xFIP_diff'] = all_qualified_pitchers['xFIP'] - all_qualified_pitchers['team_xFIP']
print(all_qualified_pitchers)

# Create 'Adjusted Bullpen Values', Controlling for Injuries, Usage, Etc.




# Fade Especially High BP Usage / xFIP Teams



# BaseRuns Calcs
all_team_batters['TB'] = (1 * all_team_batters['1B']) + (2 * all_team_batters['2B']) + (3 * all_team_batters['3B']) + (4 * all_team_batters['HR'])
all_team_batters['varA'] = all_team_batters['H'] + all_team_batters['BB'] + all_team_batters['HBP'] - all_team_batters['HR'] - .5 * all_team_batters['IBB']
all_team_batters['varB'] = (1.4 * all_team_batters['TB'] - .6 * all_team_batters['H'] - 3 * all_team_batters['HR'] + .1 * (all_team_batters['BB'] + all_team_batters['HBP'] - all_team_batters['IBB']) + .9 * (all_team_batters['SB'] - all_team_batters['CS'] - all_team_batters['GDP'])) * 1.1
all_team_batters['varC'] = all_team_batters['AB'] - all_team_batters['H'] + all_team_batters['CS'] + all_team_batters['GDP']
all_team_batters['varD'] = all_team_batters['HR']

all_team_batters.drop_duplicates(inplace=True)

all_team_batters['BsR_Sc_Season'] = ((all_team_batters['varA'] * all_team_batters['varB']) / (all_team_batters['varB'] + all_team_batters['varC'])) + all_team_batters['varD']
all_team_batters['BsR_Sc_Game'] = all_team_batters['BsR_Sc_Season'] / all_team_batters['PA'] * 38


all_team_batters.to_csv('hank.csv')

print(all_team_batters)

""" Pitching
A = H + BB - HR
B = (1.4 * (1.12 * H + 4 * HR) - .6 * H - 3 * HR + .1 * BB) * 1.1
C = 3 * IP
D = HR"""



# For Hitting, we take team stats for last 45 days, adjust based on players in lineup/ performancec over that time
# Adjust for new unknown players using their projections
