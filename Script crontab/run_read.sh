#!/bin/bash
# > /dev/ttyUSB1

#sudo service ntp stop
#sudo ntpd -q -g
#sudo service ntp start
#sudo sntp -s 24.56.178.140
sudo sntp -s 0.fr.pool.ntp.org

sudo /home/pi/Script\ crontab/kill_read.sh
python -u /home/pi/Script_domotique/read_usb.py >> /home/pi/Script\ crontab/debug/console.log 2>&1 &
