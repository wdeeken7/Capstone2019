from azureml.core import Experiment
from azureml.core import *
from retrieve import *
from azureml.core.runconfig import RunConfiguration
from dataPrep import *
from train1 import *
import csv
import pandas as pd
#This must be changed for your specific file location.
dataset_root = "C:\\Users\\wdeek\\Desktop\\ML Service\\cumodelwo2014.csv"
#Path to write file with predicted values.
to_predict_array = dict()
to_predict_array["2014"] ="C:\\Users\\wdeek\\Desktop\\ML Service\\test2014.csv" 
#to_predict_array["Good_year_corn"] = "PATH2"
#toPredict = "C:\\Users\\wdeek\\Documents\\Spring 2019\\williamCapstone\\testingScenario.csv"
predicted_values_folder = "C:\\Users\\wdeek\\Documents\\Spring 2019\\williamCapstone"
shouldShuffle = True
#preppedData is a tuple containing (x_df, y_df)
preppedData = pd.read_csv(dataset_root)
X_toTrain = preppedData.filter(items = ['cell-ID','Soil_Name','MEAN_Eleva','Crop-Type'])
Y_toTrain = preppedData.filter(items = ['NormalizedYield'])

def main():
    print("Beginning ML runs")
    #### This doc should contain meta-data for ML experiment runs ####
    #This sets the compute target to your local machine. 
    run_user_managed = RunConfiguration()
    run_user_managed.environment.python.user_managed_dependencies = False
    #Can also adjust for a specific python interpreter if desired. Otherwise, it uses the specific one declared by IDE.


    #This determines what workspace to run experiments in. Should not need any edits.
   
    ws = Workspace.from_config()
  

    #The remainder of this doc should run the models defined in other documents. 
    #This experiment runs the REGRESSION model.
    experiment = Experiment(ws, "RunFinal1")
    automated_ml_config = model(X_toTrain, Y_toTrain, "FOLDER HARD CODED", 10, 30, 'normalized_root_mean_squared_error', 5, 'regression')
    local_run = experiment.submit(automated_ml_config, show_output=True)
    ####Code to explore runs####
    def retrieveRunData():
        children = list(local_run.get_children())
        metricslist = {}
        for run in children:
            properties = run.get_properties()
            metrics = {k: v for k, v in run.get_metrics().items() if isinstance(v, float)}
            metricslist[int(properties['iteration'])] = metrics

        rundata = pd.DataFrame(metricslist).sort_index(1)
        print(rundata)
    retrieveRunData()
    #The following method retrieves the best test run's model, and makes a prediction using the previously defined .csv file.
    for toPredict in to_predict_array:
        retrieveAndPredict('normalized_root_mean_squared_error', 'runFinal1', toPredict, predicted_values_folder)
    

    

if __name__ == '__main__':
    main()


