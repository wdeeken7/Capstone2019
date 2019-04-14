from azureml.core import Workspace
import azureml.train
import azureml.dataprep as dprep
from azureml.train.automl import *
from logging import *
#### This doc defines the bare model. Parameters are passed to it and it returns a mlConfig object. ####
def model(x_train, y_train, logFolder, iterationTimeoutMinutes, iterationsToDo, primaryMetric, nCrossValidations, modelType):
    automl_settings = {
        "iteration_timeout_minutes" : iterationTimeoutMinutes,
        "iterations" : iterationsToDo,
        "primary_metric" : primaryMetric,
        "preprocess" : True,
        "verbosity" : 20,
        "n_cross_validations": nCrossValidations
    }
    automated_ml_config = AutoMLConfig(task = modelType,
                                debug_log = 'automated_ml_errors.log',
                                path = logFolder,
                                X = x_train.values,
                                y = y_train.values.flatten(),
                                **automl_settings)
    return automated_ml_config



