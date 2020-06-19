from fpl_constants import DATASETS_PATH, TEAM_FILENAME, FIXTURE_FILENAME, TEAM_DIFFICULTY_FILENAME
import pandas as pd


def get_diff_next_n(n, team_id, fdf):
    next_h_games = fdf.loc[(fdf['team_h'] == team_id) & (fdf['started'] == False), ['event', 'team_h_difficulty']]
    next_a_games = fdf.loc[(fdf['team_a'] == team_id) & (fdf['started'] == False), ['event', 'team_a_difficulty']]
    next_h_games.columns = ['gw', 'difficulty']
    next_a_games.columns = ['gw', 'difficulty']
    next_games = pd.concat([next_h_games, next_a_games], axis=0)
    next_games.reset_index(drop=True, inplace=True)
    next_games.sort_values(by=['gw'], inplace=True)
    return next_games.head(n)['difficulty'].mean()


def update_team_fixtures(tdf, fdf):
    tdf['diff_next_5'] = tdf.apply(lambda x: get_diff_next_n(5, x['id'], fdf),axis=1)
    tdf['diff_next_10'] = tdf.apply(lambda x: get_diff_next_n(10, x['id'], fdf), axis=1)
    tdf.to_csv(DATASETS_PATH + '/' + TEAM_DIFFICULTY_FILENAME, index=False)


team_data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=TEAM_FILENAME))
fixture_data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=FIXTURE_FILENAME))
update_team_fixtures(team_data, fixture_data)