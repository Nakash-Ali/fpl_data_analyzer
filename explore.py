from fpl_constants import DATASETS_PATH, PLAYER_FILENAME, PLAYER_WITH_GW_FILENAME, TEAM_FILENAME, FIXTURE_FILENAME
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

player_df = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=PLAYER_WITH_GW_FILENAME))
team_data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=TEAM_FILENAME))
fdf = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=FIXTURE_FILENAME))


next_h_games = fdf.loc[(fdf['team_h'] == 10) & (fdf['started'] == False), ['event', 'team_h_difficulty']]
next_a_games = fdf.loc[(fdf['team_a'] == 10) & (fdf['started'] == False), ['event', 'team_a_difficulty']]
next_h_games.columns = ['gw', 'difficulty']
next_a_games.columns = ['gw', 'difficulty']
next_games = pd.concat([next_h_games, next_a_games], axis=0)
next_games.reset_index(drop=True, inplace=True)
next_games.sort_values(by=['gw'], inplace=True)
print(next_games.head(5))