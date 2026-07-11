import pandas as pd
import os
from clean_methods import *
from flag import *
from scenarios import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def onlineDataCleanup(filepath):

    #create dataframe from file
    df = pd.read_csv(filepath)

    #remove flagged responses
    flagged_df = pd.read_csv(os.path.join(SCRIPT_DIR, 'flagList.csv'), sep=',')
    df = removeFlagged(df, flagged_df)

    #drop unfinished responses
    df.drop(df[df['Finished'] == 'False'].index, inplace=True)

    #add a new column to hold the scenario names
    df.insert(loc=0, column='Scenario', value='')

    #align all scenario data in the same columns
    n = 1
    while(n < 24): #the number columns with questions in each scenario block 
        for index, row in df.iterrows():
            if not (pd.isnull(df.loc[index, 'S'+str(n)])): #first scenario block (E.g., S1)
                row['Scenario'] = 'Chronic' #tag the scenario
                row['Scenario Number'] = 1
            elif not pd.isnull(df.loc[index, 'S'+str(n)+'.1']): #second scenario block (E.g., S1.1)
                row['S'+str(n)] = row['S'+str(n)+'.1'] #move value over to the left
                row['Scenario'] = 'Emergency'
                row['Scenario Number'] = 2
            elif not pd.isnull(df.loc[index, 'S'+str(n)+'.2']): #third scenario block (E.g., S1.2)
                row['S'+str(n)] = row['S'+str(n)+'.2']
                row['Scenario'] = 'Rehab'
                row['Scenario Number'] = 3
            elif not pd.isnull(df.loc[index, 'S'+str(n)+'.3']): #fourth scenario block (E.g., S1.3)
                row['S'+str(n)] = row['S'+str(n)+'.3']
                row['Scenario'] = 'Symptoms'
                row['Scenario Number'] = 4
        n = n+1

    #Remove now extra columns 
    df=df.drop(df.iloc[:, 61:130], axis = 1) #extra rows from the scenario blocks
    df=df.drop(df.iloc[:, 2:18], axis = 1) #unneeded metadata

    #Remove header rows
    df=df.drop([0, 1])

    #Add concern columns
    #df = detectConcern(df)

    #Text transformations 
    df=tidyCols(df)
    df=responseToNumbers(df)
    df['Age'] = df['Age'].astype(float)
    df=birthYeartoAge(df)
    df.insert(loc=51, column='AgeBucket', value='')
    df=agetoBucket(df)
    df.insert(loc=52, column='AdultBucket', value='')
    df=adultBucket(df)
    #df=tidyRaceEthCol(df)

    return df

def paperDataCleanup(filepath, scenario):

    #create dataframe from file
    df = pd.read_csv(filepath)

    #remove flagged responses
    flagged_df = pd.read_csv(os.path.join(SCRIPT_DIR, 'flagList.csv'), sep=',')
    df = removeFlagged(df, flagged_df)

    #drop unfinished responses
    df.drop(df[df['Finished'] == 'False'].index, inplace=True)

    #add a new column to hold the scenario names
    df.insert(loc=0, column='Scenario', value='')

    #align all scenario data in the same columns
    n = 1
    while(n < 24): #the number columns with questions in each scenario block 
        for index, row in df.iterrows():
            if not (pd.isnull(df.loc[index, 'S'+str(n)])): #first scenario block (E.g., S1)
                row['Scenario'] = scenario.name #tag the scenario
                row['Scenario Number'] = scenario.number

        n = n+1

    #Remove header rows
    df=df.drop([0, 1])

    #Add concern columns
    #df = detectConcern(df)

    #Text transformations 
    df=tidyCols(df)
    df=responseToNumbers(df)
    df['Age'] = df['Age'].astype(float)
    df=birthYeartoAge(df)
    df.insert(loc=51, column='AgeBucket', value='')
    df=agetoBucket(df)
    df.insert(loc=52, column='AdultBucket', value='')
    df=adultBucket(df)
    #df=tidyRaceEthCol(df)

    return df
