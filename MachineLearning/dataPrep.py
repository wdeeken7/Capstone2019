from azureml.core import Workspace
import azureml.dataprep as dprep
from azureml.core.runconfig import RunConfiguration
from sklearn.model_selection import train_test_split

# dataset_root path must be set to where YOU are storing the .csv file.
dataset_root = "C:/Users/wdeek/Documents/Spring 2019/williamCapstone/cuformodel.csv"

#Creates a DataFlow object from .csv file
dataFlow = dprep.auto_read_file(dataset_root, False)

#Defines the input (X) columns and the output-to-predict (Y) columns from the .csv file.
dataflow_X = dataFlow.keep_columns(['Soil_Name','MEAN_Eleva', 'V.A.T(F)','R.A.T(F)', 'M.A.T(F)', 'V.PET(inch)','R.PET(inch)', 'M.PET(inch)', 'V.T.R(inch)', 'R.T.R(inch)' ])
dataflow_Y = dataFlow.keep_columns('NormalizedYield')

#Converts data into a pandas DataFrame to ease in splitting data into Train/Test sets.
x_dataFlow_Pandas = dataflow_X.to_pandas_dataframe()
y_dataFlow_Pandas = dataflow_Y.to_pandas_dataframe()

#Splits data into a train portion and a test portion

#User-defined parameters for how the dataset is split for training/testing purposes.
#Test size should be a float between 0 and 1. Train size is 1 - testSize.
testSize = .25
#shouldShuffle determines whether data is given a final shuffle before division.
shouldShuffle = True

X_toTrain, X_toTest, Y_toTrain, Y_toTest = train_test_split(x_dataFlow_Pandas, y_dataFlow_Pandas, test_size= testSize, random_state=173, shuffle=shouldShuffle)

 