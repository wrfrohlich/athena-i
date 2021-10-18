#---------------------------------------------------------------------------------------
#
#       Name: Eng. William da Rosa Frohlich
#
#       Project: ATHENA I - Processing
#
#       Date: 2021.04.19
#
#       Update: 2021.10.17
#
#---------------------------------------------------------------------------------------

import math
import logging
import numpy as np
import pandas as pd
from biosppy import signals as bio_signals

from log import Logs
from database import Database as db

SERVICE = "processing"

class Processing():

    def main_processing(data_processing):
        log = Logs()
        log.log_out(SERVICE, "started", "INFO")

        try:
            ecg_signal = bio_signals.ecg.ecg(   signal=data_processing['ECG'],
                                                sampling_rate=1000,
                                                show=False)
        except:
            log.log_out(SERVICE, "ECG - without enought data", "ERROR")
            ecg_signal = []

        try:
            eda_signal = bio_signals.eda.eda(   signal=data_processing['EDA'],
                                                sampling_rate=1000,
                                                show=False)
        except:
            log.log_out(SERVICE, "EDA - without enought data", "ERROR")
            eda_signal = []

        try:
            rsp_signal = bio_signals.resp.resp( signal=data_processing['RSP'],
                                                sampling_rate=1000,
                                                show=False)
        except:
            log.log_out(SERVICE, "RSP - without enought data", "ERROR")
            rsp_signal = []

        return ecg_signal, eda_signal, rsp_signal


    def heart_rate_process(data_processing, ecg_signal):
        new_df = pd.DataFrame(columns =['NAME','SURNAME','HEART_RATE','HEART_RATE_TS'])
        
        new_df["HEART_RATE"] = ecg_signal["heart_rate"]
        new_df["HEART_RATE_TS"] = ecg_signal["heart_rate_ts"]

        size = len(ecg_signal["heart_rate"])
        new_df["NAME"] = data_processing["NAME"][0:size]
        new_df["SURNAME"] =  data_processing["SURNAME"][0:size]

        db.database_heart_rate(new_df)


    def ecg_process(data_processing, ecg_signal):
        new_df = pd.DataFrame(columns =['NAME','SURNAME','ECG','ECG_TS'])
        
        new_df["ECG"] = ecg_signal["filtered"]
        new_df["ECG_TS"] = ecg_signal["ts"]

        size = len(ecg_signal["filtered"])
        new_df["NAME"] = data_processing["NAME"][0:size]
        new_df["SURNAME"] =  data_processing["SURNAME"][0:size]

        db.database_ecg(new_df)


    def eda_process(data_processing, eda_signal):
        new_df = pd.DataFrame(columns =['NAME','SURNAME','EDA','EDA_TS'])

        new_df["EDA"] = eda_signal["filtered"]
        new_df["EDA_TS"] = eda_signal["ts"]

        size = len(eda_signal["filtered"])
        new_df["NAME"] = data_processing["NAME"][0:size]
        new_df["SURNAME"] =  data_processing["SURNAME"][0:size]

        db.database_eda(new_df)


    def rsp_process(data_processing, rsp_signal):
        new_df = pd.DataFrame(columns =['NAME','SURNAME','RSP','RSP_TS'])

        new_df["RSP"] = rsp_signal["filtered"]
        new_df["RSP_TS"] = rsp_signal["ts"]

        size = len(rsp_signal["filtered"])
        new_df["NAME"] = data_processing["NAME"][0:size]
        new_df["SURNAME"] =  data_processing["SURNAME"][0:size]

        db.database_rsp(new_df)

    def data_format(ecg_signal, eda_signal, rsp_signal):
        df = pd.DataFrame()

        ecg = pd.DataFrame(ecg_signal["filtered"])
        eda = pd.DataFrame(eda_signal["filtered"])
        rsp = pd.DataFrame(rsp_signal["filtered"])

        df = pd.concat([df, ecg], axis = 1)
        df = pd.concat([df, eda], axis = 1)
        df = pd.concat([df, rsp], axis = 1)

        df = df[15000:45000]

        return np.array(df)