#---------------------------------------------------------------------------------------
#
#       Name: Eng. William da Rosa Frohlich
#
#       Project: ATHENA I - Online Mode
#
#       Date: 2021.10.16
#
#       Update: 2021.10.17
#
#---------------------------------------------------------------------------------------

from prediction import PredictionOnline


class OnlineMode():
    def __init__(self):
        pass


    def run(self):
        predict = PredictionOnline()
        predict.training()


if __name__=='__main__':
    online_mode = OnlineMode()
    online_mode.run()
