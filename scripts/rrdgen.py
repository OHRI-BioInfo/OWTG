import rrdtool
import os.path
from owtg import dbFilename
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
#Default: 60
step = 60

#Change this to True if you want to suppress backup creation (not recommended)
#Default: False
noBackup = False;

#END

if step<60:
    print('ERROR: Step cannot be less than 60')
    exit(0)

if step%60 != 0:
    print('!!WARNING!! Step is not a multiple of 60. This may cause undesired behaviour.')

def createDB():
    global math
    
    minutes = int(round(step/60.0)) #Minutes represented by the step which is in seconds
    daySteps = 4*minutes
    dayRows = ceil(1440/daySteps) #1440 - number of minutes in a 24-hour day (24h*60m)
    weekSteps = 30*minutes
    weekRows = ceil(10080/weekSteps) #10080 - number of minutes in a 7-day week of 24-hour days (7d*24h*60m)
    monthSteps = 120*minutes
    monthRows = ceil(44640/monthSteps) #44640 - number of minutes in a 31-day month of 24-hour days (31d*24h*60m)
    yearSteps = 1440*minutes
    yearRows = ceil(525949/yearSteps) #525949 - approx number of minutes in an averaged 365.2425-day year (Google)
    archiveSteps = 1*minutes
    archiveRows = ceil(525949*years/archiveSteps)
    dataSources = []
    RRAString = 'RRA:AVERAGE:0.5:'
    archives = [RRAString+str(daySteps)+':'+str(dayRows),
                RRAString+str(weekSteps)+':'+str(weekRows),
                RRAString+str(monthSteps)+':'+str(monthRows),
                RRAString+str(yearSteps)+':'+str(dayRows),
                RRAString+str(archiveSteps)+':'+str(archiveRows)]
                
    for i in range(0,initialDSCount):
        dataSources.append('DS:unclaimed_'+str(i)+':GAUGE:'+str(step)+':U:U')
    
    rrdtool.create(dbFilename, 
                    '--step', str(step),
                    dataSources, archives)
                
if os.path.exists(dbFilename):
    print('The database already exists. If you continue, it will be overwritten. ')
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

createDB()
