#---------------------------------------------------------------------------------------
#
#       Name: Eng. William da Rosa Frohlich
#
#       Project: ATHENA I - Database
#
#       Date: 2021.04.19
#
#       Update: 2021.10.17
#
#---------------------------------------------------------------------------------------

import sqlite3
import os.path
import logging
import numpy as np
import pandas as pd

from log import Logs

SERVICE = "database"

class Database():
    def save_file(name, surname, time):
        log = Logs()

        file = "/var/log/athena-i/raw/" + name + "_" + surname + "_" + time + ".txt"
        data_processing = pd.DataFrame(columns =['NAME',
                                                'SURNAME',
                                                'ECG',
                                                'EDA',
                                                'RSP',
                                                'TIME'])

        if (os.path.isfile(file)):
            data_processing = pd.read_csv(file, delimiter=';')
            name_file = ("/var/log/athena-i/" + name + "_" + surname + ".csv")

            if not (os.path.isfile(name_file)):
                data_processing.to_csv( name_file,
                                        mode='w',
                                        index=None,
                                        header=True,
                                        sep=';',
                                        encoding='utf-8')
                log.log_out(SERVICE, "%s_%s.csv created" % (name, surname), "INFO")

            else:
                data_processing.to_csv( name_file,
                                        mode='a',
                                        index=None,
                                        header=False,
                                        sep=';',
                                        encoding='utf-8')
                log.log_out(SERVICE, "%s_%s.csv saved" % (name, surname), "INFO")

        if (data_processing.empty):
            log.log_out(SERVICE, "raw - no data", "WARNING")

        return data_processing


    def database_raw_data (data_processing):
        log = Logs()
        con = sqlite3.connect('/var/log/athena-i/athena-i.db')
        cur = con.cursor()
        command = "CREATE TABLE IF NOT EXISTS raw_data "
        command += "(NAME TEXT, SURNAME TEXT, ECG REAL, "
        command += "EDA REAL, RSP REAL, TIME TEXT)"
        cur.execute(command)
        data_processing.to_sql( name = 'raw_data',
                                con = con,
                                if_exists = 'append',
                                index = False)
        con.commit()
        con.close()
        log.log_out(SERVICE, "raw_data saved", "INFO")


    def database_heart_rate (data_processing):
        log = Logs()
        con = sqlite3.connect('/var/log/athena-i/athena-i.db')
        cur = con.cursor()
        command = "CREATE TABLE IF NOT EXISTS heart_rate "
        command += "(NAME TEXT, SURNAME TEXT, HEART_RATE REAL, HEART_RATE_TS REAL)"
        cur.execute(command)
        data_processing.to_sql( name = 'heart_rate',
                                con = con,
                                if_exists = 'append',
                                index = False)
        con.commit()
        con.close()
        log.log_out(SERVICE, "heart rate saved", "INFO")


    def database_ecg (data_processing):
        log = Logs()
        con = sqlite3.connect('/var/log/athena-i/athena-i.db')
        cur = con.cursor()
        command = "CREATE TABLE IF NOT EXISTS ecg "
        command += "(NAME TEXT, SURNAME TEXT, ECG REAL, ECG_TS REAL)"
        cur.execute(command)
        data_processing.to_sql( name = 'ecg',
                                con = con,
                                if_exists = 'append',
                                index = False)
        con.commit()
        con.close()
        log.log_out(SERVICE, "ecg saved", "INFO")


    def database_eda (data_processing):
        log = Logs()
        con = sqlite3.connect('/var/log/athena-i/athena-i.db')
        cur = con.cursor()
        command = "CREATE TABLE IF NOT EXISTS eda "
        command += "(NAME TEXT, SURNAME TEXT, EDA REAL, EDA_TS REAL)"
        cur.execute(command)
        data_processing.to_sql( name = 'eda',
                                con = con,
                                if_exists = 'append',
                                index = False)
        con.commit()
        con.close()
        log.log_out(SERVICE, "eda saved", "INFO")


    def database_rsp (data_processing):
        log = Logs()
        con = sqlite3.connect('/var/log/athena-i/athena-i.db')
        cur = con.cursor()
        command = "CREATE TABLE IF NOT EXISTS rsp "
        command += "(NAME TEXT, SURNAME TEXT, RSP REAL, RSP_TS REAL)"
        cur.execute(command)
        data_processing.to_sql( name = 'rsp',
                                con = con,
                                if_exists = 'append',
                                index = False)
        con.commit()
        con.close()
        log.log_out(SERVICE, "rsp saved", "INFO")