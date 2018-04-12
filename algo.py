# MLB Future Earnings Model using PyBaseball

from pybaseball import pitching_stats_range
from pybaseball import batting_stats_range
import pandas as pd
import csv
import numpy as np


"""
Pitching Stats
"""
# Import Dataset, Add Variables
all_pitching = pd.DataFrame(pitching_stats_range('2014-04-01', '2014-11-01'))

# FIP Calculation, Append to Pitcher Datasets
fip_constant = 3.158 #to be replaced with dynamic calculation
fip = pd.DataFrame(((13 * all_pitching['HR']) + (3 * (all_pitching['BB'] + all_pitching['HBP']))
        - (2 * all_pitching['SO'])) / all_pitching['IP'] + 3.158)
all_pitching['FIP'] = fip

# Total Bases Calculation, Add Variables
tb_allowed = pd.DataFrame((all_pitching['H']-all_pitching['HR']-all_pitching['2B']
    - all_pitching['3B']) + (all_pitching['HR'] * 4) + (all_pitching['2B'] * 2) + (all_pitching['3B'] * 3))
all_pitching['TB'] = tb_allowed

# Splits into AL / NL
AL_pitching = all_pitching.loc[all_pitching['Lev'] == 'MLB-AL']
NL_pitching = all_pitching.loc[all_pitching['Lev'] == 'MLB-NL']

# Team Name Inputs
AL_teams = ['Baltimore', 'Boston', 'Chicago', 'Detroit', 'Houston', 'Kansas City',
                'Los Angeles', 'Minnesota', 'New York', 'Oakland', 'Seattle',
                'Tampa Bay', 'Texas', 'Toronto', 'Cleveland']
NL_teams = ['Arizona', 'Atlanta', 'Chicago', 'Cincinnati', 'Colorado', 'Los Angeles',
                'Miami', 'Milwaukee', 'New York', 'Philadelphia', 'Pittsburgh', 'San Diego',
                'San Francisco', 'St. Louis', 'Washington']

# Create Team Pitching Tables
AL_pitch = {}
for x in AL_teams:
    x_class = AL_pitching['Tm'] == x
    x_pitch = pd.DataFrame(AL_pitching[x_class])
    AL_pitch[x] = pd.DataFrame(x_pitch)
NL_pitch = {}
for x in NL_teams:
    x_class = NL_pitching['Tm'] == x
    x_pitch = pd.DataFrame(NL_pitching[x_class])
    NL_pitch[x] = pd.DataFrame(x_pitch)

# Calculate Overall Team FIP Average, Store in List, add in Team Names
AL_team_fip_avg = []
for x in AL_teams:
    total_ip = (AL_pitch[x]['IP'].sum())
    total_fip = ((AL_pitch[x]['FIP'] * AL_pitch[x]['IP']).sum())
    fip_avg = total_fip / total_ip
    AL_team_fip_avg.append(fip_avg)
NL_team_fip_avg = []
for x in NL_teams:
    total_ip = (NL_pitch[x]['IP'].sum())
    total_fip = ((NL_pitch[x]['FIP'] * NL_pitch[x]['IP']).sum())
    fip_avg = total_fip / total_ip
    NL_team_fip_avg.append(fip_avg)

AL_team_avgs = pd.DataFrame(
    {'FIP': AL_team_fip_avg,
    'Tm': AL_teams
    })
NL_team_avgs = pd.DataFrame(
    {'FIP': NL_team_fip_avg,
    'Tm': NL_teams
    })

# Calculate BaseRuns Allowed, Apply Specific League Adjustment, Add to Teams
AL_team_br_allowed = []
for x in AL_teams:
    A = AL_pitch[x]['H'] + AL_pitch[x]['BB'] + AL_pitch[x]['HBP'] - (AL_pitch[x]['IBB']*0.5)
    - AL_pitch[x]['HR']
    B = 1.1 * (1.4 * AL_pitch[x]['TB'] - 0.6 * AL_pitch[x]['H'] - 3 * AL_pitch[x]['HR']
    + 0.1 * (AL_pitch[x]['BB'] + AL_pitch[x]['HBP'] - AL_pitch[x]['IBB'])
    + 0.9 * (AL_pitch[x]['SB'] - AL_pitch[x]['CS'] - AL_pitch[x]['GDP']))
    C = AL_pitch[x]['BF'] - AL_pitch[x]['BB'] - AL_pitch[x]['SF'] - AL_pitch[x]['HBP']
    - AL_pitch[x]['H'] + AL_pitch[x]['CS'] + AL_pitch[x]['GDP']
    D = (AL_pitch[x]['HR'])
    games = AL_pitch[x]['G']
    base_runs_allowed = (((A*B) / (B+C)) + D).sum()
    AL_team_br_allowed.append(base_runs_allowed)
NL_team_br_allowed = []
for x in NL_teams:
    A = NL_pitch[x]['H'] + NL_pitch[x]['BB'] + NL_pitch[x]['HBP'] - (NL_pitch[x]['IBB']*0.5)
    - NL_pitch[x]['HR']
    B = 1.1 * (1.4 * NL_pitch[x]['TB'] - 0.6 * NL_pitch[x]['H'] - 3 * NL_pitch[x]['HR']
    + 0.1 * (NL_pitch[x]['BB'] + NL_pitch[x]['HBP'] - NL_pitch[x]['IBB'])
    + 0.9 * (NL_pitch[x]['SB'] - NL_pitch[x]['CS'] - NL_pitch[x]['GDP']))
    C = NL_pitch[x]['BF'] - NL_pitch[x]['BB'] - NL_pitch[x]['SF'] - NL_pitch[x]['HBP']
    - NL_pitch[x]['H'] + NL_pitch[x]['CS'] + NL_pitch[x]['GDP']
    D = (NL_pitch[x]['HR'])
    base_runs_allowed = (((A*B) / (B+C)) + D).sum()
    NL_team_br_allowed.append(base_runs_allowed)

AL_lg_adj = (AL_pitching['R'].sum()) / (sum(AL_team_br_allowed))
AL_team_br_allowed = [x * AL_lg_adj for x in AL_team_br_allowed]
AL_team_avgs['br_allowed'] = AL_team_br_allowed

NL_lg_adj = (NL_pitching['R'].sum()) / (sum(NL_team_br_allowed))
NL_team_br_allowed = [x * NL_lg_adj for x in NL_team_br_allowed]
NL_team_avgs['br_allowed'] = NL_team_br_allowed


"""
Actual Batting Stats
"""
# Import Dataset, Add Variables
actual_batting = pd.DataFrame(batting_stats_range('2018-03-01', '2018-11-01'))

# Total Bases Calculation, Add Variables
tb_scored = pd.DataFrame((actual_batting['H']-actual_batting['HR']-actual_batting['2B']
    - actual_batting['3B']) + (actual_batting['HR'] * 4) + (actual_batting['2B'] * 2) + (actual_batting['3B'] * 3))
actual_batting['TB'] = tb_scored

# Splits into AL / NL
AL_batting = actual_batting.loc[actual_batting['Lev'] == 'MLB-AL']
NL_batting = actual_batting.loc[actual_batting['Lev'] == 'MLB-NL']

# Create Team Batting Tables
AL_actual_batting = {}
for x in AL_teams:
    x_class = AL_batting['Tm'] == x
    x_batting = pd.DataFrame(AL_batting[x_class])
    AL_actual_batting[x] = pd.DataFrame(x_batting)
NL_actual_batting = {}
for x in NL_teams:
    x_class = NL_batting['Tm'] == x
    x_batting = pd.DataFrame(NL_batting[x_class])
    NL_actual_batting[x] = pd.DataFrame(x_batting)

"""
Projected Batting Stats
"""
# Import Steamer Batting Projections
projected_batting = pd.read_csv('steamer_batters.csv')
projected_batting = pd.DataFrame(projected_batting)
print(projected_batting['proj_Team'])

# Add Total Bases to Dataframe
tb_scored_proj = pd.DataFrame((projected_batting['proj_H']-projected_batting['proj_HR']-projected_batting['proj_2B']
    - projected_batting['proj_3B']) + (projected_batting['proj_HR'] * 4) + (projected_batting['proj_2B'] * 2) + (projected_batting['proj_3B'] * 3))
projected_batting['proj_TB'] = tb_scored_proj

# Team Name Inputs
AL_teams_names = ['Orioles', 'Red Sox', 'White Sox', 'Tigers', 'Astros', 'Royals',
                'Angels', 'Twins', 'Yankees', 'Athletics', 'Mariners',
                'Rays', 'Rangers', 'Blue Jays', 'Indians']
NL_teams_names = ['Diamondbacks', 'Braves', 'Cubs', 'Reds', 'Rockies', 'Dodgers',
                'Marlins', 'Brewers', 'Mets', 'Phillies', 'Pirates', 'Padres',
                'Giants', 'Cardinals', 'Nationals']

# Create Projected Team Batting Tables
AL_projected_batting = {}
for y in AL_teams_names:
    y_class = projected_batting['proj_Team'] == y
    y_batting = pd.DataFrame(projected_batting[y_class])
    AL_projected_batting[y] = pd.DataFrame(y_batting)
NL_projected_batting = {}
for y in NL_teams_names:
    y_class = projected_batting['proj_Team'] == y
    y_batting = pd.DataFrame(projected_batting[y_class])
    NL_projected_batting[y] = pd.DataFrame(y_batting)
print(NL_projected_batting['Marlins'])
print(NL_actual_batting['Miami'])
# Rename Projected Team Names


# Calculate BaseRuns Scored, Apply Specific League Adjustment, Add to Teams
"""
AL_team_br_scored = []
for x in AL_teams:
    A = AL_bat[x]['H'] + AL_bat[x]['BB'] + AL_bat[x]['HBP'] - (AL_bat[x]['IBB']*0.5)
    - AL_bat[x]['HR']
    B = 1.1 * (1.4 * AL_bat[x]['TB'] - 0.6 * AL_bat[x]['H'] - 3 * AL_bat[x]['HR']
    + 0.1 * (AL_bat[x]['BB'] + AL_bat[x]['HBP'] - AL_bat[x]['IBB'])
    + 0.9 * (AL_bat[x]['SB'] - AL_bat[x]['CS'] - AL_bat[x]['GDP']))
    C = AL_bat[x]['PA'] - AL_bat[x]['BB'] - AL_bat[x]['SF'] - AL_bat[x]['HBP']
    - AL_bat[x]['H'] + AL_bat[x]['CS'] + AL_bat[x]['GDP']
    D = (AL_bat[x]['HR'])
    base_runs_scored = (((A*B) / (B+C)) + D).sum()
    AL_team_br_scored.append(base_runs_scored)
NL_team_br_scored = []
for x in NL_teams:
    A = NL_bat[x]['H'] + NL_bat[x]['BB'] + NL_bat[x]['HBP'] - (NL_bat[x]['IBB']*0.5)
    - NL_bat[x]['HR']
    B = 1.1 * (1.4 * NL_bat[x]['TB'] - 0.6 * NL_bat[x]['H'] - 3 * NL_bat[x]['HR']
    + 0.1 * (NL_bat[x]['BB'] + NL_bat[x]['HBP'] - NL_bat[x]['IBB'])
    + 0.9 * (NL_bat[x]['SB'] - NL_bat[x]['CS'] - NL_bat[x]['GDP']))
    C = NL_bat[x]['PA'] - NL_bat[x]['BB'] - NL_bat[x]['SF'] - NL_bat[x]['HBP']
    - NL_bat[x]['H'] + NL_bat[x]['CS'] + NL_bat[x]['GDP']
    D = (NL_bat[x]['HR'])
    base_runs_scored = (((A*B) / (B+C)) + D).sum()
    NL_team_br_scored.append(base_runs_scored)

AL_lg_adj = (AL_batting['R'].sum()) / (sum(AL_team_br_scored))
AL_team_br_scored = [x * AL_lg_adj for x in AL_team_br_scored]
AL_team_avgs['br_scored'] = AL_team_br_scored

NL_lg_adj = (NL_batting['R'].sum()) / (sum(NL_team_br_scored))
NL_team_br_scored = [x * NL_lg_adj for x in NL_team_br_scored]
NL_team_avgs['br_scored'] = NL_team_br_scored
"""
