import pandas as pd
import docx
import os

#RESOURCE: https://rowannicholls.github.io/python/data/export_to_word.html#export

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def out(filename):
    return os.path.join(SCRIPT_DIR, filename)

df = pd.read_csv(out('qualtrics_cleaned_raw.csv'), sep=',')

## Q: General Healthcare Experience 
# all
alltext = df['EXP1']
alltext.to_csv(out('HealthcareText_all.csv'))

# by Adult Bucket
younger50 = df[df['AdultBucket'] == 'Younger50']
younger50Text = younger50['EXP1']
younger50Text.to_csv(out('HealthcareText_younger50.csv'))
older50 = df[df['AdultBucket'] == 'Older50']
older50Text = older50['EXP1']
older50Text.to_csv(out('HealthcareText_older50.csv'))

# by Age Bucket
age1834 = df[df['AgeBucket'] == '18-34']
age1834Text = age1834['EXP1']
age1834Text.to_csv(out('HealthcareText_1834.csv'))

age3549 = df[df['AgeBucket'] == '35-49']
age3549Text = age3549['EXP1']
age3549Text.to_csv(out('HealthcareText_3549.csv'))

age5064 = df[df['AgeBucket'] == '50-64']
age5064Text = age5064['EXP1']
age5064Text.to_csv(out('HealthcareText_5064.csv'))

age65 = df[df['AgeBucket'] == '65+']
age65Text = age65['EXP1']
age65Text.to_csv(out('HealthcareText_65Above.csv'))

## Q: Impacts on healthcare experiences
# all
alltext = df['D12']
alltext.to_csv(out('Impacts_all.csv'))

# by Adult Bucket
younger50 = df[df['AdultBucket'] == 'Younger50']
younger50Text = younger50['D12']
younger50Text.to_csv(out('Impacts_younger50.csv'))
older50 = df[df['AdultBucket'] == 'Older50']
older50Text = older50['D12']
older50Text.to_csv(out('Impacts_older50.csv'))

# by Age Bucket
age1834 = df[df['AgeBucket'] == '18-34']
age1834Text = age1834['D12']
age1834Text.to_csv(out('Impacts_1834.csv'))

age3549 = df[df['AgeBucket'] == '35-49']
age3549Text = age3549['D12']
age3549Text.to_csv(out('Impacts_3549.csv'))

age5064 = df[df['AgeBucket'] == '50-64']
age5064Text = age5064['D12']
age5064Text.to_csv(out('Impacts_5064.csv'))

age65 = df[df['AgeBucket'] == '65+']
age65Text = age65['D12']
age65Text.to_csv(out('Impacts_65Above.csv'))

# Q: Other concerns for all data types
age65 = df[df['AgeBucket'] == '65+']
age65Text = pd.concat([age65['S5'], 
                      age65['S9'],
                      age65['S13'],
                      age65['S17']
                      ])
age65Text.to_csv(out('Concerns_65Above.csv'))