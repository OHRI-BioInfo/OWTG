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
#For correct operation this MUST be a multiple of 60 (as cron only operates in minutes)
#and must be equal to the interval in minutes that cron runs the update script.
#60 (one minute) is the minimum, and will give you maximum resolution.
#You should not need to change this value.
#Default: 30
step = 30

#Change this to True if you want to suppress backup creation (not recommended)
#Default: False
noBackup = False

#The width, in pixels, of the canvas of the graphs that will be generated with this RRD.
#If you change this, you must change width in rrdgraph.py to the same value.
#Default: 400
width = 400

#END

dbFilenames = [adbFilename,gdbFilename]

lockFile = open(etcDir+'allowRun','w+')
lockFile.write('0')
lockFile.close()

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

for dbFilename in dbFilenames:
    if os.path.exists(dbFilename):
        print('The database ' + dbFilename + ' already exists. If you continue, it will be overwritten. ')
        if not noBackup:
            print('A backup will be made (this will erase any existing backup).')
        else:
            print('A backup will not be made and you WILL lose data.')
        #Input verification loop
        while True:
            choice = raw_input('\nDo you want to continue (yes/no)? ')
            if choice == 'no':
                exit(0)
            elif choice != 'yes':
                print('Invalid choice. Please try again.')
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

lockFile = open('/opt/owtg/etc/allowRun','w+')
lockFile.write('1')
lockFile.close()
