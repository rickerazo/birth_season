'''
Ricardo Erazo, PhD 	2024
Seattle Children's Research Institute
Center for Integrative Brain Research

These functions support analysis of CDC, and Census data.
These are kept in a separate script because they are called from several other scripts,
and in order to maintain consistency between codes, the functions ought to the shared.


'''

# ninja_functions.py

############## 	BACKBONE LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os

from datetime import datetime, timedelta

import time

os.makedirs('output_figures/',exist_ok=True)

## graphics stuff
import matplotlib as mpl

############### CUSTOM FUNCTIONS: NINJA BECAUSE THEY APPEAR AND DISEPPEAR LEAVING NO TRACE
'''
these functions are used for processing and cleaning of timeseries data

'''

def get_coordinates_keyDates(time_series,keyDates):
	x_coord = np.array([])
	x_label = np.array([])
	for x in range(0, len(keyDates)):
		if keyDates['plot'][x]=='y':
			# print(x)
			for i in range(0,len(time_series)):
			# i=71
				xdate = time_series[i]
				ydate = keyDates['plot_date'][x].date()

				# print(xdate,ydate.strftime('%Y-%m-%d'))
				# print(xdate==ydate.strftime('%Y-%m-%d'))
				if xdate==ydate.strftime('%Y-%m-%d'):
					print(time_series[i],xdate,keyDates['event'][x])
					x_coord = np.append(x_coord, time_series[i])
					x_label = np.append(x_label, keyDates['event'][x])
	return x_coord, x_label

def get_clean_column(source_dir,bigData,var1):
	tab = bigData[['date', var1]].copy()
	tab = tab.dropna(subset=[var1,'date'])
	dict1 = pd.read_excel(source_dir+'CDC_database_codeNames.xlsx')
	cod_of_int = dict1.Code[dict1.Code==var1]
	var_of_int = dict1.Label[dict1.Code==var1]
	# print(var_of_int.values[0])

	return tab, var_of_int.values[0]

def get_two_column(source_dir,bigData,var1,var2):
	tab = bigData[['date', var1,var2]].copy()
	tab = tab.dropna(subset=[var1,var2,'date'])
	dict1 = pd.read_excel(source_dir+'CDC_database_codeNames.xlsx')
	cod_of_int = dict1.Code[dict1.Code==var1]
	var_of_int1 = dict1.Label[dict1.Code==var1]
	var_of_int2 = dict1.Label[dict1.Code==var1]
	# print(var_of_int.values[0])
	df = pd.DataFrame({var1:var_of_int1.values[0],var2:var_of_int2.values[0]})
	return tab, df

def make_time_list(start_date, end_date):
	# Define the start and end dates

	# Create an empty list to store the dates
	date_list = np.array([], dtype='datetime64')

	# Loop through the range of dates and append to the list
	current_date = start_date
	while current_date <= end_date:
		date_list = np.append(date_list, current_date.date())
		# current_date += timedelta(days=1)
		current_date += timedelta(weeks=10)
		# print(current_date.strftime("%Y-%m-%d"))

	date_list=np.append(date_list,end_date)
	return date_list


'''

birth functions
the goal is to have functions as generalizable as possible; right now I have three kinds, based on the information encoded in the database:
1. count a total based from a number input
2. count a total based from a number code
3. count a total based from a letter code
'''
##################################################################################
######## 1. integer numeric input 
def compute_births(var1,tab, label):

	print(tab.columns,'\n')
	# tab.to_csv('output_figures/tab.csv')

	###### loop parameters:
	time_series = tab['date'].unique()
	time_series = np.sort(time_series)

	birthseries = np.array([])
	##### information on current process
	tik = time.perf_counter()
	print('started loop for ', label, ', t= ', datetime.now().time())
	##### actual loop
	for x in range(0,len(time_series)):
		current_date = time_series[x]
		babies_0 = tab[var1][tab.date==current_date].values.astype(int)
		babies_day = np.sum(tab[var1][tab.date==current_date].values.astype(int))

		birthseries= np.append(birthseries, babies_day)
		# print('date',current_date,'babiesday' ,babies_day,'\n',babies_0,'\n \n')
		print('date',current_date,', babies born' ,babies_day)

	tok = time.perf_counter()
	DT= (tok-tik)/60
	DT_= '%.2f' % DT
	###### report time on loop
	print('finished loop, time: ',DT_,' minutes \n')

	return time_series, birthseries


##################################################################################
######## 2. numeric code input
def collect_variable(tab,var1):
	###########################################
	###########################################
	# print(tab.columns, '\n')
	###### loop parameters:
	time_series = tab['date'].unique()
	time_series = np.sort(time_series)

	codes = np.unique(tab[var1].values.astype(int))
	g = np.zeros((len(codes),len(time_series)))

	print('Procesing variable ', var1, ', number of codes: ',len(codes))
	
	for y in range(0,len(time_series)):
		current_date = time_series[y]
		MAGE = tab[var1][tab.date==current_date].values.astype(int)

		for x in range(0,len(codes)):
			current_code = codes[x]
			g[x,y] = len(MAGE[MAGE==current_code])


	return time_series, g

##################################################################################
######## 3. letter code input
def collect_YayNay_variable(tab,var1):
	###########################################
	###########################################
	# print(tab.columns, '\n')
	###### loop parameters:
	time_series = tab['date'].unique()
	time_series = np.sort(time_series)

	codes = np.unique(tab[var1].values)
	g = np.zeros((len(codes),len(time_series)))

	print('Procesing variable ', var1, ', number of codes: ',len(codes))
	
	for y in range(0,len(time_series)):
		current_date = time_series[y]
		MAGE = tab[var1][tab.date==current_date]

		for x in range(0,len(codes)):
			current_code = codes[x]
			g[x,y] = len(MAGE[MAGE==current_code])


	return time_series, g


'''

census functions
'''
def get_pop_percentages_F21(tab):

	''' (...) From the documentation. For further details read in census_data

	Index(['Label (Grouping)', 'United States!!Total!!Estimate',
	       'United States!!Total!!Margin of Error',
	       'United States!!Percent!!Estimate',
	       'United States!!Percent!!Margin of Error',
	       'United States!!Male!!Estimate', 'United States!!Male!!Margin of Error',
	       'United States!!Percent Male!!Estimate',
	       'United States!!Percent Male!!Margin of Error',
	       'United States!!Female!!Estimate',
	       'United States!!Female!!Margin of Error',
	       'United States!!Percent Female!!Estimate',
	       'United States!!Percent Female!!Margin of Error'],
	      dtype='object')

	0                              Total population
	1                                           AGE
	2                                 Under 5 years
	3                                  5 to 9 years
	4                                10 to 14 years
	5                                15 to 19 years
	6                                20 to 24 years
	7                                25 to 29 years
	8                                30 to 34 years
	9                                35 to 39 years
	10                               40 to 44 years
	11                               45 to 49 years
	12                               50 to 54 years
	13                               55 to 59 years
	14                               60 to 64 years
	15                               65 to 69 years
	16                               70 to 74 years
	17                               75 to 79 years
	18                               80 to 84 years
	19                            85 years and over
	20                      SELECTED AGE CATEGORIES
	21                                5 to 14 years
	22                               15 to 17 years
	23                               Under 18 years
	24                               18 to 24 years
	25                               15 to 44 years
	26                            16 years and over
	27                            18 years and over
	28                            21 years and over
	29                            60 years and over
	30                            62 years and over
	31                            65 years and over
	32                            75 years and over
	33                           SUMMARY INDICATORS
	34                           Median age (years)
	35            Sex ratio (males per 100 females)
	36                         Age dependency ratio
	37                     Old-age dependency ratio
	38                       Child dependency ratio
	39                            PERCENT ALLOCATED
	40                                          Sex
	41                                          Age
	'''
	# print(pop21['Label (Grouping)'],pop21['United States!!Total!!Estimate'])
	tab['United States!!Total!!Estimate'] = tab['United States!!Total!!Estimate'].str.replace(',','')
	total = int(tab['United States!!Total!!Estimate'][0])
	under_5 = float(tab['United States!!Total!!Estimate'][2])
	five_9 = float(tab['United States!!Total!!Estimate'][3])
	ten_14 = float(tab['United States!!Total!!Estimate'][4])
	fifteen_19 = float(tab['United States!!Total!!Estimate'][5])
	twenty_24 = float(tab['United States!!Total!!Estimate'][6])
	twentyfive_29 = float(tab['United States!!Total!!Estimate'][7])
	thirty_34 = float(tab['United States!!Total!!Estimate'][8])
	thirtyfive_39 = float(tab['United States!!Total!!Estimate'][9])
	forty_44 = float(tab['United States!!Total!!Estimate'][10])
	fortyfive_49 = float(tab['United States!!Total!!Estimate'][11])
	fifty_54 = float(tab['United States!!Total!!Estimate'][12])
	fiftyfive_59 = float(tab['United States!!Total!!Estimate'][13])
	sixty_64 = float(tab['United States!!Total!!Estimate'][14])
	sixtyfive_69 = float(tab['United States!!Total!!Estimate'][15])
	seventy_74 = float(tab['United States!!Total!!Estimate'][16])
	seventyfive_79 = float(tab['United States!!Total!!Estimate'][17])
	eighty_84 = float(tab['United States!!Total!!Estimate'][18])
	eightyfiveplus = float(tab['United States!!Total!!Estimate'][19])

	population_percentages=np.array([under_5, five_9, ten_14, fifteen_19, twenty_24, twentyfive_29, thirty_34, thirtyfive_39, forty_44, fortyfive_49, fifty_54, fiftyfive_59, sixty_64, sixtyfive_69, seventy_74, seventyfive_79, eighty_84, eightyfiveplus],dtype=int)
	return total, population_percentages

def get_pop_percentages(tab):

	''' (...) From the documentation. For further details read in census_data
	2 		S0101_C01_001E		Total!!Estimate!!Total population
	14 		S0101_C01_002E		Total!!Estimate!!AGE!!Under 5 years
	26 		S0101_C01_003E		Total!!Estimate!!AGE!!5 to 9 years
	38 		S0101_C01_004E		Total!!Estimate!!AGE!!10 to 14 years
	50 		S0101_C01_005E 		Total!!Estimate!!AGE!!15 to 19 years
	62 		S0101_C01_006E 		Total!!Estimate!!AGE!!20 to 24 years
	74 		S0101_C01_007E 		Total!!Estimate!!AGE!!25 to 29 years
	86 		S0101_C01_008E 		Total!!Estimate!!AGE!!30 to 34 years
	98 		S0101_C01_009E 		Total!!Estimate!!AGE!!35 to 39 years
	110 	S0101_C01_010E 		Total!!Estimate!!AGE!!40 to 44 years
	122 	S0101_C01_011E 		Total!!Estimate!!AGE!!45 to 49 years
	134 	S0101_C01_012E 		Total!!Estimate!!AGE!!50 to 54 years
	146 	S0101_C01_013E 		Total!!Estimate!!AGE!!55 to 59 years
	158 	S0101_C01_014E 		Total!!Estimate!!AGE!!60 to 64 years
	170 	S0101_C01_015E 		Total!!Estimate!!AGE!!65 to 69 years
	182 	S0101_C01_016E 		Total!!Estimate!!AGE!!70 to 74 years
	194 	S0101_C01_017E 		Total!!Estimate!!AGE!!75 to 79 years
	206 	S0101_C01_018E 		Total!!Estimate!!AGE!!80 to 84 years
	218 	S0101_C01_019E 		Total!!Estimate!!AGE!!85 years and over
	'''

	total = int(tab['S0101_C01_001E'][1])

	under_5 = float(tab['S0101_C01_002E'][1])
	five_9 = float(tab['S0101_C01_003E'][1])
	ten_14 = float(tab['S0101_C01_004E'][1])
	fifteen_19 = float(tab['S0101_C01_005E'][1])
	twenty_24 = float(tab['S0101_C01_006E'][1])
	twentyfive_29 = float(tab['S0101_C01_007E'][1])
	thirty_34 = float(tab['S0101_C01_008E'][1])
	thirtyfive_39 = float(tab['S0101_C01_009E'][1])
	forty_44 = float(tab['S0101_C01_010E'][1])
	fortyfive_49 = float(tab['S0101_C01_011E'][1])
	fifty_54 = float(tab['S0101_C01_012E'][1])
	fiftyfive_59 = float(tab['S0101_C01_013E'][1])
	sixty_64 = float(tab['S0101_C01_014E'][1])
	sixtyfive_69 = float(tab['S0101_C01_015E'][1])
	seventy_74 = float(tab['S0101_C01_016E'][1])
	seventyfive_79 = float(tab['S0101_C01_017E'][1])
	eighty_84 = float(tab['S0101_C01_018E'][1])
	eightyfiveplus = float(tab['S0101_C01_019E'][1])

	population_percentages=np.array([under_5, five_9, ten_14, fifteen_19, twenty_24, twentyfive_29, thirty_34, thirtyfive_39, forty_44, fortyfive_49, fifty_54, fiftyfive_59, sixty_64, sixtyfive_69, seventy_74, seventyfive_79, eighty_84, eightyfiveplus],dtype=int)
	return total, population_percentages


def get_pop_percentages_F15(tab):

	''' (...) From the documentation. For further details read in census_data
	2 		S0101_C01_001E		Total!!Estimate!!Total population
	14 		S0101_C01_002E		Total!!Estimate!!AGE!!Under 5 years
	26 		S0101_C01_003E		Total!!Estimate!!AGE!!5 to 9 years
	38 		S0101_C01_004E		Total!!Estimate!!AGE!!10 to 14 years
	50 		S0101_C01_005E 		Total!!Estimate!!AGE!!15 to 19 years
	62 		S0101_C01_006E 		Total!!Estimate!!AGE!!20 to 24 years
	74 		S0101_C01_007E 		Total!!Estimate!!AGE!!25 to 29 years
	86 		S0101_C01_008E 		Total!!Estimate!!AGE!!30 to 34 years
	98 		S0101_C01_009E 		Total!!Estimate!!AGE!!35 to 39 years
	110 	S0101_C01_010E 		Total!!Estimate!!AGE!!40 to 44 years
	122 	S0101_C01_011E 		Total!!Estimate!!AGE!!45 to 49 years
	134 	S0101_C01_012E 		Total!!Estimate!!AGE!!50 to 54 years
	146 	S0101_C01_013E 		Total!!Estimate!!AGE!!55 to 59 years
	158 	S0101_C01_014E 		Total!!Estimate!!AGE!!60 to 64 years
	170 	S0101_C01_015E 		Total!!Estimate!!AGE!!65 to 69 years
	182 	S0101_C01_016E 		Total!!Estimate!!AGE!!70 to 74 years
	194 	S0101_C01_017E 		Total!!Estimate!!AGE!!75 to 79 years
	206 	S0101_C01_018E 		Total!!Estimate!!AGE!!80 to 84 years
	218 	S0101_C01_019E 		Total!!Estimate!!AGE!!85 years and over
	'''

	total = int(tab['S0101_C01_001E'][1])

	under_5 = float(tab['S0101_C01_002E'][1])
	five_9 = float(tab['S0101_C01_003E'][1])
	ten_14 = float(tab['S0101_C01_004E'][1])
	fifteen_19 = float(tab['S0101_C01_005E'][1])
	twenty_24 = float(tab['S0101_C01_006E'][1])
	twentyfive_29 = float(tab['S0101_C01_007E'][1])
	thirty_34 = float(tab['S0101_C01_008E'][1])
	thirtyfive_39 = float(tab['S0101_C01_009E'][1])
	forty_44 = float(tab['S0101_C01_010E'][1])
	fortyfive_49 = float(tab['S0101_C01_011E'][1])
	fifty_54 = float(tab['S0101_C01_012E'][1])
	fiftyfive_59 = float(tab['S0101_C01_013E'][1])
	sixty_64 = float(tab['S0101_C01_014E'][1])
	sixtyfive_69 = float(tab['S0101_C01_015E'][1])
	seventy_74 = float(tab['S0101_C01_016E'][1])
	seventyfive_79 = float(tab['S0101_C01_017E'][1])
	eighty_84 = float(tab['S0101_C01_018E'][1])
	eightyfiveplus = float(tab['S0101_C01_019E'][1])

	population_percentages=np.array([under_5, five_9, ten_14, fifteen_19, twenty_24, twentyfive_29, thirty_34, thirtyfive_39, forty_44, fortyfive_49, fifty_54, fiftyfive_59, sixty_64, sixtyfive_69, seventy_74, seventyfive_79, eighty_84, eightyfiveplus],dtype=float)
	return total, population_percentages



##### make time series data from census data:
def make_population_series(total,year_,time_series):
	population_series = np.array([],dtype=int)
	t_series = np.array([])
	for x in time_series:
		if x[0:4]==str(year_):
			population_series= np.append(population_series, int(total))
			t_series = np.append(t_series, x)
	return population_series, t_series



'''
mortality functions

'''




'''
multivariate analysis
'''

def get_two_column(source_dir,bigData,var1,var2):
	tab = bigData[['date', var1,var2]].copy()
	tab = tab.dropna(subset=[var1,var2,'date'])
	dict1 = pd.read_excel(source_dir+'CDC_database_codeNames.xlsx')
	cod_of_int1 = dict1.Code[dict1.Code==var1]
	cod_of_int2 = dict1.Code[dict1.Code==var2]
	var_of_int1 = dict1.Label[dict1.Code==var1]
	var_of_int2 = dict1.Label[dict1.Code==var2]
	print(	cod_of_int1.values[0], var_of_int1.values[0], '\n',
			cod_of_int2.values[0], var_of_int2.values[0])

	codes = [cod_of_int1.values[0],cod_of_int2.values[0]]
	labes = [var_of_int1.values[0],var_of_int2.values[0]]
	return tab, labes, codes


def get_plus_column(source_dir,bigData,var1,var2,var3,var4,var5,dvar):
	tab = bigData[['date', var1,var2,var3,var4,var5,dvar]].copy()
	tab = tab.dropna(subset=[var1,var2,var3,var4,var5,dvar,'date'])
	dict1 = pd.read_excel(source_dir+'CDC_database_codeNames.xlsx')
	cod_of_int1 = dict1.Code[dict1.Code==var1]
	cod_of_int2 = dict1.Code[dict1.Code==var2]
	cod_of_int3 = dict1.Code[dict1.Code==var3]
	cod_of_int4 = dict1.Code[dict1.Code==var4]
	cod_of_int5 = dict1.Code[dict1.Code==var5]
	cod_of_dvar = dict1.Code[dict1.Code==dvar]
	var_of_int1 = dict1.Label[dict1.Code==var1]
	var_of_int2 = dict1.Label[dict1.Code==var2]
	var_of_int3 = dict1.Label[dict1.Code==var3]
	var_of_int4 = dict1.Label[dict1.Code==var4]
	var_of_int5 = dict1.Label[dict1.Code==var5]
	var_of_dvar = dict1.Label[dict1.Code==dvar]
	print(	cod_of_int1.values[0], var_of_int1.values[0], '\n',
			cod_of_int2.values[0], var_of_int2.values[0], '\n',
			cod_of_int2.values[0], var_of_int3.values[0], '\n',
			cod_of_int2.values[0], var_of_int4.values[0], '\n',
			cod_of_int2.values[0], var_of_int5.values[0], '\n',
			cod_of_int2.values[0], var_of_dvar.values[0])

	codes = [cod_of_int1.values[0], cod_of_int2.values[0], cod_of_int3.values[0], cod_of_int4.values[0], cod_of_int5.values[0], cod_of_dvar.values[0]]
	labes = [var_of_int1.values[0], var_of_int2.values[0], var_of_int3.values[0], var_of_int4.values[0], var_of_int5.values[0], var_of_dvar.values[0]]
	return tab, labes, codes
