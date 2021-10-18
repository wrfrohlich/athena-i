# ATHENA I

## 0 - Prepare the System

`sudo su`

`passwd`

`sed -i.bkp 's|#PermitRootLogin prohibit-password|PermitRootLogin yes|i' /etc/ssh/sshd_config`



## 1 - Startup Commands:

### 1.1 - Install:

- Install system:

`sudo bash athena-i/build.sh`

or

`unzip athena-i.zip && rm -rf athena-i.zip && sudo bash athena-i/build.sh`


### 1.2 - Bluetooth:

`sudo bluetoothctl`

- `scan on`
  
- `pair xx:xx:xx:xx:xx:xx`


### 1.3 - Crontab:

`crontab -e`

- `1`
	
- `#crontab`



## 3 - Useful Commands:

### 3.1 - Basic Commands:

- Access database:

`sqlite3 /var/log/athena-i/athena-i.db`

- Start Manually the **Processing**

`sudo python3 /etc/athena-i/models/receive.py`


### 3.1 - Advanced Commands:

- Remove ATHENA I:

`sudo bash /etc/athena-i/remove.sh`

- Remove database

`rm -rf /var/log/athena-i/athena-i.db`