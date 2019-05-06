# Import Libraries
import datetime, time
import pandas as pd
import numpy as np

# Import Scraped Data
qualified_pitchers_df_2018 = pd.read_csv('   .csv')
team_batters_df_2018 = pd.read_csv('   .csv')
team_pitchers_basic_df_2018 = pd.read_csv('   .csv')
team_Spitchers_advanced_df_2018 = pd.read_csv('   .csv')
team_batters_vsL_advanced_df_2018 = pd.read_csv('   .csv')
team_batters_vsR_advanced_df_2018 = pd.read_csv('     .csv')
team_batters_vsAll_advanced_df_2018 = pd.read_csv('   .csv')

# BaseRuns Scored
team_batters_df_2018['TB'] = (1 * team_batters_df_2018['1B']) + (2 * team_batters_df_2018['2B']) + (3 * team_batters_df_2018['3B']) + (4 * team_batters_df_2018['HR'])
team_batters_df_2018['varA'] = team_batters_df_2018['H'] + team_batters_df_2018['BB'] + team_batters_df_2018['HBP'] - team_batters_df_2018['HR'] - .5 * team_batters_df_2018['IBB']
team_batters_df_2018['varB'] = (1.4 * team_batters_df_2018['TB'] - .6 * team_batters_df_2018['H'] - 3 * team_batters_df_2018['HR'] + .1 * (team_batters_df_2018['BB'] + team_batters_df_2018['HBP'] - team_batters_df_2018['IBB']) + .9 * (team_batters_df_2018['SB'] - team_batters_df_2018['CS'] - team_batters_df_2018['GDP'])) * 1.1
team_batters_df_2018['varC'] = team_batters_df_2018['AB'] - team_batters_df_2018['H'] + team_batters_df_2018['CS'] + team_batters_df_2018['GDP']
team_batters_df_2018['varD'] = team_batters_df_2018['HR']
team_batters_df_2018.drop_duplicates(inplace=True)
team_batters_df_2018['BsR_Sc_Season'] = ((team_batters_df_2018['varA'] * team_batters_df_2018['varB']) / (team_batters_df_2018['varB'] + team_batters_df_2018['varC'])) + team_batters_df_2018['varD']

# BaseRuns Allowed
team_pitchers_basic_df_2018['varA'] = team_pitchers_basic_df_2018['H'] + team_pitchers_basic_df_2018['BB'] - team_pitchers_basic_df_2018['HR']
team_pitchers_basic_df_2018['varB'] = (1.4 * (1.12 * team_pitchers_basic_df_2018['H'] + 4 * team_pitchers_basic_df_2018['HR']) - .6 * team_pitchers_basic_df_2018['H'] - 3 * team_pitchers_basic_df_2018['HR'] + .1 * team_pitchers_basic_df_2018['BB']) * 1.1
team_pitchers_basic_df_2018['varC'] = 3 * team_pitchers_basic_df_2018['IP']
team_pitchers_basic_df_2018['varD'] = team_pitchers_basic_df_2018['HR']
team_pitchers_basic_df_2018.drop_duplicates(inplace=True)
team_pitchers_basic_df_2018['BsR_Al_Season'] = ((team_pitchers_basic_df_2018['varA'] * team_pitchers_basic_df_2018['varB']) / (team_pitchers_basic_df_2018['varB'] + team_pitchers_basic_df_2018['varC'])) + team_pitchers_basic_df_2018['varD']
