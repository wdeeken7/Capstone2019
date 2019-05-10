from azureml.core import Workspace
import azureml.dataprep as dprep
from azureml.core.runconfig import RunConfiguration
from sklearn.model_selection import train_test_split
import pandas as pd
#This doc prepares the yield data for model training and testing.
#Currently, this code sets all years as training data except the year(s) that planted cropTypeForTest. These years are left aside for 
#testing. 
def prepareDataForMLTraining(dataset_root, cropToTest):
    # dataset_root path must be set to where YOU are storing the .csv file.
      
    dataFrame = pd.read_csv(dataset_root)
    #Renames crop type. Queries do not accept the "-" character.
    dataFrame.rename(columns={"Crop-Type" : "Crop"}, inplace=True)
    #Queries dataFrame for the crop type to test. Returns all rows that satisfy the condition. 
    toTrain = dataFrame.query("Crop != @cropToTest")
    toTest = dataFrame.query("Crop == @cropToTest")
    #Defines the input (X) columns and the output-to-predict (Y) columns from the .csv file.
    
    X_toTrain = toTrain.filter(items = ['Crop-Type', 'V.A.T(F)','R.A.T(F)', 'M.A.T(F)', 'V.PET(inch)','R.PET(inch)', 'M.PET(inch)', 'V.T.R(inch)', 'R.T.R(inch)' ])
    Y_toTrain = toTrain.filter(items = ['NormalizedYield'])
    X_toTest = toTest.filter(items = ['Crop-Type', 'V.A.T(F)','R.A.T(F)', 'M.A.T(F)', 'V.PET(inch)','R.PET(inch)', 'M.PET(inch)', 'V.T.R(inch)', 'R.T.R(inch)' ])
    Y_toTest = toTest.filter(items = ['NormalizedYield'])
    
  
    
   
    #X_toTrain, X_toTest, Y_toTrain, Y_toTest = train_test_split(x_dataFlow_Pandas, y_dataFlow_Pandas, test_size= testSize, random_state=173, shuffle=shouldShuffle)

    return (X_toTrain, Y_toTrain, X_toTest, Y_toTest)