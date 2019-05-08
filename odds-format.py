# Script to automate the formatting and cleaning of Historical Odds excel files
# Import packages
import datetime, time
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Import CSV Data Files
odds_file = pd.read_csv('mlb-odds/mlb-odds-2018.csv')

AL_east = pd.read_csv('historical-backtest/qualified-pitchers/al-east-qualified-pitchers.csv')
AL_central = pd.read_csv('historical-backtest/qualified-pitchers/al-central-qualified-pitchers.csv')
AL_west = pd.read_csv('historical-backtest/qualified-pitchers/al-west-qualified-pitchers.csv')
NL_east = pd.read_csv('historical-backtest/qualified-pitchers/nl-east-qualified-pitchers.csv')
NL_central = pd.read_csv('historical-backtest/qualified-pitchers/nl-central-qualified-pitchers.csv')
NL_west = pd.read_csv('historical-backtest/qualified-pitchers/nl-west-qualified-pitchers.csv')

# Combine CSV Data Files, Add Columns
all_qualified_pitchers = pd.DataFrame()
all_qualified_pitchers = all_qualified_pitchers.append([AL_east, AL_central, AL_west, NL_east, NL_central, NL_west])
all_qualified_pitchers = all_qualified_pitchers.reset_index(drop=True)

# Fuzzy Match for Pitchers in Each Dataset
odds_pitchers = odds_file['Pitcher'].astype(str).unique()

odds_pitcher_hand = []
for x in odds_pitchers:
    Handedness = x[-1]
    odds_pitcher_hand.append(Handedness)

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
final['hand'] = odds_pitcher_hand

final = final.loc[final['fit'] == 100]
final = final.loc[final['source'] != "n"]
composite = final.merge(qualified_pitchers_df, on='qp_match', how='left')
composite = composite.reset_index(drop=True)

fixed_odds = pd.DataFrame()
# Merge Matched Values With Odds Files
fixed_odds = odds_file.merge(composite, on='Pitcher', how='left')
#fixed_odds = fixed_odds.loc[fixed_odds['fit'] == 100]
fixed_odds = fixed_odds.reset_index(drop=True)
fixed_odds['concat'] = fixed_odds['Date'].astype(str) + fixed_odds['Pitcher'].astype(str)
fixed_odds = fixed_odds.drop_duplicates(subset='concat')
fixed_odds.to_csv('testtesttest.csv')
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

# Assign Individual Game IDs
game_ids = []
fixed_odds = fixed_odds.reset_index(drop=True)
end_range = int(int(len(fixed_odds.index))/2)
print(end_range)
for i in range(1,end_range):
    label = "Game " + str(i)
    game_ids.append(label)
    game_ids.append(label)

game_ids = pd.Series(game_ids)
fixed_odds['game_id'] = game_ids


# Align Home and Away Teams in Single Matchup
home_fixed_odds = fixed_odds.loc[fixed_odds['VH'] == "H"]
home_fixed_odds = home_fixed_odds.reset_index(drop=True)
home_fixed_odds.to_csv('hfo.csv')

away_fixed_odds = fixed_odds.loc[fixed_odds['VH'] == "V"]
away_fixed_odds = away_fixed_odds.reset_index(drop=True)
away_fixed_odds.to_csv('afo.csv')

complete_fixed_odds = home_fixed_odds.merge(away_fixed_odds, on='game_id', how='left')
print(complete_fixed_odds)

# Clean Dataset, Remove columns
complete_fixed_odds = complete_fixed_odds.drop(['Rot_x', 'Date_y', 'Rot_y', 'VH_y'], axis=1)




complete_fixed_odds.to_csv('complete-fixed-odds-2018.csv')
