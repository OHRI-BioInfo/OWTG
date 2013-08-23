#!/bin/bash
#This should be called in crontab like this:
#* * * * * bash /opt/owtg/bin/minute.sh
#Use the sleep function to help you use intervals other than
#whole minutes
python /opt/owtg/bin/detect_sensors.py;
python /opt/owtg/bin/rrdupdate.py;
sleep 30;
python /opt/owtg/bin/rrdupdate.py;
