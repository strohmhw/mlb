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


# For Hitting, we take team stats for last 45 days, adjust based on players in lineup/ performancec over that time
# Adjust for new unknown players using their projections
