#!/usr/bin/python
#   Copyright (C) 2013 OHRI 
#
#   This file is part of OWTG.
#
#   OWTG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   OWTG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with OWTG.  If not, see <http://www.gnu.org/licenses/>.

import time
import ownet
import rrdtool
from owtg import *

if datGet('allowRun') != '1':
    exit(0)

if not dbExists():
    exit(1)
ownet.init('localhost:4304')
newFile = [] #Array of lines to write out to file
newFile.append(sFileTop) #Add comments to top of file

sensorArray = getSensors()

for s in sensorArray:
    curTemp = float(ownet.Sensor('/'+s.address,'localhost',4304).temperature)
    #If the temperature has crossed the maximum alarm threshold
    if s.lastTemp < s.maxAlarm and curTemp > s.maxAlarm:
        print "high alarm"
        #send email
    if s.lastTemp > s.minAlarm and curTemp < s.minAlarm:
        print "low alarm"
        #send email
    s.lastTemp = curTemp
    #[alias]:[address]:[timestamp]:[graph(y/n)]:[min-alarm]:[max-alarm]:[lasttemp]\n
    if s.graph == True:
        graphStr = 'y'
    else:
        graphStr = 'n'
    newFile.append(s.alias+':'+s.address+':'+s.timestamp+':'+graphStr+':'+str(s.minAlarm)+':'+str(s.maxAlarm)+':'+str(s.lastTemp)+'\n')

sFile = open(sFilename,'w') #sensors file, open for writing
sFile.writelines(newFile)
sFile.close()

currentTime = time.localtime()
currentHalfMinute = 0
if int(currentTime.tm_sec-30) < 0: 
    currentHalfMinute = int(time.mktime(currentTime)-currentTime.tm_sec)
else:
    currentHalfMinute = int(time.mktime(currentTime)-(currentTime.tm_sec-30))

gSensors = [s for s in sensorArray if s.graph == True] #Sensors to graph
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
