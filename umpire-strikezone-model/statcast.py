from pybaseball import statcast
import pandas as pd

# Scraping Statcast Data With Python
called_pitches = statcast(start_dt='2016-03-15', end_dt='2016-05-02')
called_pitches = called_pitches[['game_date', 'description', 'stand', 'balls', 'strikes', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'inning', 'player_name', 'game_pk']]
called_pitches.to_csv('statcast-all-2016-april.csv')
called_pitches = ""

# Scraping Statcast Data With Python
called_pitches = statcast(start_dt='2016-05-02', end_dt='2016-06-01')
called_pitches = called_pitches[['game_date', 'description', 'stand', 'balls', 'strikes', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'inning', 'player_name', 'game_pk']]
called_pitches.to_csv('statcast-all-2016-may.csv')
called_pitches = ""

# Scraping Statcast Data With Python
called_pitches = statcast(start_dt='2016-06-02', end_dt='2016-07-01')
called_pitches = called_pitches[['game_date', 'description', 'stand', 'balls', 'strikes', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'inning', 'player_name', 'game_pk']]
called_pitches.to_csv('statcast-all-2016-june.csv')
called_pitches = ""

# Scraping Statcast Data With Python
called_pitches = statcast(start_dt='2016-07-02', end_dt='2016-08-01')
called_pitches = called_pitches[['game_date', 'description', 'stand', 'balls', 'strikes', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'inning', 'player_name', 'game_pk']]
called_pitches.to_csv('statcast-all-2016-july.csv')
called_pitches = ""

# Scraping Statcast Data With Python
called_pitches = statcast(start_dt='2016-08-02', end_dt='2016-09-01')
called_pitches = called_pitches[['game_date', 'description', 'stand', 'balls', 'strikes', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'inning', 'player_name', 'game_pk']]
called_pitches.to_csv('statcast-all-2016-august.csv')
called_pitches = ""

# Scraping Statcast Data With Python
called_pitches = statcast(start_dt='2016-09-02', end_dt='2016-10-10')
called_pitches = called_pitches[['game_date', 'description', 'stand', 'balls', 'strikes', 'plate_x', 'plate_z', 'sz_top', 'sz_bot', 'inning', 'player_name', 'game_pk']]
called_pitches.to_csv('statcast-all-2016-sept.csv')
called_pitches = ""
