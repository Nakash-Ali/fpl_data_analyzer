from fpl_constants import DATASETS_PATH, PLAYER_FILENAME, PLAYER_WITH_GW_FILENAME, TEAM_FILENAME
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

player_df = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=PLAYER_WITH_GW_FILENAME))
team_data = pd.read_csv('./{dsp}/{pfn}'.format(dsp=DATASETS_PATH, pfn=TEAM_FILENAME))

print(team_data.head())