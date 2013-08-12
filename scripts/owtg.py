sFilename = '/opt/owtg/etc/sensors'
adbFilename = '/opt/owtg/etc/archive.rrd'
gdbFilename = '/opt/owtg/etc/graphing.rrd'

def getLines(filename):
    file_ = open(filename,'r') #Open file for reading
    lineList = file_.readlines()
    lineList_ = []
    file_.close()
    
    #Ignore comments (lines beginning with #)
    for line in lineList:
        if line.startswith('#'):
            continue
        if line:
            #Strip newlines
            line = line.rstrip('\n')
            lineList_.append(line)
    return lineList_            

def getSensors(graphOnly=False):
    dAddresses = [] #already discovered addresses
    gAddresses = [] #Addresses with "graph" turned on
    
    lineList = getLines(sFile)

    for line in lineList:
        if line:
            dAddresses.append(line.split(':')[1])
            if line.split(':')[3] == 'y':
                gAddresses.append(line.split(':')[1])
    if graphOnly:
        return gAddresses
    return dAddresses
    
def getAlias(address):
    lineList = getLines(sFile)
    
    for line in lineList:
        if line:
            if line.split(':')[1] == address:
                return line.split(':')[0]
