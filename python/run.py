import pandas as pd
import glob
import os
from clean import onlineDataCleanup, paperDataCleanup
from flag import *
from scenarios import *

# region CONSTANTS
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MASTER_DIR = os.path.join(PROJECT_ROOT, 'raw')
ONLINE_DATA = os.path.join(MASTER_DIR, 'online', '*.csv')
PAPER_DATA = os.path.join(MASTER_DIR, 'paper', '*.csv')
# endregion

# region HELPER METHODS

# [Params]
#   directory: directory path
# [Returns]
#   An array of string filepaths of files in the given directory
def getFileNames(directory):
    return glob.glob(directory)

# [Params]
#   dfs: a list of dataframes
# [Returns]
#   A single dataframe that is the result of combing the dataframes in the 'dfs' parameter
def combineDataFrames(dfs):
    # Combine dataframes and preserve the column order
    return pd.concat(dfs)[dfs[0].columns]

# [Params]
#   df: a dataframe that will be used to generate a .csv and .xlsx file
#   filename: the name to give the outputted file (do not provide the extension)
# [Returns]
#   Nothing.  A .csv file and a .xlsx file are generated.
def generateFiles(df, filename):
    csv_name = os.path.join(SCRIPT_DIR, filename + ".csv")
    xlsx_name = os.path.join(SCRIPT_DIR, filename + ".xlsx")

    df.to_csv(csv_name) 
    print("\n" + csv_name + " was created.")
    
    df.to_excel(xlsx_name) 
    print(xlsx_name + " was created.\n")

# [Params]
#   filename: the name of a file
# [Returns]
#   A string indicating the relevant scenario the file data pertains to
def getScenarioFromFileName(filename):
    if Chronic.name in filename: return Chronic
    elif Emergency.name in filename: return Emergency
    elif Rehab.name in filename: return Rehab
    elif Symptoms.name in filename: return Symptoms
    else: return Invalid_Scenario

# endregion 

# region SCRIPT

print('\n- - - Data cleaning in progress')

# Get the files for processing
online_data_filenames = getFileNames(ONLINE_DATA)
paper_data_filenames = getFileNames(PAPER_DATA)

print("\nNumber of files imported:")
print("\tOnline data: " + str(len(online_data_filenames)))
print("\tPaper data: " + str(len(paper_data_filenames)))

# Process imported files
data_dfs = []

print('\nProcessing online data...')
for filename in online_data_filenames:
    df = onlineDataCleanup(filename)
    data_dfs.append(df)

print('\nProcessing paper data...')
for filename in paper_data_filenames:
    scenario = getScenarioFromFileName(filename)
    df = paperDataCleanup(filename, scenario)
    data_dfs.append(df)

data_combined_df = combineDataFrames(data_dfs)
generateFiles(data_combined_df, "data_cleaned_raw")


# Assess Data Concerns



#endregion