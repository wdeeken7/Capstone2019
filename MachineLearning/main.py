from azureml.core import Experiment
from azureml.core import Workspace

from azureml.core.runconfig import RunConfiguration
from dataPrep import *
from train1 import *
import csv
testSize = .75
#This must be changed for your specific file location.
dataset_root = "C:\\Users\\wdeek\\Documents\\Spring 2019\\williamCapstone\\cuformodel.csv"
#Path to write file with predicted values.
to_predict_array = dict()
to_predict_array["Bad_year_corn"] = "PATH1"
to_predict_array["Good_year_corn"] = "PATH2"

predicted_values_folder = "PATH3"

shouldShuffle = True
#preppedData is a tuple containing (x_toTrain, x_toTest, y_toTrain, y_toTest) 
preppedData = prepareDataForMLTraining(testSize, dataset_root, shouldShuffle)
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
    experiment = Experiment(ws, "Regression_Attempt_1")
    automated_ml_config = model(preppedData[0], preppedData[2], "FOLDER HARD CODED", 10, 2, 'normalized_mean_absolute_error', 5, 'regression')
    local_run = experiment.submit(automated_ml_config, show_output=True)
    #### Here is where testing code should go. ########
    #The following code finds the best model. Then runs a predict and prints.
    def retrieveBestAndPredict():
        best_run, fitted_model = local_run.get_output()
        print(best_run)
        print(fitted_model)
        for key, value in to_predict_array:
            y_predict = fitted_model.predict(value)
            #Now, will create and write to a .csv file with filepath defined above.
            with open(predicted_values_folder + "//" + key , mode='w') as csv_file:
                filewriter = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['ID', 'Normed_Dry_Yld_Vol'])
                index = 1
                for gridBox in y_predict:
                    filewriter.writerow([index, str(gridBox)])
                    index = index + 1
    retrieveBestAndPredict()
    

if __name__ == '__main__':
    main()


