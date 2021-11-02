#---------------------------------------------------------------------------------------
#
#       Name: Eng. William da Rosa Frohlich
#
#       Project: ATHENA I - Prediction
#
#       Date: 2021.10.16
#
#       Update: 2021.10.17
#
#---------------------------------------------------------------------------------------

import sys
import math
import numpy as np
import pandas as pd
import pickle as pickle

from log import Logs
from sklearn.tree import DecisionTreeClassifier

SERVICE = "prediction"


class PredictionOnline():
    def __init__(self):
        self.model_file = "/etc/athena-i/prediction/model.sav"


    def training(self):
        x_train = pd.read_csv("/etc/athena-i/training/train-x", delimiter=';')
        x_train = x_train.to_numpy()

        y_train = pd.read_csv("/etc/athena-i/training/train-y", delimiter=';')
        y_train = y_train.to_numpy()

        model=DecisionTreeClassifier()
        sys.stdout.write("Training...\n")
        try:
            model.fit(x_train, y_train)
            sys.stdout.write("Training: SUCCESS\n")
            self.export_model(model)
        except:
            sys.stdout.write("Training: FAILED\n")



    def export_model(self, model):
        log = Logs()
        try:
            pickle.dump(model, open(self.model_file, 'wb'))
            sys.stdout.write("Export: SUCCESS\n")
            log.log_out(SERVICE, "exported", "INFO")
        except TypeError:
            sys.stdout.write("Export: FAILED\n")
            log.log_out(SERVICE, "exported - FAILED", "WARNING")


    def test_load(self):
        log = Logs()
        try:
            model = pickle.load(open(self.model_file,'rb'))
            sys.stdout.write("Load: FAILED\n")
            log.log_out(SERVICE, "loaded", "INFO")
        except TypeError:
            sys.stdout.write("Load: FAILED\n")
            log.log_out(SERVICE, "loaded - FAILED", "WARNING")



class PredictionOffline():
    def __init__(self):
        self.model_file = "/etc/athena-i/prediction/model.sav"


    def load(self, values, participant):
        log = Logs()

        try:
            model = pickle.load(open(self.model_file,'rb'))
            log.log_out(SERVICE, "loaded", "INFO")
        except TypeError:
            log.log_out(SERVICE, "loaded - FAILED", "INFO")

        predicted = model.predict(values)
        Logs.alert(predicted, participant)
