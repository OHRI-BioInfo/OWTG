from owtg import etcDir
import xml.etree.ElementTree as ET
import sys

#lockFile = open(etcDir+'allowRun','w+')
#lockFile.write('0')
#lockFile.close()

#tree = ET.parse(etcDir+'temp.xml')
tree = ET.parse('/home/john/rrdtest/graphing.xml')
names = [ds.find('name').text.strip() for ds in tree.findall('ds')]

if len(sys.argv) < 3:
    print "Syntax:"
    print "python rrdmod.py add [number]"
    print "python rrdmod.py remove [address]"

command = sys.argv[1].lower() #Command argument
address = sys.argv[2].upper() #Address argument

def remove(address):
    addressIndex = None
    for i,name in enumerate(names):
        if name == address:
            addressIndex = i
    #Reset the ds section for this sensor to defaults
    dsElement = tree.findall('ds')[addressIndex]
    dsElement.find('name').text = ' unclaimed_'+str(addressIndex)+' '
    dsElement.find('last_ds').text = 'U'
    dsElement.find('value').text = 'NaN'
    dsElement.find('unknown_sec').text = ' 0 '
    
    for rra in tree.findall('rra'):
        dsElement = rra.find('cdp_prep').findall('ds')[addressIndex]
        dsElement.find('primary_value').text = 'NaN'
        dsElement.find('secondary_value').text = 'NaN'
        dsElement.find('value').text = 'NaN'
        dsElement.find('unknown_datapoints').text = '0'
        
        dbElement = rra.find('database')
        for row in dbElement.findall('row'):
            row.findall('v')[addressIndex].text = 'NaN'
            
if command == 'add':
    print "Not implemented"
elif command == 'remove':
    remove(address)
    if address.split('_')[0] == 'unclaimed':
        print "There's no point in trying to remove an unclaimed address."
        exit(0)
else:
    print "Syntax:"
    print "python rrdmod.py add [number]"
    print "python rrdmod.py remove [address]"

tree.write('/home/john/rrdtest/newgraphing.xml')
