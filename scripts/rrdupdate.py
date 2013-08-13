import time
import ownet
import rrdtool
from owtg import *

ownet.init('localhost:4304')

currentTime = time.localtime()
currentHalfMinute = 0
if int(currentTime.tm_sec-30) < 0: 
    currentHalfMinute = int(time.mktime(currentTime)-currentTime.tm_sec)
else:
    currentHalfMinute = int(time.mktime(currentTime)-(currentTime.tm_sec-30))

gSensors = [s for s in getSensors() if s.graph == True] #Sensors to graph
sensorTemps = [] #Array of tuples in this format: ([address],[temperature])

for s in gSensors:
    sensorTemps.append((s.address,str(ownet.Sensor('/'+s.address,'localhost',4304).temperature)))
    
template = ''
for sensor in sensorTemps:
    template += sensor[0]+':'
template = template.rstrip(':')

values = str(currentHalfMinute)+':'
for sensor in sensorTemps:
    values += sensor[1]+':'
values = values.rstrip(':')

rrdtool.update(adbFilename,'-t',template,values)
rrdtool.update(gdbFilename,'-t',template,values)
