# Data-Pre-processing
The script helps in data reduction and to handle missing values in a dataset by replacing the null/empty nominal attributes with "unknown" and null/empty numeric attributes with its mean. Furthermore, the script also convert the csv to arff file, which can be easily loaded in Weka.


**Variables to look for:** 
* nan_row_threshold => Thresshold value for row/instances nan i.e. if a row has more than the threshold percentage of null/empty values it would be deleted from the dataset. Currently the value is set to 30.
* nan_col_threshold => Thresshold value for column/attributes nan i.e. if a row has more than the threshold percentage of null/empty values it would be deleted from the dataset. Currently the value is set to 30.


**How to use:** 
* Place your csv file in Dataset folder 
* execute command python data-preprocessing.py 
* command line input will ask for the file name with csv
* command line input will ask for percentage of data to consider
* The arff file created will be placed in Dataset folder with name arff_output_dataset.arff
