import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

df = pd.read_csv(os.path.join(PROJECT_ROOT, 'raw', 'online', 'Remote Healthcare - Survey (Other Online 2)_March 28, 2023_07.24.csv'))

print('- - - - Data flagging in progress')
flagList = pd.DataFrame

# Pre-processing cleaning
df.columns = df.columns.str.replace(' ','')
df.columns = df.columns.str.replace(')','')
df.columns = df.columns.str.replace('(','')
df = df.drop(labels=[0,1], axis=0) #remove two rows of extra Qualtrics stuff that are not survey responses
df['Durationinseconds'] = df['Durationinseconds'].astype('Int64')
df['D1_1'] = df['D1_1'].astype('Int64')

flagList = pd.concat([df[df['Durationinseconds'] < 240], #short duration
                      df[df.duplicated('RecordedDate')],
                      #df[df.duplicated('IPAddress')],
                      df[df['EXP1'] == 'Don\'t want to answer'],
                      df[df['EXP1'].str.len() < len('Prefer not to answer')],
                      df[df['D1_1'] > 1973]
                    ])

#Drop particular ResponseIDs from flagList
ResponseId_exceptions = {
    "R_2ANjq1dpNFAABzz",
    "R_3lLDvy3LBmHs9vb",
    "R_3CI3TA4cMBkDPXg",
    "R_1LXArEAsqaHQu7A",
    "R_2Xh5iKLX55PBO7l",
    "R_V511QeR9mB16EaR",
    "R_1jrCdarTjssDWBC",
    "R_2CTHrUsvRelBSoF",
    "R_3LaK6lWRhWumiqF",
    "R_1BPMR9cTgnVbiv5",
    "R_1eUW4nMxenEcayb",
    "R_3gSf9RySBWlcXKz",
    "R_1E4pGzPsuD1SLnU",
    "R_3lxDvQlPW6EkQdt",
    "R_87maJWRzslQE16F",
    "R_a5b4ZAQjDv7GPKh",
    "R_2RPbHBCkNPZe8p7",
    "R_zSTgG6JxDcb9aOl",
    "R_2TzaEV82oC8kHoI",
    "R_1CpzRz9wY0eyvrz",
    "R_24GYyM0Pv2rCd17",
    "R_PG9bwwzDDlkXnFL",
    "R_1EhdikCOzIcNo3B",
    "R_3Pog84InxwLr7MI",
    "R_blyFRbMQicHut1f",
    "R_a8LHiAbL99si9vb",
    "R_DDo0I2pkFQBt3Gx",
    "R_1LAURZ5QyaNobLS",
    "R_2xOXsF1x1hPgRoe"
}
flagList = flagList[flagList.ResponseId.isin(ResponseId_exceptions) == False] #only keep IDs not in exceptions

#Clean up any duplicates
flagList = flagList.drop_duplicates()

print('Number of survey responses: {}\n Number of flagged responses: {}\n Number of valid responses: {}'.format(len(df),len(flagList),(len(df)-len(flagList))))
flagList.to_csv(os.path.join(SCRIPT_DIR, 'flagList.csv'))


