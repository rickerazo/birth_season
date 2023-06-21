# Ricardo Erazo, PhD
Seattle Children's Research Institute
Center for Integrative Brain Research
2024

# CovidBirth_data_pipeline

## general libraries needed:
- numpy
- matplotlib
- pandas
- os
- datetime
- time
- scipy

## preprocess_birth_data.py

This script takes as input the *csv* file downloaded from the NBR website:
	https://www.nber.org/research/data/vital-statistics-natality-birth-data
	US Data files:
		Years 2015 through 2021

### Considerations:
- Script assumes that there's a child directory named csv_data, where all the downloaded files are stored.
- Files sometimes are downloaded as *zip, in such case, it'll be necessary to unzip to access the file
- Arrange code/directories accordingly.


### Instructions:
- Make new directory, named csv_data
- In the new directory, Download data from website and specific years above
- Unzip files if necessary
- run preprocess_birth_data.py
- run covidbirth.py
- run mathbirths.py



### The logic
behind preprocessing, and subsequent loading is to speed up computations:

1. The preprocessing algorithm takes 1 hour to run, and saves the output of its concatenation
as a large csv file.
2. Loading the output from the pre-processed file takes roughly 10 minutes. It's a significant speed-up
compared to running and loading the csv file of each year individually (10 minutes each, 70 minutes total)
3. Keeping several large dataframes loaded into RAM is inefficient and makes simple computations slow.

## covidbirth.py

This script takes as input the output from the pre-processing algorithm.
Data must me pre-processed in order to be loaded from this script.

### The purposes of this script are to:
- implement a general method to quantify variables of interest from the CDC birth database.
- visualize seasonal and general trends in births in the US
- use births per month as a normalization parameter to visualize other variables.
- produce an output for subsequent mathematical modeling and rhythmic characterization.


### Considerations:
- Script assumes that there's a child directory named covidbirth, and one named census_data
- Where all the data and preprocessing scripts are executed.
- Arrange code/directories accordingly.

### Instructions:
- Execute preprocessing algorithm
- Execute covidbirth.py algorithm
- Execute math_births.py


## math_births.py

Mathematical model and rhythmic characterization of seasonal births

Here, we import the output from the pipeline: times_series, birthseries, and other similar
post-processed variables in timeseries format

We apply a mathematical model from the combination of a linear and a periodic model.
To account to the overall trend - decrease in # of births
and the seasonal structure to births - low in winter and high in summer.

Abstract model that replicates observed oscillation and overall trend.

Interesting finding! according to the model, 2020 was the OFF year,
while the trend seems to recover by 2021.

## ninja_functions.py

library of custom functions.
These functions support analysis of CDC, and Census data.
These are kept in a separate script because they are called from several other scripts,
and in order to maintain consistency between codes, the functions ought to the shared.