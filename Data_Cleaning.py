# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

#Import Data
df = pd.read_csv('../data/Inspection.csv')

#Change Name of Column for easier searching
df.rename(columns = {'VIOLATION CODE':'CODE'}, inplace = True)

# Convert date into pandas date/time format
df['date'] = pd.to_datetime(df['INSPECTION DATE'])

#Drop Columns: most of these are empty cols to beging with
df = df.drop(['Zip Codes', 'City Council Districts', 'Police Precincts', 'Location Point', 'Community Districts', 
   'Borough Boundaries',  'GRADE DATE', 'PHONE', 'INSPECTION DATE'], axis = 1)

to_convert = []
df[to_convert].astype('category')