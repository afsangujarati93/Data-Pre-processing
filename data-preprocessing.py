import pandas as pd
import inspect
from Log_Handler import Log_Handler as lh
import statistics as s
import numpy as np

process_logger = lh.log_initializer("process_log.log", True)
error_logger = lh.log_initializer("error_log.log", False)
# method_name = inspect.stack()[0][3]
# try:
# except Exception as Ex:
# 	print("Expcetion occurred in " + method_name + "| Exception:" + str(Ex))
from time import sleep
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	method_name = inspect.stack()[0][3]
	try:
		"""
		Call in a loop to create terminal progress bar
		@params:
		    iteration   - Required  : current iteration (Int)
		    total       - Required  : total iterations (Int)
		    prefix      - Optional  : prefix string (Str)
		    suffix      - Optional  : suffix string (Str)
		    decimals    - Optional  : positive number of decimals in percent complete (Int)
		    length      - Optional  : character length of bar (Int)
		    fill        - Optional  : bar fill character (Str)
		"""
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
		# Print New Line on Complete
		if iteration == total: 
		    print("Completed the process")
	except Exception as Ex:
		print("Expcetion occurred in " + method_name + "| Exception:" + str(Ex))

def main():
	method_name = inspect.stack()[0][3]
	try:
		file_name = input("Input Dataset csv file name along with extension: ");
		file_name = "Dataset/" + file_name
		import_data_parse(file_name);

	except Exception as Ex:
		print("Expcetion occurred in " + method_name + "| Exception:" + str(Ex))


def import_data_parse(file_name):
	method_name = inspect.stack()[0][3]

	try:
		# delete process log file
		df_result = pd.read_csv(file_name);		
		column_log = ''
		row_log = ''
		#percentage of data to consider for trimming process
		per_data_consider = float(input("Please enter the percentage(%) of Data to process: "))
		data_index_consider = (per_data_consider/100) * len(df_result)
		df_result = df_result.loc[:data_index_consider]
		shape_begin = "\nShape At Beginning:" + str(df_result.shape)

		nan_row_threshold = 30
		print("Scanning and deleting rows with more than {}% NaN values".format(nan_row_threshold))
		printProgressBar(0, len(df_result), prefix = 'Progress:', suffix = 'Complete', length = 50)
		
		total_row_count = len(df_result)
		for index, df_row in df_result.iterrows():
			
			row_log = '\n================================'
			row_log += "\nRow index:" + str(index)			
			nan_count = df_row.isnull().sum()
			total_count = len(df_row)
			per_nan = (nan_count/total_count)*100
			row_log += "\nNaN count: " + str(nan_count) + "\nTotal elements:" + str(total_count) +  "\n% NaN entries:" + str(per_nan) 
			process_logger.info(row_log)
			
			if(per_nan > nan_row_threshold):				
				df_result.drop(index, inplace = True)
				deleted_log = "\n***Deleted row because of more than {}% NaN entries***".format(nan_row_threshold)
				process_logger.info(deleted_log)			
			
			printProgressBar(index + 1, total_row_count, prefix = 'Progress:', suffix = 'Complete', length = 50)
			
			row_log = '\n================================'
			process_logger.info('\n================================')			
		

		shape_before = "\nShape Before:" + str(df_result.shape)
		# print(shape_before)
		col_category_dict = {}
		nan_col_threshold = 30
		total_col_count = df_result.shape[1]
		print("Scanning and deleting columns with more than {}% NaN values".format(nan_col_threshold))
		printProgressBar(0, len(df_result), prefix = 'Progress:', suffix = 'Complete', length = 50)
		index = 0
		for df_col in df_result:
			column_log = '\n================================'
			column_log += "\nColumn name:" + df_col
			#Condition 1, if more than 10% of data is NaN, get rid of it
			nan_count = df_result[df_col].isnull().sum()
			total_count = len(df_result[df_col])
			per_nan = (nan_count/total_count)*100
			column_log += "\nNaN count: " + str(nan_count) + "\nTotal elements:" + str(total_count) +  "\n% NaN entries:" + str(per_nan) 
			process_logger.info(column_log)
			if(per_nan > nan_col_threshold):
				del df_result[df_col]
				deleted_log = "\n***Deleted column because of more than {}% NaN entries***".format(nan_col_threshold)
				process_logger.warning(deleted_log)
			elif str(df_result[df_col].dtype) == "object":
				currr_cat_dict = {}				
				# Condition 2, Divide data into category, store category names
				# converting objects to categories								
				df_result[df_col] = pd.Categorical(df_result[df_col])
				df_result[df_col] = df_result[df_col].cat.add_categories("unknown")
				#storing categories with column names for header attributes				
				col_category_dict[df_col] = df_result[df_col].cat.categories.tolist()
				df_result[df_col] = df_result[df_col].fillna("unknown")

				# ====================================================================================
				# only for considering columns with numeric value
				# # ====================================================================================
				# del df_result[df_col]
				# deleted_log = "\n***Deleted column because we are considering only numeric entries***"
				# ====================================================================================
				# Approach to insert the missing values with average of the categories (not feasible)
				# ====================================================================================
				# unique_codes = pd.unique(df_result[df_col].cat.codes)				
				# currr_cat_dict = dict(zip(unique_codes,df_result[df_col].cat.categories.tolist()))
				# error_logger.info("Current Dict:" + str(currr_cat_dict))				
				# taking the mean of categories and rounding it up to replace it with NaN				
				# Figure out a better way to do it
				# average_code = int(round(s.mean(unique_codes)))
				# average_cat = currr_cat_dict.get(average_code, "")
				# df_result[df_col].fillna(average_cat)

				# error_logger.info(df_col + " |Average code:" + str(average_code) + "| Average cat:" + str(average_cat))				
			else:								
				col_category_dict[df_col] = "NUMERIC"
				average_val = df_result[df_col].mean()			
				df_result[df_col] = df_result[df_col].fillna(average_val)
				df_result[df_col] = df_result[df_col].replace(r'\s+', average_val, regex=True)				
				
			printProgressBar(index + 1, total_col_count, prefix = 'Progress:', suffix = 'Complete', length = 50)			
			column_log = '\n================================'
			index += 1
		shape_after = "\nShape After:" + str(df_result.shape)
		print(shape_begin + " " + shape_before + " "  + shape_after)
		
		create_arff(col_category_dict, df_result)
		# df_result.to_csv("updated_csv.csv")		
	except Exception as Ex:
		print("Expcetion occurred in " + method_name + "| Exception:" + str(Ex))


def create_arff(col_category_dict, dataset_body):
	method_name = inspect.stack()[0][3]
	try:
		error_logger.debug("in method :" + method_name)
		arff_file = open("Dataset/arff_output_dataset.arff","w") 
		arff_file.write("@RELATION stackoverflow \n\n\n")
		
		for col_name, col_cat in col_category_dict.items():
			attribute_string = "@ATTRIBUTE " + col_name + " " + str(col_cat) + "\n"
			attribute_string = attribute_string.replace("[", "{")
			attribute_string = attribute_string.replace("]", "}")
			arff_file.write(attribute_string)

		arff_file.write("\n\n@DATA\n")
		for index, df_row in dataset_body.iterrows():
			data_row_string = str(df_row.values.tolist()) + "\n"
			data_row_string = data_row_string.replace("[", "")
			data_row_string = data_row_string.replace("]", "")
			arff_file.write(data_row_string)

		arff_file.close()
		
	except Exception as Ex:
		print("Expcetion occurred in " + method_name + "| Exception:" + str(Ex))


if __name__ == '__main__':
	main()

# df_result[df_result.columns[0]].isnull().any()
# df_result[df_result.columns[0]].isnull().sum()
# len(df_result[df_result.columns[0]])