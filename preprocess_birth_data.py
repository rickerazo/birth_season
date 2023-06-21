'''
Ricardo Erazo, PhD 	2024
Seattle Children's Research Institute
Center for Integrative Brain Research

This script takes as input the *csv file downloaded from the NBR website:
	
	https://www.nber.org/research/data/vital-statistics-natality-birth-data
	
	US Data files:
		Years 2015 through 2021

Considerations:
- Script assumes that there's a child directory named csv_data, where all the downloaded files are stored.
- Files sometimes are downloaded as *zip, in such case, it'll be necessary to unzip to access the file
- Arrange code/directories accordingly.


Instructions:
- Make new directory, named csv_data
- In the new directory, Download data from website and specific years above
- Unzip files if necessary
- run preprocess_birth_data.py
- run covidbirth.py
- run mathbirths.py



The logic behind preprocessing, and subsequent loading is to speed up computations:
1. The preprocessing algorithm takes 1 hour to run, and saves the output of its concatenation
as a large csv file.
2. Loading the output from the pre-processed file takes roughly 10 minutes. It's a significant speed-up
compared to running and loading the csv file of each year individually (10 minutes each, 70 minutes total)
3. Keeping several large dataframes loaded into RAM is inefficient and makes simple computations slow.

'''

## libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os

from causalimpact import CausalImpact

# from datetime import datetime
import time

os.makedirs('output_figures/',exist_ok=True)

## graphics stuff
import matplotlib as mpl
mpl.rcParams['axes.linewidth']=0
font = {'weight':'normal','size':25}
plt.rc('font', **font)
plt.rcParams['agg.path.chunksize'] = 1000
## 
data_dir = 'csv_data/'
tik = time.perf_counter()

####### DOCUMENTING APPROACH: FIRST LOAD A BUNCH OF DATA
########### 1. Import data
#######
tic = time.perf_counter()
b15 = pd.read_csv(data_dir+'natl2015.csv', low_memory=False, dtype=str)
toc = time.perf_counter()
DT= (toc-tic)/60
DT_= '%.2f' % DT
print('read b15, time: ',DT_,' minutes')

#######
tic = time.perf_counter()
b16 = pd.read_csv(data_dir+'natl2016.csv', low_memory=False, dtype=str)
toc = time.perf_counter()
DT= (toc-tic)/60
DT_= '%.2f' % DT
print('read b16, time: ',DT_,' minutes')

#######
tic = time.perf_counter()
b17 = pd.read_csv(data_dir+'natl2017.csv', low_memory=False, dtype=str)
toc = time.perf_counter()
DT= (toc-tic)/60
DT_= '%.2f' % DT
print('read b17, time: ',DT_,' minutes')

#######
tic = time.perf_counter()
b18 = pd.read_csv(data_dir+'nat2018us.csv', low_memory=False, dtype=str)
toc = time.perf_counter()
DT= (toc-tic)/60
DT_= '%.2f' % DT
print('read b18, time: ',DT_,' minutes')

#######
tic = time.perf_counter()
b19 = pd.read_csv(data_dir+'nat2019us.csv', low_memory=False, dtype=str)
toc = time.perf_counter()
DT= (toc-tic)/60
DT_= '%.2f' % DT
print('read b19, time: ',DT_,' minutes')

#######
tic = time.perf_counter()
b20 = pd.read_csv(data_dir+'nat2020us.csv', low_memory=False, dtype=str)
toc = time.perf_counter()
DT= (toc-tic)/60
DT_= '%.2f' % DT
print('read b20, time: ',DT_,' minutes')

#######
tic = time.perf_counter()
b21 = pd.read_csv(data_dir+'nat2021us.csv', low_memory=False, dtype=str)
toc = time.perf_counter()
DT= (toc-tic)/60
DT_= '%.2f' % DT
print('read b21, time: ',DT_,' minutes')
###
tok = time.perf_counter()

#check that the first data is working
print(b21.head())
print(type(b21))

## check time it took to load the data
loadTime= (tok-tik)/60
loadTime_= '%.2f' % loadTime
print('\n Total time it took to load data: ', str(loadTime_), ' minutes. \n')

################# NEXT: CLEAN OR HOMOGENIZE THE DATA FOR ANALYSIS.
################	THE KEY OF THE APPROACH HERE IS THAT WE FIND THE COMMON NAMES
#names are not all the same not all upper, so joining will remove some fields 
b21.columns = b21.columns.str.upper()
b20.columns = b20.columns.str.upper()
b19.columns = b19.columns.str.upper()
b18.columns = b18.columns.str.upper()
b17.columns = b17.columns.str.upper()
b16.columns = b16.columns.str.upper()
b15.columns = b15.columns.str.upper()

#need to combine all years but names in 2021 need to be removed and only select those that overlap in comomon with other years.
#some names like _down are not common across fields, if you want these you will need to manually rename before this
common_names = set(b21.columns)  # Initialize with the column names of b21

## 2. Isolate common names
# Find common names iteratively
common_names = common_names.intersection(b20.columns)
common_names = common_names.intersection(b15.columns)
common_names = common_names.intersection(b16.columns)
common_names = common_names.intersection(b17.columns)
common_names = common_names.intersection(b18.columns)
common_names = common_names.intersection(b19.columns)

# Convert the result back to a list
common_names = list(common_names)
print('common names',common_names,'\n')

print(b21[common_names].head())

#test that data can join
#lazy naming for easy typing
asd = pd.concat([b21[common_names].head(), b20[common_names].head(), 
				b19[common_names].head(), b18[common_names].head(), 
				b17[common_names].head(), b16[common_names].head(), 
				b15[common_names].head()], axis=0)


################# ANOTHER CORNERSTONE OF THE APPROACH: CONCATENATE RELEVANT DATA TO A SINGLE DATAFRAME
################ 	THEN, REMOVE LEFTOVER DATA, AND MOVE ON.
################	IF NECESSARY, HERE'S WHERE THINGS MIGHT HAVE TO CHANGE GIVEN DIFFERENT VARIABLES FOR STUDY

#make sure this will work before running, this takes time and creates a VERY large dataframe
asd = pd.concat([b21[common_names], b20[common_names], b19[common_names],
				b18[common_names], b17[common_names], b16[common_names],
				b15[common_names]], axis=0)


frequency_table = pd.crosstab(asd['DOB_YY'], asd['DOB_MM'], dropna=False)

print('\n Frequency table \n',frequency_table)
### free up memory
# del b21, b20, b19, b18, b17, b16, b15

#convert to date for ease of plotting

# Rename columns
asd.rename(columns={'Unnamed: 0': 'date', 'Unnamed: 1': 'var1', 'Unnamed: 2': 'freq'}, inplace=True)

# Convert 'DOB_YY' and 'DOB_MM' columns to strings
asd['DOB_YY'] = asd['DOB_YY'].astype(str)
asd['DOB_MM'] = asd['DOB_MM'].astype(str)

# Combine 'DOB_YY' and 'DOB_MM' columns and create 'Date' column
asd['date'] = pd.to_datetime(asd['DOB_YY'] + '-' + asd['DOB_MM'] + '-01', format='%Y-%m-%d')

# print Large DataFrame
print(asd)

## and save up pre-processed data
asd.to_csv(data_dir+'BigData_births2015to2021.csv')
frequency_table.to_csv(data_dir+'frequency_table_births2015to2021.csv')


# ############ next script in pipeline: process_covidBirth_data.py

# ## runs with no problems as of this line: 5/23/2023

# ### Need to clean the data. I only want to save meaningful data, so remove all NaN
# tab = asd.dropna(subset=['CIG3_R','date'])
# f1=plt.figure(figsize=(20,20))
# ax=f1.add_subplot(111)
# ax.scatter(tab.date,tab.CIG3_R)
# f1.savefig('output_figures/CIG3_R.png')

# ## need to figure out a way to easily find the meaning of these code names of database



## next steps:
# make a function that takes in a string input and returns a plot of that var as a function of time
# make a function that queries the code names of this database
# 