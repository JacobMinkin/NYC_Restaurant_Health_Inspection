
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
sns.set_style('darkgrid')

#Import Data
df = pd.read_csv('../data/Inspection.csv')

#Change Name of Column for easier searching
df.rename(columns = {'VIOLATION CODE':'CODE'}, inplace = True)

# Convert date into pandas date/time format
df['date'] = pd.to_datetime(df['INSPECTION DATE'])

# Create Dictionaries for Violation Codes and Resteraunt Names
code_list = df.CODE[df.CODE.isna() == False].unique()
violation_dicts = {}
for name in code_list:
    violation_dicts[name] = df.VIOLATION[df.CODE == name].unique()

Name_list = df.CAMIS[df.CAMIS.isna() == False].unique()
Name_dicts = {}
latest_inspection_dicts = {}

for name in Name_list:
    Name_dicts[name] = df.DBA[df.CAMIS == name].unique()
    latest_inspection_dicts[name] = df[df.CAMIS == name].date.max()

# Making new variables first is Latest inspection date and second is a dummy variable that keeps True if it is the latest inspection
df.Latest_Inspection = df.CAMIS.map(latest_inspection_dicts)
df['isLatest'] = pd.to_datetime(df['INSPECTION DATE']) == df.Latest_Inspection
df['LatestandCrit'] = df['isLatest'] ==True and df['isLatest']

#Choose variables for final analysis
finalVariables = ['CAMIS','CUISINE','STREET', 'ZIPCODE', 'Community Board', 'BBL', 'BORO', 'date', 'CRITICAL FLAG']
fdf = df[finalVariables]

# df = df.drop(['Zip Codes', 'City Council Districts', 'Police Precincts', 'Location Point', 'Community Districts', 
#    'Borough Boundaries',  'GRADE DATE', 'PHONE', 'INSPECTION DATE', 'DBA', 'VIOLATION', 'RECORD DATE'], axis = 1)

# List of CONVERSION to categorical functions. 
to_convert = ['ZIPCODE', 'Community Board']
fdf[to_convert] = fdf[to_convert].astype('category')