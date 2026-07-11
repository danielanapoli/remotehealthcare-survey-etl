# EXAMPLE RESOURCE:
#https://medium.com/@jb.ranchana/easy-way-to-create-stacked-bar-graphs-from-dataframe-19cc97c86fe3

import numpy as np
import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

df = pd.read_csv(os.path.join(PROJECT_ROOT, 'python', 'qualitrics_cleaned_raw.csv'))

df.plot.bar(x='Scenario', stacked=True, title='The number of Students')
ax = df.plot.bar(x='Scenario', stacked=True, color=['tomato','lightseagreen'], figsize=(8,6))
ax.set_title('The Number of Students', fontsize=20)
ax.set_ylim(0,500)
ax.set_xticklabels(['A','B','C'], rotation=0)