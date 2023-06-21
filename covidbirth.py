'''
Ricardo Erazo, PhD 	2024
Seattle Children's Research Institute
Center for Integrative Brain Research

This script takes as input the output from the pre-processing algorithm.
Data must me pre-processed in order to be loaded from this script.

The purposes of this script are to
- implement a general method to quantify variables of interest from the CDC birth database.
- visualize seasonal and general trends in births in the US
- use births per month as a normalization parameter to visualize other variables.
- produce an output for subsequent mathematical modeling and rhythmic characterization.


In this file
Considerations:
- Script assumes that there's a child directory named covidbirth, and one named census_data
- Where all the data and preprocessing scripts are executed.
- Arrange code/directories accordingly.

Instructions:
- Execute preprocessing algorithm
- Execute covidbirth.py algorithm
- Execute math_births.py

'''

import ninja_functions
## libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os

import plotly.graph_objects as go
import plotly.express as px

# from causalimpact import CausalImpact
from datetime import datetime, timedelta

# from datetime import datetime
import time

os.makedirs('output_figures/',exist_ok=True)
os.makedirs('model_data/',exist_ok=True)

## graphics stuff
import matplotlib as mpl
mpl.rcParams['axes.linewidth']=0
font = {'weight':'normal','size':25}
plt.rc('font', **font)
plt.rcParams['agg.path.chunksize'] = 1000

#################################################################################### setting up directories
legend_font = {'size': 12, 'weight': 'normal'}

### nativity
source_dir = 'covidbirth/documentation/'
data_dir = 'covidbirth/csv_data/'

birth_metadata = pd.read_excel(source_dir+'CDC_database_codeNames.xlsx')
##
census_dir = 'census_data/'

### mortality
mortality_source_dir = 'mortality/documentation/'
mortality_data_dir = 'mortality/data/'

#### print infinite pandas dataframe data
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

### plotting crutch
colores = ['forestgreen','orangered','cyan','brown','magenta','violet']
## 

#################################################################################### loading data chunk
#### first count the total births per day and then per month.
#### variable to count birth incidences: DPLURAL
print('... loading pre-processed data, please wait (approx 10 minutes starting ', datetime.now().time(), ') ...')
tik = time.perf_counter()
tab = pd.read_csv(data_dir+'BigData_births2015to2021.csv', dtype=str)
tok = time.perf_counter()
DT= (tok-tik)/60
DT_= '%.2f' % DT
print('loaded preprocessed data, time: ',DT_,' minutes \n')


############## processing of "total births" and also total "labor events"
keyDates = pd.read_excel(source_dir+'covid_keydates.xlsx')


################################################################################## census data

mtd15 = pd.read_csv(census_dir+'ACSST1Y2015.S0101-Column-Metadata.csv', dtype=str)
pop15 = pd.read_csv(census_dir+'ACSST1Y2015.S0101-Data.csv', dtype=str)
pop16 = pd.read_csv(census_dir+'ACSST1Y2016.S0101-Data.csv', dtype=str)
pop17 = pd.read_csv(census_dir+'ACSST1Y2017.S0101-Data.csv', dtype=str)
pop18 = pd.read_csv(census_dir+'ACSST1Y2018.S0101-Data.csv', dtype=str)
pop19 = pd.read_csv(census_dir+'ACSST1Y2019.S0101-Data.csv', dtype=str)
pop20 = pd.read_csv(census_dir+'ACSST5Y2020.S0101-Data.csv', dtype=str)
pop21 = pd.read_csv(census_dir+'ACSST1Y2021.S0101-2023-06-12T202017.csv', dtype=str)



tota15, population_ratio15= ninja_functions.get_pop_percentages_F15(pop15)
tota16, population_ratio16= ninja_functions.get_pop_percentages_F15(pop16)
tota17, population_ratio17= ninja_functions.get_pop_percentages(pop17)
tota18, population_ratio18= ninja_functions.get_pop_percentages(pop18)
tota19, population_ratio19= ninja_functions.get_pop_percentages(pop19)
tota20, population_ratio20= ninja_functions.get_pop_percentages(pop20)
tota21, population_ratio21= ninja_functions.get_pop_percentages_F21(pop21)


################################################################################## birth data


var1 = 'DPLURAL'
### get clean data
borntab, label =  ninja_functions.get_clean_column(source_dir,tab,var1)
### organize it with some function
time_series, birthseries= ninja_functions.compute_births(var1,borntab, label)

############ births per month
norm_year = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
leap_year = np.array([31,29,31,30,31,30,31,31,30,31,30,31])

# days_in_month = 2015, 2016, 2017, 2018, 2019, 2020, 2021
days_in_month = np.concatenate((norm_year, norm_year, norm_year, norm_year, norm_year, leap_year, norm_year), axis=None)
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
###########################################################################################	MOTHER'S AGE

###########################################
## MAGER9 - Mother's Age recode 9 (years): 
# g[0] - under 15
# g[1]- 15 to 19
# g[2] - 20 to 24
# g[3] - 25 to 29
# g[4] - 30 to 34
# g[5] - 35 to 39
# g[6] - 40 to 44
# g[7] - 45 to 49
# g[8] - 50 to 54
###########################################

tik=time.perf_counter()
### get clean data
magetab, label =  ninja_functions.get_clean_column(source_dir,tab,'MAGER9')
# time_series, g1, g2, g3, g4, g5, g6, g7, g8, g9 = ninja_functions.collect_MAGE(magetab,'MAGER9')
time_series, g = ninja_functions.collect_variable(magetab,'MAGER9')


##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
######################################################################################################### PRENATAL VISITS
'''
Numer of Prenatal visits recode
1 - No visits
2 - 1 to 2
3 - 3 to 4
4 - 5 to 6
5 - 7 to 8
6 - 9 to 10
7 - 11 to 12
8 - 13 to 14
9 - 15 to 16
10 - 17 to 18
11 - 19 or more
12 - no data 
'''

### get clean data
# previstab, label =  ninja_functions.get_two_column(source_dir,tab,'PREVIS_REC','MEDUC')
previstab, labels, codes =  ninja_functions.get_two_column(source_dir,tab,'PREVIS_REC','MEDUC')

### 	the logic of the coding scheme for all variables are consistent
### 	the higher the number, the greater the number of prenatal visits
### 	and also a greater number represents further education

###### time-series analysis

# time_series, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11 = ninja_functions.collect_prenatal_visits(previstab,'PREVIS_REC')
# time_series, e1, e2, e3, e4, e5, e6, e7, e8, e9 = ninja_functions.collect_mothers_education(previstab,'MEDUC')

time_series, n= ninja_functions.collect_variable(previstab,'PREVIS_REC')
time_series, e= ninja_functions.collect_variable(previstab,'MEDUC')


'''
mother's education (from documentation):
1	8th grade or less
2	9th through 12th grade with no diploma
3	High school graduate or GED completed
4	Some college credit, but not a degree.
5	Associate degree (AA,AS)
6	Bachelor’s degree (BA, AB, BS)
7	Master’s degree (MA, MS, MEng, MEd, MSW, MBA)
8	Doctorate (PhD, EdD) or Professional Degree (MD, DDS, DVM, LLB, JD)
9	Unknown

'''

tik=time.perf_counter() 
var1 = 'RF_INFTR'
### get clean data
fttab, label =  ninja_functions.get_clean_column(source_dir,tab,var1)

time_series, yay_nay = ninja_functions.collect_YayNay_variable(fttab,var1)


############################################ save variables for subsequent analysis

np.save('model_data/time_series.npy', time_series, allow_pickle=True)
np.save('model_data/birthseries.npy', birthseries, allow_pickle=False)
np.save('model_data/days_series.npy', days_in_month, allow_pickle=False)
np.save('model_data/mage_series.npy', g, allow_pickle=False)
np.save('model_data/prenaseries.npy', n, allow_pickle=False)
np.save('model_data/educ_series.npy', e, allow_pickle=False)
np.save('model_data/fertiseries.npy', yay_nay, allow_pickle=False)


############################################ plot data

######### replicate blogpost graphs:
## 1 total births + births per day
f0=plt.figure(figsize=(20,20))
ax0=f0.add_subplot(211)
ax1=f0.add_subplot(212)

ax0.plot(time_series, birthseries)
ax1.plot(time_series, birthseries/days_in_month)

ax0.set_ylabel('total births')
ax1.set_ylabel('births per day')

p1=ax0.get_xticks()
p2=ax1.get_xticks()
ax0.set_xticks(np.arange(p1[0],p1[-1],12))
ax1.set_xticks(np.arange(p2[0],p2[-1],12))
f0.autofmt_xdate(rotation=45)

f0.savefig('output_figures/figure1.png')
plt.close('all')
##### 2 MAGER 9

f0=plt.figure(figsize=(20,20))
ax0=f0.add_subplot(111)

ax0.plot(time_series, g[0]/birthseries, label= 'under 15')
ax0.plot(time_series, g[1]/birthseries, label= '15 to 19')
ax0.plot(time_series, g[2]/birthseries, label= '20 to 24')
ax0.plot(time_series, g[3]/birthseries, label= '25 to 29')
ax0.plot(time_series, g[4]/birthseries, label= '30 to 34')
ax0.plot(time_series, g[5]/birthseries, label= '35 to 39')
ax0.plot(time_series, g[6]/birthseries, label= '30 to 44')
ax0.plot(time_series, g[7]/birthseries, label= '45 to 49')
ax0.plot(time_series, g[8]/birthseries, label= '50 to 54')

ax0.set_ylabel('Mother age normalized')

p1=ax0.get_xticks()
ax0.set_xticks(np.arange(p1[0],p1[-1],12))
# ax1.set_xticks(np.arange(p1[0],p1[-1],12))
f0.autofmt_xdate(rotation=45)
f0.legend()
f0.savefig('output_figures/figure2.png')
plt.close('all')



#### 3 mother 15 to 19
f0=plt.figure(figsize=(20,20))
ax0=f0.add_subplot(111)

ax1 = ax0.twinx()

ax0.plot(time_series, g[1]/birthseries, label='15 to 19')
g1_ = g[1]/birthseries

ax1.plot(time_series[12:83], (g1_[12:83]-g1_[0:71])/g1_[0:71],color='orangered',alpha=0.5, label='Y/y')

# YoY change = ((Current Year Value - Previous Year Value) / Previous Year Value) * 100

p1=ax0.get_xticks()
ax0.set_xticks(np.arange(p1[0],p1[-1],12))
ax1.set_xticks(np.arange(p1[0],p1[-1],12))
f0.autofmt_xdate(rotation=45)

# ax0.set_ylabel('proportion of mothers relative to monthly births')
# ax1.set_ylabel('proportion of mothers relative to monthly births')
ax0.set_title('Mothers age 15 to 19, Year/Year')
ax0.set_xlabel('dates')
f0.legend()
f0.savefig('output_figures/figure3.png')
plt.close('all')

############### figure 4 previs rec

f0=plt.figure(figsize=(20,20))
ax0=f0.add_subplot(111)

ax0.plot(time_series, n[0]/birthseries, label= 'No visits')
ax0.plot(time_series, n[1]/birthseries, label= '1-2')
ax0.plot(time_series, n[2]/birthseries, label= '3-4')
ax0.plot(time_series, n[3]/birthseries, label= '5-6')
ax0.plot(time_series, n[4]/birthseries, label= '7-8')
ax0.plot(time_series, n[5]/birthseries, label= '9-10')
ax0.plot(time_series, n[6]/birthseries, label= '11-12')
ax0.plot(time_series, n[7]/birthseries, label= '13-14')
ax0.plot(time_series, n[8]/birthseries, label= '15-16')
ax0.plot(time_series, n[9]/birthseries, label= '15-16')
ax0.plot(time_series, n[10]/birthseries, label= '17-18')
ax0.plot(time_series, n[11]/birthseries, label= '19+')

start_date = datetime(2015, 1, 1)
end_date = datetime(2023, 1, 10)
date_list = ninja_functions.make_time_list(start_date, end_date)

x_coord, x_label = ninja_functions.get_coordinates_keyDates(time_series,keyDates)
# Convert dates to datetime object
datetime_dates = np.array([datetime.strptime(date, '%Y-%m-%d') for date in x_coord])
# Add 42 weeks to each date
gestation = np.array([date + timedelta(weeks=42) for date in datetime_dates])
gestation = np.array([date.replace(day=1) for date in gestation])
# Convert new dates back to string format
ninemonthsaftercovid = np.array([date.strftime('%Y-%m-%d') for date in gestation])

# min 3
# max 6
print('dates: \n')
displace_1 = 3e-3
for x in range(0,len(x_coord)):
	ax0.plot([x_coord[x], x_coord[x]],[np.min(n[3]/birthseries)-x*displace_1, np.max(n[6]/birthseries)-x*displace_1],'--',label=x_label[x],linewidth=5, c=colores[x],alpha=0.4)
	ax0.plot([ninemonthsaftercovid[x],ninemonthsaftercovid[x]],[np.min(n[3]/birthseries)-x*displace_1, np.max(n[6]/birthseries)-x*displace_1],'--',linewidth=5, c=colores[x],alpha=0.4)
	ax0.plot([x_coord[x],ninemonthsaftercovid[x]],[np.max(n[6]/birthseries)-x*displace_1, np.max(n[6]/birthseries)-x*displace_1],'--',linewidth=5, c=colores[x],alpha=0.4)
	ax0.plot([x_coord[x],ninemonthsaftercovid[x]],[np.min(n[3]/birthseries)-x*displace_1, np.min(n[3]/birthseries)-x*displace_1],'--',linewidth=5, c=colores[x],alpha=0.4)


ax0.set_ylabel('Prenatal care normalized')

p1=ax0.get_xticks()
ax0.set_xticks(np.arange(p1[0],p1[-1],12))
# ax1.set_xticks(np.arange(p1[0],p1[-1],12))
f0.autofmt_xdate(rotation=45)
f0.legend(ncol=4)
f0.savefig('output_figures/figure4.png')
plt.close('all')



