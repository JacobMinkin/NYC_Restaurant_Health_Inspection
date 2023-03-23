
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from sklearn.impute import KNNImputer
sns.set_style('darkgrid')

#Import Data
df = pd.read_csv('../data/Inspection.csv')

#Change Name of Column for easier searching
df.rename(columns = {'VIOLATION CODE':'CODE'}, inplace = True)
df.rename(columns = {'Community Board':'CBoard'}, inplace = True)
# Convert date into pandas date/time format
df['date'] = pd.to_datetime(df['INSPECTION DATE'])
to_convert = ['ZIPCODE', 'CBoard']
df[to_convert] = df[to_convert].astype('category')

# Create Dictionaries for Violation Codes and Resteraunt Names
code_list = df.CODE[df.CODE.isna() == False].unique()
violation_dicts = {}
for name in code_list:
    violation_dicts[name] = df.VIOLATION[df.CODE == name].unique()

Name_list = df.CAMIS.unique()
Name_dicts = {}
latest_inspection_dicts = {}

for name in Name_list:
    Name_dicts[name] = df.DBA[df.CAMIS == name].unique()
    latest_inspection_dicts[name] = df[df.CAMIS == name].date.max()

#Imputing Time: I had to seperate the imputations for better results
impute_variables_1 = ['CAMIS', 'CBoard', 'Longitude', 'Latitude']
impute_variables_2 = ['CAMIS', 'ZIPCODE', 'Longitude', 'Latitude']

impute_df_1 = df[impute_variables_1].groupby('CAMIS').first()
impute_df_2 = df[impute_variables_2].groupby('CAMIS').first()

imputer1 = KNNImputer(n_neighbors=2, weights="uniform")
imputer2 = KNNImputer(n_neighbors=2, weights="uniform")
a_1=imputer1.fit_transform(impute_df_1)
a_2=imputer2.fit_transform(impute_df_2)

df_imputed_1 = pd.DataFrame(a_1, columns= list(impute_df_1), index= impute_df_1.index)
df_imputed_2 = pd.DataFrame(a_2, columns= list(impute_df_2), index= impute_df_2.index)
Community_Board_Imputed = {}
ZIPCODE_Imputed = {}
for name in Name_list:
    Community_Board_Imputed[name] = df_imputed_1.CBoard[name]
    ZIPCODE_Imputed[name] = df_imputed_2.ZIPCODE[name]
df['CBoard'] = df.CAMIS.map(Community_Board_Imputed)
df['ZIPCODE'] = df.CAMIS.map(ZIPCODE_Imputed)

# Making new variables first is Latest inspection date and second is a dummy variable that keeps True if it is the latest inspection
df['Latest_Inspection'] = df.CAMIS.map(latest_inspection_dicts)
df['isLatest'] = pd.to_datetime(df['INSPECTION DATE']) == df.Latest_Inspection
df['Critical'] = np.where(df['CRITICAL FLAG'] == 'Critical', 1, 0)
df['LatestandCrit'] = (df.Critical==1)  & (df.isLatest ==True )
df['PreviousCrit'] = (df.Critical==1)  & (df.isLatest ==False )

pastCrit = {}
nowCrit = {}
for name in Name_list:
    pastCrit[name] = df.PreviousCrit[df.CAMIS == name].max()
    nowCrit[name] = df.LatestandCrit[df.CAMIS == name].max()

df['Past_Crit'] = df.CAMIS.map(pastCrit)
df['Now_Crit'] = df.CAMIS.map(nowCrit)

#Now its time to make the final data set 
final_df = df[df.isLatest == True].groupby('CAMIS').first()
finalVariables = ['Now_Crit','CUISINE', 'BORO', 'ZIPCODE', 'CBoard', 'Past_Crit']

final_df[to_convert] = final_df[to_convert].astype('category')
final_df = final_df.drop(final_df[final_df.date== '1900-01-01'].index)
final_df = final_df[finalVariables]

