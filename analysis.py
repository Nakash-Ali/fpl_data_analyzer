from fpl_constants import DATASETS_PATH, PLAYER_PROCESSED_FILENAME
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=PLAYER_PROCESSED_FILENAME))

## SHOW TOP 10
top_10 = data.nlargest(20, 'roi')
print(top_10.head(30))

# plt.figure(figsize=(20, 20))
# top_10_by_pts.plot.bar(x='full_name', y='roi_last_5', rot=0)
# plt.show()
