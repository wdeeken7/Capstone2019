from azureml.core import Experiment
from azureml.core import Workspace

from azureml.core.runconfig import RunConfiguration
from dataPrep import *
from train1 import *
testSize = .75
#This must be changed for your specific file location.
dataset_root = "C:\\Users\\wdeek\\Documents\\Spring 2019\\williamCapstone\\cuformodel.csv"
shouldShuffle = True
#prepperData is a tuple containing (x_toTrain, x_toTest, y_toTrain, y_toTest) 
preppedData = prepareDataForMLTraining(testSize, dataset_root, shouldShuffle)
def main():
    print("Beginning ML runs")
    #### This doc should contain meta-data for ML experiment runs ####
    #This sets the compute target to your local machine. 
    run_user_managed = RunConfiguration()
    run_user_managed.environment.python.user_managed_dependencies = False
    #Can also adjust for a specific python interpreter if desired. Otherwise, it uses the specific one declared by IDE.


    #This determines what workspace to run experiments in. Should not need any edits.
    try:
        #This provides information to access ML Service workspace. Do not change.
        ws = Workspace(subscription_id = "8402fd02-6a15-499c-bb04-1dee338962d6", resource_group = "NDSUCapstone2019", workspace_name = "Capstone2019MLServerWorksapce")
        # write the details of the workspace to a configuration file.
        ws.write_config()
        print("Workspace configuration succeeded. Skip the workspace creation steps below")
    except:
        print("Workspace not accessible. Change your parameters or create a new workspace below")
    ws = Workspace.from_config()
  

    #The remainder of this doc should run the models defined in other documents. 
    #This experiment runs the REGRESSION model.
    experiment = Experiment(ws, "Regression_Attempt_1")
    automated_ml_config = model(preppedData[0], preppedData[2], "FOLDER HARD CODED", 10, 20, 'spearman_correlation', 5, 'regression')
    local_run = experiment.submit(automated_ml_config, show_output=True)
    #### Here is where testing code should go. ########
if __name__ == '__main__':
    main()

