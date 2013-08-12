from owtg import *
import rrdtool

#This is the width of the graph canvas, where the data is displayed.
#It must be the same as the width specified in rrdgen.py *when the RRD files were generated*
#Default: 400
width = 400

#Path to generate the graphs. You should not need to change this unless your webserver
#root is elsewhere.
#Default: /var/www/graphs
graphsPath = '/var/www/graphs/'

gAddresses = getSensors(True)

for address in gAddresses:
    alias = getAlias(address)
    #Not implemented yet:
    #highWaterMark = 0.0
    #lowWaterMark = 0.0
    
    #:::: is a placeholder for time, ::-:: is a placeholder for title
    #Colons are used because the user isn't allowed to enter them in the alias 
    arguments = [graphsPath+address+'-::::'+'.png','--end','now','--start',\
    'end-::::','--title','::-::','--width',str(width),\
    'DEF:'+address+'=/opt/owtg/etc/graphing.rrd:'+address+':AVERAGE',\
    'LINE:'+address+'#1A50BC:'+alias]
    
    arguments = [s.replace('::::','1h') for s in arguments]
    arguments = [s.replace('::-::','Past hour') for s in arguments]
    rrdtool.graph(arguments)
    
    arguments = [s.replace('::::','3h') for s in arguments]
    arguments = [s.replace('::-::','Past 3 hours') for s in arguments]
    rrdtool.graph(arguments)
    
    arguments = [s.replace('::::','1d') for s in arguments]
    arguments = [s.replace('::-::','Past day') for s in arguments]
    rrdtool.graph(arguments)
    
    arguments = [s.replace('::::','1w') for s in arguments]
    arguments = [s.replace('::-::','Past week') for s in arguments]
    rrdtool.graph(arguments)
    
    arguments = [s.replace('::::','1month') for s in arguments]
    arguments = [s.replace('::-::','Past month') for s in arguments]
    rrdtool.graph(arguments)
    
    arguments = [s.replace('::::','1y') for s in arguments]
    arguments = [s.replace('::-::','Past year') for s in arguments]
    rrdtool.graph(arguments)
