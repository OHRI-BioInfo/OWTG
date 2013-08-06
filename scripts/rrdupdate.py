import time
import ownet
import rrdtool
from owtg import *

ownet.init('localhost:4304')

currentTime = time.localtime()
currentMinute = int(time.mktime(currentTime)-currentTime.tm_sec)

gAddresses = getSensors(True) #Addresses to graph
sensorTemps = [] #Array of tuples in this format: ([address],[temperature])

for a in gAddresses:
    sensorTemps.append((a,str(ownet.Sensor('/'+a,'localhost',4304).temperature)))
    
template = ''
for sensor in sensorTemps:
    template += sensor[0]+':'
template = template.rstrip(':')

values = str(currentMinute)+':'
for sensor in sensorTemps:
    values += sensor[1]+':'
values = values.rstrip(':')

rrdtool.update(dbFilename,'-t',template,values)
