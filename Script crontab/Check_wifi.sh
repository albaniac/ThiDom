#!/bin/bash

IP=`ifconfig wlan0 | grep 'inet '  | tr -d [:alpha:] | tr -s [:space:] | cut -d: -f2`
IP_fixe='192.168.1.25'

if [ $IP == ' ' ]; 
	then echo "not exist";
	else
	if [ $(cat /sys/class/net/wlan0/carrier) == 0 ] || [ $IP != $IP_fixe ];
		then 	
			 sudo /etc/init.d/networking restart &&  touch /var/www/nodejs/public_html/cronNode.txt &&
			 strDate=$(date) && strAct=" Relance wlan0" &&
			 echo $strDate $strAct $IP  " //  "  $IP_fixe >> /var/www/nodejs/public_html/cronNode.txt ;
		 fi;
	fi;