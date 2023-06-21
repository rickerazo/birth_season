'''

Ricardo Erazo, PhD 	2024
Seattle Children's Research Institute
Center for Integrative Brain Research

Mathematical model and rhythmic characterization of seasonal births

Here, we import the output from the pipeline: times_series, birthseries, and other similar
post-processed variables in timeseries format

We apply a mathematical model from the combination of a linear and a periodic model.
To account to the overall trend - decrease in # of births
and the seasonal structure to births - low in winter and high in summer.

Abstract model that replicates observed oscillation and overall trend.

Interesting finding! according to the model, 2020 was the OFF year,
while the trend seems to recover by 2021.



LAST SCRIPT TO RUN IN THE PIPELINE

'''


import ninja_functions
# math_births.py
## libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import os

from scipy.signal import find_peaks
from scipy.signal import savgol_filter
from scipy.stats import linregress

import plotly.graph_objects as go
import plotly.express as px

# from causalimpact import CausalImpact
from datetime import datetime, timedelta

# from datetime import datetime
import time

os.makedirs('model_output/',exist_ok=True)
os.makedirs('model_data/',exist_ok=True)

## graphics stuff
import matplotlib as mpl
mpl.rcParams['axes.linewidth']=0
font = {'weight':'normal','size':25}
plt.rc('font', **font)
plt.rcParams['agg.path.chunksize'] = 1000

#################################################################################### setting up directories
legend_font = {'size': 12, 'weight': 'normal'}
### plotting crutch
colores = ['forestgreen','orangered','cyan','brown','magenta','violet']
#
time_series = 	np.load('model_data/time_series.npy', allow_pickle=True)
birthseries = 	np.load('model_data/birthseries.npy', allow_pickle=False)
days_in_month = np.load('model_data/days_series.npy', allow_pickle=False)
g = np.load('model_data/mage_series.npy', allow_pickle=False)
n = np.load('model_data/prenaseries.npy', allow_pickle=False)
e = np.load('model_data/educ_series.npy', allow_pickle=False)
yay_nay = 		np.load('model_data/fertiseries.npy', allow_pickle=False)

########## normalize around a median value:
birth_median15 = np.median(birthseries[0:12])
birth_median16 = np.median(birthseries[12:24])
birth_median17 = np.median(birthseries[24:36])
birth_median18 = np.median(birthseries[36:42])
birth_median19 = np.median(birthseries[42:60])
birth_median20 = np.median(birthseries[60:72])
birth_median21 = np.median(birthseries[72:84])


######## create timeseries of birth median, use it to normalize, visualize normalized data
pop15, t_15 = ninja_functions.make_population_series(birth_median15, '2015',time_series)
pop16, t_16 = ninja_functions.make_population_series(birth_median16, '2016',time_series)
pop17, t_17 = ninja_functions.make_population_series(birth_median17, '2017',time_series)
pop18, t_18 = ninja_functions.make_population_series(birth_median18, '2018',time_series)
pop19, t_19 = ninja_functions.make_population_series(birth_median19, '2019',time_series)
pop20, t_20 = ninja_functions.make_population_series(birth_median20, '2020',time_series)
pop21, t_21 = ninja_functions.make_population_series(birth_median21, '2021',time_series)

median_normalization = np.concatenate((pop15, pop16, pop17, pop18, pop19, pop20, pop21), axis=None)

### normalized births series, remove the trend, only the oscillation:
seasonal_births = birthseries-median_normalization

########## characterize trough to peak amplitude:
## id troughs:
peaks_locs, peaks_ = find_peaks(seasonal_births, height=3500, distance=6)
troughlocs, trough = find_peaks(-seasonal_births, height=3500, distance=6)

oscillation_amplitude = np.abs(seasonal_births[troughlocs[0:-1]],seasonal_births[peaks_locs])

print('\nCDC DATA: \n')
print('Oscillation amplitudes: ' ,oscillation_amplitude,'\n')

print('peak months: ' ,time_series[peaks_locs],'\n')

print('trough months: ' ,time_series[troughlocs[0:-1]],'\n')

###### rhythmic characteristics:
print('distance between peaks: ', np.diff(peaks_locs),'\n')

print('distance between troughs: ', np.diff(troughlocs[0:-1]),'\n')

print('distance between amplitudes: ', np.diff(oscillation_amplitude),'\n')

#### linear regression on median trend
## ordinal variable, dummy but encodes linearity
x_ = np.arange(0,len(time_series),1)

trend = linregress(x_, median_normalization)

print('Linear regression of decreasing trend (births median per year). R= ', '%.2f' % trend.rvalue, ', p = ', '%.3f' % trend.pvalue)

# shift_ = 10
shift_ = 5
period_ = .51


## linear part fitted. The sine wave seems a good candidate. let's tweak a few function parameters to figure whether we can use it to model birth seasonality

# for shift_ in np.arange(0,10,1):
# for period_ in np.arange(.48,.55,1e-2):

#################################
## visualize data
f0=plt.figure(figsize=(30,20))
ax1=f0.add_subplot(211)
ax2=f0.add_subplot(212)

ax3 = ax2.twinx()

## raw data
ax1.plot(time_series, birthseries)
ax1.plot(time_series, median_normalization)


## normalized data, remove declining trend. model median separately (linear)
ax2.plot(time_series, seasonal_births)
### peaks and troughs
ax2.scatter(time_series[peaks_locs], seasonal_births[peaks_locs],c='k')
ax2.scatter(time_series[troughlocs[0:-1]], seasonal_births[troughlocs[0:-1]],c='r')

p1=ax1.get_xticks()
p2=ax2.get_xticks()
ax1.set_xticks(np.arange(p1[0],p1[-1],12))
ax2.set_xticks(np.arange(p2[0],p2[-1],12))

ax1.set_ylabel('total births')
ax2.set_ylabel('births- yearly median')

f0.autofmt_xdate(rotation=45)

f0.savefig('model_output/f1_simple.png')


### plot linear model
model_l = x_*trend.slope+trend.intercept
ax1.plot(time_series, model_l, c='r',linewidth=2)
f0.savefig('model_output/f1_linear_model.png')
#### smoothened line
ax2.plot(time_series, savgol_filter(seasonal_births, 3, 1),linewidth=3)

f0.savefig('model_output/f1_smoothened.png')

### plot periodic model
## first attempt: sine wave
periodic_model = np.sin(period_*x_+shift_)
ax3.plot(x_, periodic_model, c='orangered',linewidth=3)
# ax3.plot(x, np.sin(.5*x), c='orangered',linewidth=3)

# plt.close('all')
f0.savefig('model_output/f1_periodic_model.png')


####### generate artificial curve
amplitude_ = 30e3
oscillation_model = amplitude_*periodic_model+ model_l

ax1.plot(time_series, oscillation_model, c='orangered', linewidth=3)


f0.savefig('model_output/f1_full_model_.png')
# f0.savefig('model_output/f1_shift_'+str( '%.2f' % shift_)+'_period_'+str( '%.2f' % period_)+'_.png')
plt.close('all')	

print('\nMODEL:\n')
peaks_locs_m, peaks__m= find_peaks(periodic_model)
troughlocs_m, trough_m = find_peaks(-periodic_model)

oscillation_amplitude_model = np.abs(periodic_model[troughlocs_m],periodic_model[peaks_locs_m[0:6]])

print('Oscillation amplitudes: ' ,oscillation_amplitude_model,'\n')

print('peak months: ' ,x_[peaks_locs_m[0:6]],'\n')
print('peak dates: ' ,time_series[peaks_locs_m[0:6]],'\n')

print('trough months: ' ,x_[troughlocs_m],'\n')
print('trough dates: ' ,time_series[troughlocs_m],'\n')

###### rhythmic characteristics:
print('distance between peaks: ', np.diff(peaks_locs_m[0:6]),'\n')

print('distance between troughs: ', np.diff(troughlocs_m),'\n')

print('distance between amplitudes: ', np.diff(oscillation_amplitude_model),'\n')