from fpl_constants import DATASETS_PATH, PLAYER_PROCESSED_FILENAME, TEAM_DIFFICULTY_FILENAME
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=PLAYER_PROCESSED_FILENAME))
tdf = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=TEAM_DIFFICULTY_FILENAME))

data['points_per_min'] = data['total_points'] / data['minutes']
data['ppm_roi'] = data['points_per_min'] / data['now_cost']
data = pd.merge(data, tdf[['id', 'diff_next_5', 'diff_next_10']], how='left', left_on='team', right_on='id')

cols = data.columns.tolist()
cols = cols[:6] + cols[-2:] + cols[6:-2]
data = data[cols]

## SHOW TOP 10
top_scorers_only = data[data['total_points'] > 80]
top = top_scorers_only.nlargest(30, 'pts_last_5')
#top.sort_values(by=['diff_next_5'], inplace=True)
print(len(top))

top_vals = top[['pts_last_5', 'roi_last_5']]
x = top_vals.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
top_vals = pd.DataFrame(x_scaled)
top_vals.columns = ['pts_last_5', 'roi_last_5']
names = pd.DataFrame(top[['full_name']])

top_vals.reset_index(drop=True, inplace=True)
names.reset_index(drop=True, inplace=True)
df = pd.concat( [names, top_vals], axis=1)
df.set_index('full_name', inplace=True, drop=True)

print(top.head(50))

# #plt.figure(figsize=(20, 20))
# ax = df.plot.bar(rot=0)
# ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
# ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
# plt.tight_layout()
# plt.show()
