#!/bin/bash

########## SUPPRIME LES BACKUPS SUPERIEUR à 3 JOURS  ###############

#NOW=$(date +"%d_%m_%Y")
#FILE="/home/pi/backup_bdd_$NOW.sql"

#mysqldump thidom > $FILE

#find /home/pi/backup_bdd_* -mtime +2 -exec rm -rf {} \;

python /home/pi/Script_domotique/backup_bdd.py  >> /home/pi/Script\ crontab/debug/console.log 2>&1 &