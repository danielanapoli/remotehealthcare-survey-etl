def removeFlagged(df, flagged):
    df = df[df.ResponseId.isin(flagged['ResponseId']) == False] #store rows with ResponseIds that are not in the flagged list
    return(df)

def responseToNumbers(df):
# transform text responses to numbers
# NOTE: .replace() acts like a "Replace All" which modifies every instance in the .csv
#       don't use this .csv to conduct qualitative analysis because open text boxes will be affected 
    df=df.replace('I don\'t know', 0)
    #df=df.replace('Prefer not to answer', 0)

    df=df.replace('(?i)Very comfortable', 5, regex=True) #case insensitive
    df=df.replace('(?i)Extremely comfortable', 5, regex=True) #case insensitive
    df=df.replace('Somewhat comfortable', 4)
    df=df.replace('Neither comfortable nor uncomfortable', 3)
    df=df.replace('Somewhat uncomfortable', 2)
    df=df.replace('(?i)Very uncomfortable', 1, regex=True) #case insensitive
    df=df.replace('(?i)Extremely uncomfortable', 1, regex=True) #case insensitive

    df=df.replace('(?i)Very likely', 5, regex=True) #case insensitive
    df=df.replace('Somewhat likely', 4)
    df=df.replace('Neither likely nor unlikely', 3)
    df=df.replace('Somewhat unlikely', 2)
    df=df.replace('(?i)Very unlikely', 1, regex=True) #case insensitive
    df=df.replace('Extremely likely', 5)
    df=df.replace('Extremely unlikely', 1)

    df=df.replace('Strongly agree', 5)
    df=df.replace('Somewhat agree', 4)
    df=df.replace('Neither agree nor disagree', 3)
    df=df.replace('Somewhat disagree', 2)
    df=df.replace('Strongly disagree', 1)

    df=df.replace('Always', 4)
    df=df.replace('Most of the time', 3)
    df=df.replace('Sometimes', 2)
    df=df.replace('Never', 1)

    df=df.replace('Yes', 2)
    df=df.replace('No', 1)
    
    return(df)

def birthYeartoAge (df):
    for index, row in df.iterrows():
        df.at[index, 'Age']=2023 - row['Age']
    return(df)

def agetoBucket (df):
    for index, row in df.iterrows():
        if (df.at[index, 'Age'] >= 18) & (df.at[index, 'Age'] <= 34):
            df.at[index, 'AgeBucket'] = '18-34'
        elif (df.at[index, 'Age'] >= 35) & (df.at[index, 'Age'] <= 49):
            df.at[index, 'AgeBucket'] = '35-49'
        elif (df.at[index, 'Age'] >= 50) & (df.at[index, 'Age'] <= 64):
            df.at[index, 'AgeBucket'] = '50-64'
        elif (df.at[index, 'Age'] >= 65):
            df.at[index, 'AgeBucket'] = '65+'
    return(df)

def adultBucket (df):
    for index, row in df.iterrows():
        if (df.at[index, 'AgeBucket'] == '18-34') | (df.at[index, 'AgeBucket'] == '35-49'):
            df.at[index, 'AdultBucket'] = 'Younger50'
        else:
            df.at[index, 'AdultBucket'] = 'Older50'
    return(df)

def tidyRaceEthCol (df):
    #Indigenous North American (E.g., First Nations, Metis, Inuit, etc.)
    #Black
    #East Asian
    #South East Asian
    #Caribbean
    #Latin or South/Central American/Hispanic
    #Central or South African
    #Middle Eastern, North African, or West Asian
    #White
    #Prefer not to answer

    df['RaceEthn']=df['RaceEthn'].str.strip()
    df['RaceEthn']=df['RaceEthn'].str.title()

    df=df.replace('Caucasian', 'White')
    df=df.replace('Caucasion', 'White')
    df=df.replace('Canadian', 'White')
    df=df.replace('Canadian Origin', 'White')
    df=df.replace('White Man', 'White')
    df=df.replace('White European', 'White')
    df=df.replace('White/Caucasian', 'White')
    df=df.replace('European', 'White')
    df=df.replace('The White Race', 'White')
    df=df.replace('Wasp', 'White')
    return(df)

def tidyCols (df):
    #health experience questions
    df.rename(columns={'EXP2-1' : 'ExpChangeSinceCovid',
                        'EXP3_1' : 'BeforeCov_Inperson',
                        'EXP3_2' : 'BeforeCov_Telephone',
                        'EXP3_3' : 'BeforeCov_Video',
                        'EXP3_4' : 'BeforeCov_Email',
                        'EXP3_5' : 'BeforeCov_InstantMsg',
                        'EXP3_6' : 'BeforeCov_SMS',
                        'EXP4_1' : 'AfterCov_Inperson',
                        'EXP4_2' : 'AfterCov_Telephone',
                        'EXP4_3' : 'AfterCov_Video',
                        'EXP4_4' : 'AfterCov_Email',
                        'EXP4_5' : 'AfterCov_InstantMsg',
                        'EXP4_6' : 'AfterCov_SMS',
                        }, inplace=True)

    #scenario questions
    df.rename(columns={'S1': 'ScenarioExp', 'S2': 'TechUseLikelihood', 
                        'S3': 'VideoIDComfort', 'S4' : 'VideoIDConcerns', 'S6' : 'VideoIDShare',
                        'S7': 'VideoANONComfort', 'S8' : 'VideoANONConcerns', 'S10' : 'VideoANONShare',
                        'S11': 'AudioComfort', 'S12' : 'AudioConcerns', 'S14' : 'AudioShare',
                        'S15': 'WellnessComfort', 'S16' : 'WellnessConcerns', 'S18' : 'WellnessShare',
                        'S19': 'VitalsComfort', 'S20' : 'VitalsConcerns', 'S22' : 'VitalsShare',
                        }, inplace=True)

    #SA-6 + privacy questions
    df.rename(columns={'SP1' : 'SA61', 'SP2' : 'SA62', 'SP3' : 'SA63', 'SP4' : 'SA64', 'SP5' : 'SA65', 
                        'SP6' : 'SA66', 'SP7' : 'Priv1', 'SP8' : 'Priv2'
                        }, inplace=True)   
    
    
    #demographic questions
    df.rename(columns={'D1_1' : 'Age', 'D2' : 'Gender', 'D3' : 'RaceEthn', 'D4' : 'Province', 'D5' : 'Education',
                        'D6' : 'Language', 'D7' : 'TechUse', 'D8' : 'LiveWhere', 'D9' : 'LiveWith',
                        'D10' : 'CareTake', 'D11' : 'HealthcareImpact'
                        }, inplace=True)
    return(df)