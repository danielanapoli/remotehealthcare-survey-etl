import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

df = pd.read_csv(os.path.join(PROJECT_ROOT, 'raw', 'Remote Healthcare - Raffle data_April 25, 2023_12.20 - Copy.csv'))
flagged = pd.read_csv(os.path.join(SCRIPT_DIR, 'flagList.csv'))

df = df[df.IPAddress.isin(flagged['IPAddress']) == False] #keep rows with IPAddresses that are not in the flagged list

winners = df.sample(1) #select a number of random winners needed for 1 in 50 chance

print(winners)