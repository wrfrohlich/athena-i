#---------------------------------------------------------------------------------------
#
#       Name: Eng. William da Rosa Frohlich
#
#       Project: ATHENA I - Builder
#
#       Date: 2021.04.19
#
#       Update: 2021.10.17
#
#---------------------------------------------------------------------------------------

#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#!/bin/sh
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
sed -i.bkp 's|#PermitRootLogin prohibit-password|PermitRootLogin yes|i' /etc/ssh/sshd_config
#----------------------------------------------------
#////////// Variables ///////////////////////////////
#----------------------------------------------------
DIR_ETC=/etc/athena-i
DIR_ROOT=/root/athena-i
DIR_API=/etc/athena-i/api/
DIR_NGINX=/etc/athena-i/nginx/
DIR_PRED=/etc/athena-i/prediction/
DIR_ACQUISITION=/etc/athena-i/acquisition/
DIR_MODELS=/etc/athena-i/models/
#----------------------------------------------------
API_LOG=/api.log
API_FILE=api.py
#----------------------------------------------------
PROCESSING_LOG=/manager.log
PROCESSING_FILE=manager.py
#----------------------------------------------------
ACQUISITION_FILE=acquisition
#----------------------------------------------------
NGINX_ZIP=nginx_html.zip
NGINX_DEFAULT=default.conf
NGINX_INDEX=index.nginx-debian.html
DIR_NGINX_HTML=/var/www/html/
DIR_NGINX_DEFAULT=/etc/nginx/conf.d/
#----------------------------------------------------
RAW=/raw
ALERTS=/alerts
REPORT=athena-i
DIR_LOG=/var/log/
#----------------------------------------------------
sudo mv $DIR_ROOT $DIR_ETC
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#////////// Create Directories //////////////////////
#----------------------------------------------------
if [ -e "$DIR_LOG$REPORT" ]; then
	echo "Paths exist"
else
	sudo mkdir "$DIR_LOG$REPORT" "$DIR_LOG$REPORT$RAW" "$DIR_LOG$REPORT$ALERTS" "$DIR_PRED"
	echo -e "$DIR_LOG$REPORT: created\n$DIR_PRED: created"
fi
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#////////// Update System ///////////////////////////
#----------------------------------------------------
sudo apt update -y
sudo apt upgrade -y
#----------------------------------------------------
sudo apt-get install libbluetooth-dev -y
sudo apt-get install pi-bluetooth -y
sudo apt-get install python-dev -y
sudo apt-get install libatlas-base-dev -y
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#////////// Install and Configure Postgres //////////
#----------------------------------------------------
sudo apt-get install sqlite3 -y
cat /etc/athena-i/database/init.sql | sqlite3 /var/log/athena-i/athena-i.db
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#////////// Install API and Dependencies ////////////
#----------------------------------------------------
pip3 install bottle
crontab -l|sed "\$a@reboot sudo python3 $DIR_API$API_FILE &"|crontab -
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#////////// Install Processing and Dependencies /////
#----------------------------------------------------
pip3 install pandas
pip3 install numpy
pip3 install biosppy
pip3 install db-sqlite3
crontab -l|sed "\$a@reboot sudo python3 $DIR_MODELS$PROCESSING_FILE &"|crontab -
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#////////// Install and Configure Ngnix /////////////
#----------------------------------------------------
sudo apt-get install nginx -y
#----------------------------------------------------
rm -rf $DIR_NGINX_HTML$NGINX_INDEX
cp $DIR_NGINX$NGINX_ZIP $DIR_NGINX_HTML
cd $DIR_NGINX_HTML && unzip -o $NGINX_ZIP && rm -rf $NGINX_ZIP && cd
cp $DIR_NGINX$NGINX_DEFAULT $DIR_NGINX_DEFAULT$NGINX_DEFAULT
sudo /etc/init.d/nginx start
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
#////////// Create Acquisition File /////////////////
#----------------------------------------------------
if [ -e "$DIR_ACQUISITION$ACQUISITION_FILE" ]; then
	echo "acquisition: already exists"
else
	cd $DIR_ACQUISITION && sudo make
	echo "acquisition: created"
fi
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
sudo reboot now
#----------------------------------------------------
#////////////////////////////////////////////////////
#----------------------------------------------------
