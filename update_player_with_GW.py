from fpl_constants import DATASETS_PATH, PLAYER_FILENAME, PLAYER_WITH_GW_FILENAME,
import pandas as pd
from os import path
import numpy as np

player_df = pd.read_csv('./{datasets_path}/{player_filename}'
                        .format(datasets_path=DATASETS_PATH, player_filename=PLAYER_FILENAME))
points_df = pd.DataFrame(columns=['id'])
minutes_df = pd.DataFrame(columns=['id'])

## CREATE EMPTY LISTS FOR THE POINTS AND MINUTES PLAYED FOR EACH PLAYER. EACH LIST SHOULD HAVE 38 ITEMS, ONE FOR EACH
## GAMEWEEK
def update_points_and_minutes(player_row, gwdf, gameweek, pdf, mdf):
    pts_val = 0
    mins_val = 0
    player_id = player_row['id']
    result_df = gwdf.loc[gwdf['id'] == player_row['id'], ['id', 'minutes', 'total_points']]

    ## Check to make sure only one entry in that gameweek's data for that player
    if len(result_df) > 1:
        print(result_df.head())
        raise Exception('Multiple entries for one player in gameweek {gw} dataset'.format(gw=gw))
    elif len(result_df) == 1:
        gw_row = result_df.iloc[0]
        pts_val = float(gw_row['total_points'])
        mins_val = float(gw_row['minutes'])

    pp_rows = pdf[pdf['id'] == player_id]
    if len(pp_rows) == 0:
        pass
    elif len(pp_rows) == 1:
        # set new gw's points value in the same row using iloc
    pdf_row = [player_id, pts_val]
    mdf_row = [play]
    pdf.append(pd.DataFrame([player_id, ])) = pts_val
    mdf[gameweek] = mins_val


## LOOP THROUGH THE GAMEWEEK DATA FILES AND ADD THE POINTS AND MINUTES FOR EACH PLAYER FOR THE CORRESPONDING GAMEWEEK
loop_condition = True
gw = 1
while loop_condition:
    loop_condition = False
    gw_filepath = './{datasets_path}/gw{gw}.csv'.format(datasets_path=DATASETS_PATH, gw=gw)
    if path.exists(gw_filepath):
        loop_condition = True
        gw_data = pd.read_csv(gw_filepath)
        player_df.apply(lambda x: update_points_and_minutes(x, gw_data, gw, points_df, minutes_df), axis=1)
        print('Done GameWeek {gw}'.format(gw=gw))
        gw += 1

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
player_df.to_csv(DATASETS_PATH + '/' + PLAYER_WITH_GW_FILENAME, index=False)
