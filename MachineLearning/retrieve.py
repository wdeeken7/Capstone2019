from azureml.core import Experiment
from azureml.core import Workspace

from azureml.core.runconfig import RunConfiguration
from dataPrep import *
from train1 import *
import csv
import pandas as pd
def retrieveAndPredict(primaryMetric, experimentName, valuesToPredictOn, predicted_values_folder):
        ### This file finds the best run child run in an automl run, and deploys the model. Then, predictions are run on the model.
        
        df = pd.read_csv(valuesToPredictOn)
        X_toTest = df.filter(items = ['cell-ID','Soil_Name','MEAN_Eleva','Crop-Type'])

        #gets workspace.
        ws = Workspace.from_config()
        #USER must type their experiment name in dictionary key.
        dictExperiments = ws.experiments

        myExperiment = dictExperiments[experimentName]
        #prints off experiment name (For Testing).
        print(myExperiment)
        #get runs in experiment
        myRuns = myExperiment.get_runs()
        #Arbitrary high number
        lowestNormedRootError = 100
        #This variable will store the runID of the lowest run
        lowestKey = ""
        #outer loop iterates through parent runs (theoretically, there should only be one), and inner loop iterates through child runs. Then, checks the
        #the value of the primary metric and compares it with the lowest metric thus far.
        for run in myRuns:
                metrics = run.get_metrics(recursive = True)
                for key, mets in metrics.items():
                        if mets[primaryMetric] < lowestNormedRootError:
                                lowestKey = key
        #After finding the lowest child run, we find the child run to deploy its model.
        print(str(lowestKey))
        myRuns = myExperiment.get_runs()
        run = next(myRuns)
        children = run.get_children()
        bestChild = None
        foundChild = False
        for child in children:
                if child.id == lowestKey:
                        bestChild = child
                        foundChild = True
                        break
        print("Found child: " + str(foundChild))
        print("Deploying Model....")
        #Predict normalized yield using the best-scored model. 
        bestRun, fittedModel = bestChild.get_output()
        y_predict = fittedModel.predict(X_toTest.values)


        with open(predicted_values_folder + "//" + "predictions" , mode='w') as csv_file:
                filewriter = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['ID', 'Normed_Dry_Yld_Vol'])
                index = 0
                #We must associate each grid square with an output.
                columnIDs = X_toTest["Column1"]
                for gridBox in y_predict:
                        filewriter.writerow([str(next(columnIDs)), str(gridBox)])
                        index = index + 1

    


        
   
        

