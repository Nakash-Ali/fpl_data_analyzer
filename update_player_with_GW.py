from fpl_constants import DATASETS_PATH, PLAYER_FILENAME, PLAYER_WITH_GW_FILENAME
import pandas as pd
from os import path
import numpy as np

large_player_df = pd.read_csv('./{datasets_path}/{player_filename}'
                        .format(datasets_path=DATASETS_PATH, player_filename=PLAYER_FILENAME))
player_df = large_player_df[['id','first_name','second_name', 'team', 'team_code', 'total_points',
                             'minutes', 'now_cost', 'selected_by_percent']]

## CREATE EMPTY LISTS FOR THE POINTS AND MINUTES PLAYED FOR EACH PLAYER. EACH LIST SHOULD HAVE 38 ITEMS, ONE FOR EACH
## GAMEWEEK
def update_points_list(player_row, gwdf, gameweek):
    pts_val = 0
    mins_val = 0
    result_df = gwdf.loc[gwdf['id'] == player_row['id'], ['id', 'minutes', 'total_points']]
    if len(result_df) > 1:
        print(result_df.head())
        raise Exception('Multiple entries for one player in gameweek {gw} dataset'.format(gw=gw))
    elif len(result_df) == 1:
        gw_row = result_df.iloc[0]
        pts_val = float(gw_row['total_points'])
        mins_val = float(gw_row['minutes'])

    if gameweek == 1:
        player_row['points_list'] = [pts_val]
        player_row['minutes_list'] = [mins_val]
    elif gameweek > 1:
        pts_list = player_row['points_list']
        pts_list.append(pts_val)
        player_row['points_list'] = pts_list
        mins_list = player_row['minutes_list']
        mins_list.append(mins_val)
        player_row['minutes_list'] = mins_list

    return player_row


## LOOP THROUGH THE GAMEWEEK DATA FILES AND ADD THE POINTS AND MINUTES FOR EACH PLAYER FOR THE CORRESPONDING GAMEWEEK
loop_condition = True
gw = 1
while loop_condition:
    loop_condition = False
    gw_filepath = './{datasets_path}/gw{gw}.csv'.format(datasets_path=DATASETS_PATH, gw=gw)
    if path.exists(gw_filepath):
        loop_condition = True
        gw_data = pd.read_csv(gw_filepath)
        player_df = player_df.apply(lambda x: update_points_list(x, gw_data, gw), axis=1)
        print('Done GameWeek {gw}'.format(gw=gw))
        gw += 1

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
player_df.to_csv(DATASETS_PATH + '/' + PLAYER_WITH_GW_FILENAME, index=False)
