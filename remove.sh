#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#!/bin/sh
#----------------------------------------------------
#////////// Variables ///////////////////////////////
#----------------------------------------------------
LOG=raspbit.log
REPORT=raspbit
DIR_LOG=/var/log/
DIR_ETC=/etc/raspbit
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
sudo rm -rf $DIR_ETC $DIR_LOG$LOG $DIR_LOG$REPORT
#----------------------------------------------------
crontab -l|sed 's|@reboot sudo python3 /etc/raspbit/api/api.py >> /var/log/raspbit.log/api.log &||i'|crontab -
#----------------------------------------------------
crontab -l|sed 's|@reboot sudo python3 /etc/raspbit/models/receive.py >> /var/log/raspbit.log/receive.log &||i'|crontab -
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
sudo reboot now
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------