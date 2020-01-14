from fpl_constants import DATASETS_PATH, PLAYER_FILENAME, TEAM_FILENAME, FIXTURE_FILENAME
import requests
import pandas as pd
from pandas.io.json import json_normalize


def make_http_get(url):
    print(url)
    return requests.get(url).json()


loop_condition = True
gw = 1
while loop_condition:
    loop_condition = False
    gw_res = make_http_get('https://fantasy.premierleague.com/api/event/{gw}/live/'.format(gw=gw))

    if 'elements' in gw_res.keys():
        if len(gw_res['elements']) > 0:
            loop_condition = True
            gw_data = json_normalize(gw_res['elements'])
            gw_cols = gw_data.columns.tolist()
            for i, col in enumerate(gw_cols):
                gw_cols[i] = col.replace('stats.', '')
            gw_data.columns = gw_cols
            gw_data.to_csv(DATASETS_PATH + '/gw{gw}.csv'.format(gw=gw), index=False)
            gw += 1


all_response = make_http_get('https://fantasy.premierleague.com/api/bootstrap-static/')
fixture_response = make_http_get('https://fantasy.premierleague.com/api/fixtures/')

player_data = json_normalize(all_response['elements'])
player_cols = player_data.columns.tolist()
player_cols = player_cols[14:15] + player_cols[12:13] + player_cols[21:22] + player_cols[28:29] + player_cols[:12] + \
              player_cols[13:14] + player_cols[15:21] + player_cols[22:28] + player_cols[29:]
player_data = player_data[player_cols]
player_data.to_csv(DATASETS_PATH + '/' + PLAYER_FILENAME, index=False)

team_data = json_normalize(all_response['teams'])
team_cols = team_data.columns.tolist()
team_cols = team_cols[3:4] + team_cols[5:6] + team_cols[9:10] + team_cols[:3] + team_cols[4:5] + team_cols[6:9] + \
            team_cols[10:]
team_data = team_data[team_cols]
team_data.to_csv(DATASETS_PATH + '/' + TEAM_FILENAME, index=False)

fixture_data = json_normalize(fixture_response)
fixture_data.to_csv(DATASETS_PATH + '/' + FIXTURE_FILENAME, index=False)




# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# print(gw1_response['elements'][0]['explain'])
# print(player_data.head())
# print(player_data[player_data['id'] == 262].head())
# print(gw1_data.head(20))