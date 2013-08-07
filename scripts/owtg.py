sFilename = '/opt/owtg/etc/sensors'
adbFilename = '/opt/owtg/etc/archive.rrd'
gdbFilename = '/opt/owtg/etc/graphing.rrd'

def getSensors(graphOnly=False):
    dAddresses = [] #already discovered addresses
    gAddresses = [] #Addresses with "graph" turned on
    
    sFile = open(sFilename,'r') #discovered file, open for reading
    lineList = sFile.readlines()
    sFile.close()

    for line in lineList:
        #ignore comments (lines beginning with #)
        if line.startswith('#'):
            continue
        if line:
            line = line.rstrip('\n')
            dAddresses.append(line.split(':')[1])
            if line.split(':')[3] == 'y':
                gAddresses.append(line.split(':')[1])
    if graphOnly:
        return gAddresses
    return dAddresses
