from fpl_constants import DATASETS_PATH, PLAYER_WITH_GW_FILENAME, TEAM_FILENAME, PLAYER_PROCESSED_FILENAME, \
    FIXTURE_FILENAME
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

player_df = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=PLAYER_WITH_GW_FILENAME))
team_data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=TEAM_FILENAME))
fixture_data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=FIXTURE_FILENAME))

def read_csv_list(str):
    str = str.replace(' ', '').replace(']', '').replace('[', '')
    new_list = [float(i) for i in str.split(',')]
    return new_list


def get_pts_last_5(pts_list):
    if len(pts_list) < 5: raise Exception('Not enough history to get last 5 games')
    return sum(pts_list[-5:])


def get_var_last_5(pts_list):
    if len(pts_list) < 5: raise Exception('Not enough history to get last 5 games')
    return np.var(pts_list[-5:])


## ADD OTHER PLAYER METRICS SUCH AS ROI (RETURN ON INVESTMENT) AND POINTS IN LAST 5 GAMES ETC.
player_df['points_list'] = player_df['points_list'].apply(read_csv_list)
player_df['minutes_list'] = player_df['minutes_list'].apply(read_csv_list)
player_df['pts_last_5'] = player_df['points_list'].apply(get_pts_last_5)
player_df['roi'] = player_df['total_points'] / player_df['now_cost']
player_df['roi_last_5'] = player_df['pts_last_5'] / player_df['now_cost']
player_df['variance'] = player_df['points_list'].apply(np.var)
player_df['variance_last_5'] = player_df['points_list'].apply(get_var_last_5)
player_df['full_name'] = player_df['first_name'] + ' ' + player_df['second_name']

## ADD TEAM NAMES NEXT TO PLAYERS
team_data_small = team_data[['code', 'name']]
player_df = pd.merge(player_df, team_data_small, how='left', left_on='team_code', right_on='code')

## RE-ARRANGE COLUMNS TO MAKE IT LOOK NICER
cols = player_df.columns.tolist()
cols = cols[-3:-2] + cols[-1:] + cols[7:8] + cols[11:-3] + cols[3:7] + cols[8:11] + cols[:3] + cols[-2:-1]
player_df = player_df[cols]

player_df.columns = ['full_name', 'team_name', 'now_cost', 'pts_last_5', 'roi', 'roi_last_5', 'variance',
                     'variance_last_5', 'team', 'team_code', 'total_points', 'minutes', 'selected_by_percent',
                     'points_list', 'minutes_list', 'id', 'first_name', 'second_name', 'code']

player_df = player_df[['full_name', 'team_name', 'now_cost', 'pts_last_5', 'roi', 'roi_last_5', 'variance',
                       'variance_last_5', 'total_points', 'minutes', 'selected_by_percent', 'id', 'team']]
player_df.to_csv(DATASETS_PATH + '/' + PLAYER_PROCESSED_FILENAME, index=False)

# gw1_df = pd.read_csv('./{dsp}/gw1.csv'.format(dsp=DATASETS_PATH))
#
# joined_player = pd.merge(player_df, gw1_df, how='left', on=['id', 'id'])
# x = joined_player.loc[joined_player['id'] == 1, ['id', 'first_name', 'second_name']]
# print(x.head())