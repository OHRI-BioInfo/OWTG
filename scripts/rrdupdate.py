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

gAddresses = getSensors(True) #Addresses to graph
sensorTemps = [] #Array of tuples in this format: ([address],[temperature])

for a in gAddresses:
    sensorTemps.append((a,str(ownet.Sensor('/'+a,'localhost',4304).temperature)))
    
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
