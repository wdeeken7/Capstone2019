from azureml.core import Workspace
import azureml.dataprep as dprep
from azureml.core.runconfig import RunConfiguration
#### This doc should contain meta-data for ML experiment runs ####
#This sets the compute target to your local machine. 
run_user_managed = RunConfiguration()
run_user_managed.environment.python.user_managed_dependencies = True
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
#The remainder of this doc should run the models defined in other documents. 
#This experiment runs the REGRESSION model.
experiment = Experiment(ws, "Regression_Attempt_1")
local_run = experiment.submit(automated_ml_config, show_output=True)