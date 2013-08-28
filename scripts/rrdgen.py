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

import rrdtool
import os
import time
from owtg import adbFilename, gdbFilename, etcDir
from math import ceil
import shutil

#BEGIN - You may change these values

#The number of initial data sources (sensors) to define in the RRD file. This should be
#large enough to store each sensor you expect to monitor with OWTG. More data sources
#can be added later via the web interface.
#Default: 20
initialDSCount = 20

#The time, in years, to keep data. Note that only the last year of data will be graphed
#automatically, but it is possible to manually request graphs of any time period that
#you have data for via the web interface.
#Default: 1
years = 1

#The interval, in seconds, that the RRD file will be updated with values.
#30 (30 seconds) is the minimum, and will give you maximum resolution.
#A <1 minute step is achieved with a sleep function in minute.sh; if you change this step
#then use that function as well as cron to make sure the timings are matched up with this value
#You should not need to change this value.
#Default: 30
step = 30

#Change this to True if you want to suppress backup creation (not recommended)
#Default: False
noBackup = False

#The width, in pixels, of the canvas of the graphs that will be generated with this RRD.
#Default: 400
width = 400

#END

dbFilenames = [adbFilename,gdbFilename]

datSet('allowRun','0')
datSet('width',str(width))

if step<30:
    print('ERROR: Step cannot be less than 30')
    exit(0)

if step%30 != 0:
    print('!!WARNING!! Step is not a multiple of 30. This may cause undesired behaviour.')

currentTime = time.localtime()
currentMinute = int(time.mktime(currentTime)-currentTime.tm_sec)

def createDB(dbType):
    global math
    dbFilename = ''
    
    minutes = round(step/60.0,1) #Minutes represented by the step which is in seconds
    hourSteps = 1
    hourRows = ceil(60/minutes)
    hoursSteps = 1
    hoursRows = ceil(180/minutes)
    daySteps = ceil(1440.0/width/minutes) #1440 - number of minutes in a 24-hour day (24h*60m)
    dayRows = ceil(1440.0/(1440.0/width))
    weekSteps = ceil(10080.0/width/minutes) #10080 - number of minutes in a 7-day week of 24-hour days (7d*24h*60m)
    weekRows = ceil(10080.0/(10080.0/width))
    monthSteps = ceil(44640.0/width/minutes) #44640 - number of minutes in a 31-day month of 24-hour days (31d*24h*60m)
    monthRows = ceil(44640.0/(44640.0/width))
    yearSteps = ceil(525949.0/width/minutes) #525949 - approx number of minutes in an averaged 365.2425-day year (Google)
    yearRows = ceil(525949.0/(525949.0/width))
    archiveSteps = 1
    archiveRows = ceil(525949.0*(1/minutes)*years)
    dataSources = []
    RRAString = 'RRA:AVERAGE:0.5:'
    if dbType == 'archive':
        archives = [RRAString+str(archiveSteps)+':'+str(archiveRows)]
        dbFilename = adbFilename
    elif dbType == 'graphing':
        archives = [RRAString+str(hourSteps)+':'+str(hourRows),
                    RRAString+str(hoursSteps)+':'+str(hoursRows),
                    RRAString+str(daySteps)+':'+str(dayRows),
                    RRAString+str(weekSteps)+':'+str(weekRows),
                    RRAString+str(monthSteps)+':'+str(monthRows),
                    RRAString+str(yearSteps)+':'+str(yearRows)]
        dbFilename = gdbFilename
                
    for i in range(0,initialDSCount):
        dataSources.append('DS:unclaimed_'+str(i)+':GAUGE:'+str(step)+':U:U')
    
    rrdtool.create(dbFilename, 
                    '--step', str(step),
                    dataSources, archives,
                    '--start',str(currentMinute))

choice = 'null'

for dbFilename in dbFilenames:
    if os.path.exists(dbFilename):
        print('The database file(s) already exist. If you continue, it will be overwritten. ')
        if not noBackup:
            print('A backup will be made (this will erase any existing backup).')
        else:
            print('A backup will not be made and you WILL lose data.')
        #Input verification loop
        while True:
            if choice == 'null':    
                #Only ask for a choice if it hasn't been made already for another file
                #This ensures that either both files will be created, or neither will be
                choice = raw_input('\nDo you want to continue (yes/no)? ')
            if choice == 'no':
                exit(0)
            elif choice != 'yes':
                print('Invalid choice. Please try again.')
                choice = 'null'
                continue
            break
        if not noBackup:
            shutil.copy2(dbFilename,dbFilename+'~')
            os.chmod(dbFilename+'~',0666)
            
    if dbFilename == adbFilename:
        createDB('archive')
    elif dbFilename == gdbFilename:
        createDB('graphing')
    os.chmod(dbFilename,0666)

datSet('allowRun','1')
