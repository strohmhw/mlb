# Import Libraries
import pandas as pd
from pygam import LogisticGAM
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import log_loss
import datetime as dt
from datetime import timedelta, date

# Load Called Pitches CSV File For Training
data = pd.read_csv('umpire-strikezone-model/statcast-all-2017-short.csv', low_memory=False)
game_totals_results = pd.read_csv('umpire-strikezone-model/MLB-Games-2017.csv')
games = pd.DataFrame(data)

# Clean Data and Create Called Pitches Dataset
types = ['ball', 'called_strike']
called_pitches = pd.DataFrame(data)
called_pitches = called_pitches[np.isfinite(called_pitches['plate_x'])]
called_pitches = called_pitches.loc[called_pitches['description'].isin(types)]
called_pitches['strikeCall'] = ""
# called_pitches['bsCount'] = str(called_pitches['balls']) + str(called_pitches['strikes'])

called_pitches.loc[called_pitches['description'] == 'called_strike', 'strikeCall'] = 1
called_pitches.loc[called_pitches['description'] == 'ball', 'strikeCall'] = 0
called_pitches.loc[called_pitches['stand'] == 'R', 'stand'] = 1
called_pitches.loc[called_pitches['stand'] == 'L', 'stand'] = 0

# Estimate Daily Lagged 90-Day Moving Strike Zone Models
called_pitches['game_date'] = pd.to_datetime(called_pitches['game_date'])
called_pitches['pred_zone_last90'] = ""
dates = called_pitches['game_date'].unique()
dates = pd.to_datetime(dates)
dates.sort_values('game_date')
called_pitches.sort_values('game_date')

for i in dates:
    # Fit Model to 90 Days of Data Lagged
    mask = (called_pitches['game_date'] <= i) & (called_pitches['game_date'] >= (i - dt.timedelta(days=90)))
    set = called_pitches.loc[mask]
    df = pd.DataFrame(set)
    target_df = pd.Series(set.strikeCall)
    X = df[['plate_x', 'plate_z', 'sz_top', 'sz_bot']]# 'bsCount'
    y = target_df
    gam_fit = LogisticGAM().fit(X, y)

    # Predict Each Day of Games Using 90 Day Model
    games = called_pitches.loc[called_pitches['game_date'] == i]
    x_games = games[['plate_x', 'plate_z', 'sz_top', 'sz_bot']]
    results = gam_fit.predict(x_games)
    called_pitches.at[called_pitches['game_date'] == i, 'pred_zone_last90'] = results

    # Track Progress and Reset Model
    print("Inserted..." + str(i))
    gam_fit = ""

called_pitches['zone_dev_last90'] = called_pitches['strikeCall'] - called_pitches['pred_zone_last90']

# Create Unique Umpire-Date ID, Average Zone Deviation for each Umpire-Game, # of Called_Pitches
called_pitches['umpire_date'] = called_pitches['umpire'] + called_pitches['game_date'].map(str)
umpDev90 = called_pitches[['game_date', 'umpire_date', 'umpire', 'game_pk']]
umpDev90 = pd.DataFrame(umpDev90)
umpDev90 = umpDev90.drop_duplicates('umpire_date')
umpDev90['last90_zonedev'] = ""
umpDev90['called_pitches_sum'] = ""
umpDev90.columns = ['game_date', 'umpire_date', 'umpire', 'game_pk', 'last90_zonedev', 'called_pitches_sum']

for x in umpDev90['umpire_date']:
    set = called_pitches.loc[called_pitches['umpire_date'] == x]
    umpDev90.at[umpDev90['umpire_date'] == x, 'last90_zonedev'] = set['zone_dev_last90'].mean()
    umpDev90.at[umpDev90['umpire_date'] == x, 'called_pitches_sum'] = set['strikeCall'].count()

umpDev90 = umpDev90.loc[umpDev90['last90_zonedev'] != 0]

# Load Game Results and Totals information, Merge with Umpire-Game Summaries, Re-order
full_dataset = pd.merge(umpDev90, game_totals_results, on='game_pk')
full_dataset.sort_values('umpire')
full_dataset.sort_values('game_date')
full_dataset.reset_index(drop=True)

# Calculate game level 90-day rolling sum of called Pitches
full_dataset['lagPitches_90d'] = ""
for row in full_dataset.itertuples(index=True, name='Pandas'):
    game_pk_set = getattr(row, "game_pk")
    umpire_set = getattr(row, "umpire")
    start_dt = getattr(row, "game_date")
    end_dt = getattr(row, "game_date") - dt.timedelta(days=90)
    mask = (full_dataset['game_date'] < start_dt) & (full_dataset['game_date'] >= end_dt) & (full_dataset['umpire'] == umpire_set)
    set = full_dataset.loc[mask]
    full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagPitches_90d'] = set['called_pitches_sum'].sum()
    set = ""
print("lagPitches_90d completed")

# Calculate game-level 90-day rolling average DEVIATION
full_dataset['lagDevAvg_90d'] = ""
for row in full_dataset.itertuples(index=True, name='Pandas'):
    game_pk_set = getattr(row, "game_pk")
    umpire_set = getattr(row, "umpire")
    start_dt = getattr(row, "game_date")
    end_dt = getattr(row, "game_date") - dt.timedelta(days=90)
    mask = (full_dataset['game_date'] < start_dt) & (full_dataset['game_date'] >= end_dt) & (full_dataset['umpire'] == umpire_set)
    set = full_dataset.loc[mask]
    setWeighted = set['called_pitches_sum'] * set['last90_zonedev']
    if set['called_pitches_sum'].sum() > 0:
        result = setWeighted.sum() / set['called_pitches_sum'].sum()
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevAvg_90d'] = result
    else:
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevAvg_90d'] = ""
    print("Inserted..." + umpire_set)
    set = ""
print("lagDevAvg_90d completed")

# Calculate game-level 90-day rolling average deviation SD
full_dataset['lagDevSD_90d'] = ""
for row in full_dataset.itertuples(index=True, name='Pandas'):
    game_pk_set = getattr(row, "game_pk")
    umpire_set = getattr(row, "umpire")
    start_dt = getattr(row, "game_date")
    end_dt = getattr(row, "game_date") - dt.timedelta(days=90)
    mask = (full_dataset['game_date'] < start_dt) & (full_dataset['game_date'] >= end_dt) & (full_dataset['umpire'] == umpire_set)
    set = full_dataset.loc[mask]
    setWts = set['called_pitches_sum'] * set['last90_zonedev']
    if set['called_pitches_sum'].sum() > 0:
        setMean = setWts.sum() / set['called_pitches_sum'].sum()
        setWts2 = (set['last90_zonedev']-setMean)**2
        setWts3 = (set['called_pitches_sum']/(set['called_pitches_sum'].sum()))
        setWts4 = setWts2 * setWts3
        result = np.sqrt(setWts4.sum())
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevSD_90d'] = result
    else:
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevSD_90d'] = ""
    print("Inserted..." + umpire_set)
    set = ""

# Calculate average actual runs totals by umps over last 90 days
full_dataset['lagActualRuns_90d'] = ""
for row in full_dataset.itertuples(index=True, name='Pandas'):
    game_pk_set = getattr(row, "game_pk")
    umpire_set = getattr(row, "umpire")
    start_dt = getattr(row, "game_date")
    end_dt = getattr(row, "game_date") - dt.timedelta(days=90)
    mask = (full_dataset['game_date'] < start_dt) & (full_dataset['game_date'] >= end_dt) & (full_dataset['umpire'] == umpire_set)
    set = full_dataset.loc[mask]
    if set['called_pitches_sum'].sum() > 0:
        result = set['Total'].mean()
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagActualRuns_90d'] = result
    else:
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagActualRuns_90d'] = ""
    print("Inserted..." + umpire_set)
    set = ""

# Calculate deviation from opening totals line by umps over last 90 days
full_dataset['DevLineOpen'] = full_dataset['Total'] - full_dataset['Open OU']
full_dataset['lagDevLineOpen_90d'] = ""
for row in full_dataset.itertuples(index=True, name='Pandas'):
    game_pk_set = getattr(row, "game_pk")
    umpire_set = getattr(row, "umpire")
    start_dt = getattr(row, "game_date")
    end_dt = getattr(row, "game_date") - dt.timedelta(days=90)
    mask = (full_dataset['game_date'] < start_dt) & (full_dataset['game_date'] >= end_dt) & (full_dataset['umpire'] == umpire_set)
    set = full_dataset.loc[mask]
    if set['called_pitches_sum'].sum() > 0:
        result = set['DevLineOpen'].mean()
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevLineOpen_90d'] = result
    else:
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevLineOpen_90d'] = ""
    print("Inserted..." + umpire_set)
    set = ""

# Calculate deviation from closing totals line by umps over last 90 days
full_dataset['DevLineClose'] = full_dataset['Total'] - full_dataset['Close OU']
full_dataset['lagDevLineClose_90d'] = ""
for row in full_dataset.itertuples(index=True, name='Pandas'):
    game_pk_set = getattr(row, "game_pk")
    umpire_set = getattr(row, "umpire")
    start_dt = getattr(row, "game_date")
    end_dt = getattr(row, "game_date") - dt.timedelta(days=90)
    mask = (full_dataset['game_date'] < start_dt) & (full_dataset['game_date'] >= end_dt) & (full_dataset['umpire'] == umpire_set)
    set = full_dataset.loc[mask]
    if set['called_pitches_sum'].sum() > 0:
        result = set['DevLineClose'].mean()
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevLineClose_90d'] = result
    else:
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagDevLineClose_90d'] = ""
    print("Inserted..." + umpire_set)
    set = ""

# Calculate the number of games umped over past 90 days
full_dataset['lagGamesUmped_90d'] = ""
for row in full_dataset.itertuples(index=True, name='Pandas'):
    game_pk_set = getattr(row, "game_pk")
    umpire_set = getattr(row, "umpire")
    start_dt = getattr(row, "game_date")
    end_dt = getattr(row, "game_date") - dt.timedelta(days=90)
    mask = (full_dataset['game_date'] < start_dt) & (full_dataset['game_date'] >= end_dt) & (full_dataset['umpire'] == umpire_set)
    set = full_dataset.loc[mask]
    if set['called_pitches_sum'].sum() > 0:
        result = set['umpire'].count()
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagGamesUmped_90d'] = result
    else:
        full_dataset.at[full_dataset['game_pk'] == game_pk_set, 'lagGamesUmped_90d'] = ""
    print("Inserted..." + umpire_set)
    set = ""

# Drop unnecessary variables

full_dataset.to_csv('output-2017.csv')
