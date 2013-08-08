#!/bin/bash
#This should be called in crontab like this:
#* * * * * bash /opt/owtg/bin/minute.sh
if [ "$(</opt/owtg/etc/allowRun)" = "1" ]; then
    python /opt/owtg/bin/detect_sensors.py;
    python /opt/owtg/bin/rrdupdate.py;
    sleep 30;
    python /opt/owtg/bin/rrdupdate.py;
fi
