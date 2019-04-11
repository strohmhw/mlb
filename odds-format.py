# Script to automate the formatting and cleaning of Historical Odds excel files
# Import packages
import datetime, time
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Import CSV Data Files
odds_file = pd.read_csv('mlb-odds/mlb-odds-2018.csv')
print(odds_file)

AL_east = pd.read_csv('qualified-pitchers/al-east-qualified-pitchers.csv')
AL_central = pd.read_csv('qualified-pitchers/al-central-qualified-pitchers.csv')
NL_east = pd.read_csv('qualified-pitchers/nl-east-qualified-pitchers.csv')
AL_west = pd.read_csv('qualified-pitchers/al-west-qualified-pitchers.csv')
NL_central = pd.read_csv('qualified-pitchers/nl-central-qualified-pitchers.csv')
NL_west = pd.read_csv('qualified-pitchers/nl-west-qualified-pitchers.csv')

# Combine CSV Data Files, Add Columns
all_qualified_pitchers = pd.DataFrame()
all_qualified_pitchers = all_qualified_pitchers.append([AL_east, AL_central, AL_west, NL_east, NL_central, NL_west])
all_qualified_pitchers = all_qualified_pitchers.reset_index(drop=True)

# Fuzzy Match for Pitchers in Each Dataset
odds_pitchers = odds_file['Pitcher'].astype(str).unique()
qualified_pitchers = all_qualified_pitchers['Name'].unique()
qualified_pitchers_df = pd.DataFrame(qualified_pitchers)
qualified_pitchers_series = pd.Series(qualified_pitchers)
qualified_pitchers_split = qualified_pitchers_series.str.split(expand=True)

first_initial_list = []
for x in qualified_pitchers_split[0]:
    first_initial = x[0]
    first_initial_list.append(first_initial)


qualified_pitchers_df['qp_match'] = first_initial_list + qualified_pitchers_split[1]
qualified_pitchers_df.rename(columns={0:'qp'}, inplace=True)

base_list = []
source_list = []
match_list = []
fit_list = []
final = pd.DataFrame()

for x in odds_pitchers:
    base = x.format(str)
    str2Match = x[:-2].format(str)
    strOptions = qualified_pitchers_df['qp_match']
    highest_selected = process.extractOne(str2Match,strOptions,scorer=fuzz.partial_ratio)
    match_pitcher = highest_selected[0]
    fit = highest_selected[1]
    base_list.append(base)
    source_list.append(str2Match)
    match_list.append(match_pitcher)
    fit_list.append(fit)
    print("Inserted " + match_pitcher)

final['Pitcher'] = base_list
final['source'] = source_list
final['qp_match'] = match_list
final['fit'] = fit_list

final = final.loc[final['fit'] == 100]
final = final.loc[final['source'] != "n"]
composite = final.merge(qualified_pitchers_df, on='qp_match', how='left')
composite = composite.reset_index(drop=True)

# Merge Matched Values With Odds Files
fixed_odds = odds_file.merge(composite, on='Pitcher', how='left')
#fixed_odds = fixed_odds.loc[fixed_odds['fit'] == 100]
fixed_odds = fixed_odds.reset_index(drop=True)

fixed_dates = []

# Date Correction
for x in fixed_odds['Date']:
    date = str(x)
    day = int(date[len(date)-2:])
    month = int(date[:len(date)-2])
    year = 2018
    full_date = pd.datetime(year, month, day)
    fixed_dates.append(full_date)

fixed_odds['Date'] = fixed_dates
fixed_odds['F5'] = fixed_odds['1st'] + fixed_odds['2nd'] + fixed_odds['3rd'] + fixed_odds['4th'] + fixed_odds['5th']
fixed_odds = fixed_odds.drop(['fit', 'source', 'qp_match', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th'], axis=1)
print(fixed_odds)
# Align Home and Away Teams in Single Matchup
home_fixed_odds = fixed_odds.loc[fixed_odds['VH'] == "H"]
home_fixed_odds = home_fixed_odds.reset_index(drop=True)
home_fixed_odds.columns = ['Date Home', 'Rot Home', 'VH Home', 'Team Home', 'Pitcher Home', 'Final Home', 'Open Home', 'Close Home', 'RL Home', 'Open OU Home', 'Open Line Home,
'Close OU Home', 'Close Line Home', 'Qualified Pitcher Home', 'F5 Total Home']

away_fixed_odds = fixed_odds.loc[fixed_odds['VH'] == "V"]
away_fixed_odds = away_fixed_odds.reset_index(drop=True)

complete_fixed_odds = pd.concat([home_fixed_odds, away_fixed_odds], axis=1)

print(complete_fixed_odds)
