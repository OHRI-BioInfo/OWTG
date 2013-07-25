import ownet

ownet.init('localhost:4304')

dFile = open('/etc/owfs-etm/discovered','r+')
dAddresses = []

lineList = dFile.readlines()
for line in lineList:
    dAddresses.append(line.split(':')[0])

for directory in ownet.Sensor('/','localhost',4304).sensorList():
    address = None
    if(directory == ownet.Sensor('/simultaneous','localhost',4304)):
        continue
    if hasattr(directory,'temperature'):
        address = directory.address
    
