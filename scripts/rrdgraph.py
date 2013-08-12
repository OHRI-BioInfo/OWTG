from owtg import *
from string import replace
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

def replaceArguments(arguments,time,title):
    arguments = [replace(s,'::::',time) for s in arguments]
    arguments = [replace(s,'::-::',title) for s in arguments]
    return arguments

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
    
    rrdtool.graph(replaceArguments(arguments,'1h','Past hour'))
    rrdtool.graph(replaceArguments(arguments,'3h','Past 3 hours'))
    rrdtool.graph(replaceArguments(arguments,'1d','Past day'))
    rrdtool.graph(replaceArguments(arguments,'1w','Past week'))
    rrdtool.graph(replaceArguments(arguments,'1m','Past month'))
    rrdtool.graph(replaceArguments(arguments,'1y','Past year'))
