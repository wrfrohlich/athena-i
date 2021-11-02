#---------------------------------------------------------------------------------------
#
#       Name: Eng. William da Rosa Frohlich
#
#       Project: ATHENA I - Manager
#
#       Date: 2021.04.19
#
#       Update: 2021.10.17
#
#---------------------------------------------------------------------------------------

import socket
import datetime
import subprocess
import pandas as pd

from log import Logs
from database import Database as db
from processing import Processing as process
from prediction import PredictionOffline

SERVICE = "manager"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address =('', 18000)
sock.bind(address)


class Manager():

    def __init__(self):
        pass


    def run(self):
        log = Logs()
        log.log_out(SERVICE, "started", "INFO")

        self.reset_bluetooth()

        acquisition = False
        name = "None"
        surname = "None"
        time = "None"

        while True:
            try:
                packet, addr = sock.recvfrom(1024)
                packet = (str(packet))
                size = len(packet)
                data = packet[2:(size-1)]
                data = data.split(';')

                if (data[0] == "START" and acquisition == False):
                    log.log_out("acquisition", "started", "INFO")
                    name = str(data[1])
                    surname = str(data[2])
                    if (name == "" and surname == ""):
                        log.log_out(SERVICE, "shutting down", "INFO")
                        subprocess.Popen(   "sudo shutdown now",
                                            shell=True,
                                            close_fds=True)
                    else:
                        cmd = "sudo /etc/athena-i/"
                        cmd += "acquisition/acquisition %s %s" % (  name,
                                                                    surname)
                        cmd += " > /var/log/athena-i/acquisition.log &"
                        subprocess.Popen(cmd,
                                        shell=True,
                                        close_fds=True)
                        acquisition = True

                elif (data[0] == "READ"):
                    log.log_out(SERVICE, "read file", "INFO")
                    time = str(data[1])
                    values, enough= self.read(name, surname, time)
                    if enough:
                        predict = PredictionOffline()
                        predict.load(values, "%s_%s" % (name, surname))

                elif (data[0] == "STOP"):
                    log.log_out("acquisition", "stopped", "INFO")
                    time = str(data[1])
                    acquisition = False
                    self.reset_bluetooth()
                    self.read(name, surname, time)

            except KeyboardInterrupt:
                
                sock.close()
                self.reset_bluetooth()
                break


    def read(self, name, surname, time):
        log = Logs()
        data_processing = db.save_file(name, surname, time)
        if not (data_processing.empty):
            db.database_raw_data (data_processing)

            ecg, eda, rsp = process.main_processing(data_processing)

            if len(ecg) != 0:
                process.heart_rate_process(data_processing, ecg)
                process.ecg_process(data_processing, ecg)
                first_test = len(ecg['filtered']) >= 55000
            else:
                first_test = False

            if len(eda) != 0:
                process.eda_process(data_processing, eda)
                second_test = len(eda['filtered']) >= 55000
            else:
                second_test = False
                
            if len(rsp) != 0:
                process.rsp_process(data_processing, rsp)
                third_test = len(rsp['filtered']) >= 55000
            else:
                third_test = False


            if first_test and second_test and third_test:
                return process.data_format(ecg, eda, rsp), True

        return None, False


    def reset_bluetooth(self):
        log = Logs()
        try:
            subprocess.Popen(   "sudo systemctl restart bluetooth -f",
                                shell=True,
                                close_fds=True)
            subprocess.Popen(   "sudo hciconfig hci0 reset",
                                shell=True,
                                close_fds=True)
        except:
            log.log_out("bluetooth", "failed to restart", "INFO")


if __name__=='__main__':
    manager = Manager()
    manager.run()