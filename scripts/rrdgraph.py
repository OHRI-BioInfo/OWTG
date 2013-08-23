from owtg import *
from string import replace
import rrdtool

if datGet('allowRun') != '1':
    exit(0)

if not dbExists():
    exit(1)

#Path to generate the graphs. You should not need to change this unless your webserver
#root is elsewhere.
#Default: /var/www/graphs
graphsPath = '/var/www/graphs/'

width = datGet('width')

gSensors = [s for s in getSensors() if s.graph == True]
colors = ['#9BC4E5','#310106','#04640D','#FEFB0A','#FB5514','#E115C0','#00587F','#0BC582','#FEB8C8','#9E8317','#01190F','#847D81','#58018B','#B70639','#703B01','#F7F1DF',
'#118B8A','#4AFEFA','#FCB164','#796EE6','#000D2C','#53495F','#F95475','#61FC03','#5D9608','#DE98FD','#98A088','#4F584E','#248AD0','#5C5300','#9F6551','#BCFEC6',
'#932C70','#2B1B04','#B5AFC4','#D4C67A','#AE7AA1','#C2A393','#0232FD','#6A3A35','#BA6801','#168E5C','#16C0D0','#C62100','#014347','#233809','#42083B','#82785D',
'#023087','#B7DAD2','#196956','#8C41BB','#ECEDFE','#2B2D32','#94C661','#F8907D','#895E6B','#788E95','#FB6AB8','#576094','#DB1474','#8489AE','#860E04','#FBC206',
'#6EAB9B','#F2CDFE','#645341','#760035','#647A41','#496E76','#E3F894','#F9D7CD','#876128','#A1A711','#01FB92','#FD0F31','#BE8485','#C660FB','#120104','#D48958',
'#05AEE8','#C3C1BE','#9F98F8','#1167D9','#D19012','#B7D802','#826392','#5E7A6A','#B29869','#1D0051','#8BE7FC','#76E0C1','#BACFA7','#11BA09','#462C36','#65407D',
'#491803','#F5D2A8','#03422C','#72A46E','#128EAC','#47545E','#B95C69','#A14D12','#C4C8FA','#372A55','#3F3610','#D3A2C6','#719FFA','#0D841A','#4C5B32','#9DB3B7',
'#B14F8F','#747103','#9F816D','#D26A5B','#8B934B','#F98500','#002935','#D7F3FE','#FCB899','#1C0720','#6B5F61','#F98A9D','#9B72C2','#A6919D','#2C3729','#D7C70B',
'#9F9992','#EFFBD0','#FDE2F1','#923A52','#5140A7','#BC14FD','#6D706C','#0007C4','#C6A62F','#000C14','#904431','#600013','#1C1B08','#693955','#5E7C99','#6C6E82',
'#D0AFB3','#493B36','#AC93CE','#C4BA9C','#09C4B8','#69A5B8','#374869','#F868ED','#E70850','#C04841','#C36333','#700366','#8A7A93','#52351D','#B503A2','#D17190',
'#A0F086','#7B41FC','#0EA64F','#017499','#08A882','#7300CD','#A9B074','#4E6301','#AB7E41','#547FF4','#134DAC','#FDEC87','#056164','#FE12A0','#C264BA','#939DAD',
'#0BCDFA','#277442','#1BDE4A','#826958','#977678','#BAFCE8','#7D8475','#8CCF95','#726638','#FEA8EB','#EAFEF0','#6B9279','#C2FE4B','#304041','#1EA6A7','#022403',
'#062A47','#054B17','#F4C673','#02FEC7','#9DBAA8','#775551','#835536','#565BCC','#80D7D2','#7AD607','#696F54','#87089A','#664B19','#242235','#7DB00D','#BFC7D6',
'#D5A97E','#433F31','#311A18','#FDB2AB','#D586C9','#7A5FB1','#32544A','#EFE3AF','#859D96','#2B8570','#8B282D','#E16A07','#4B0125','#021083','#114558','#F707F9',
'#C78571','#7FB9BC','#FC7F4B','#8D4A92','#6B3119','#884F74','#994E4F','#9DA9D3','#867B40','#CED5C4','#1CA2FE','#D9C5B4','#FEAA00','#507B01','#A7D0DB','#53858D',
'#588F4A','#FBEEEC','#FC93C1','#D7CCD4','#3E4A02','#C8B1E2','#7A8B62','#9A5AE2','#896C04','#B1121C','#402D7D','#858701','#D498A6','#B484EF','#5C474C','#067881']

def replaceArguments(arguments,time,title):
    arguments = [replace(s,'::::',time) for s in arguments]
    arguments = [replace(s,'::-::',title) for s in arguments]
    return arguments

for sensor in gSensors:
    alias = sensor.alias
    minAlarm = sensor.minAlarm
    maxAlarm = sensor.maxAlarm
    address = sensor.address
    
    #:::: is a placeholder for time, ::-:: is a placeholder for title
    #Colons are used because the user isn't allowed to enter them in the alias 
    arguments = [graphsPath+address+'-::::'+'.png','--end','now','--start',\
    'end-::::','--title','::-::','--width',str(width),\
    'DEF:'+address+'='+gdbFilename+':'+address+':AVERAGE',\
    'LINE:'+address+'#1A50BC:'+alias,\
    'HRULE:'+str(minAlarm)+'#0000FF:"Minimum Alarm"',\
    'HRULE:'+str(maxAlarm)+'#FF0000:"Maximum Alarm"']
    
    rrdtool.graph(replaceArguments(arguments,'1h','Past hour'))
    rrdtool.graph(replaceArguments(arguments,'3h','Past 3 hours'))
    rrdtool.graph(replaceArguments(arguments,'1d','Past day'))
    rrdtool.graph(replaceArguments(arguments,'1w','Past week'))
    rrdtool.graph(replaceArguments(arguments,'1m','Past month'))
    rrdtool.graph(replaceArguments(arguments,'1y','Past year'))

defs = []
lines = []

#Now we generate the graphs containing all sensors.

for i,sensor in enumerate(gSensors):
    label = ''
    address = sensor.address
    if sensor.alias != '':
        label = sensor.alias
    else:
        label = sensor.address
    defs.append('DEF:'+address+'='+gdbFilename+':'+address+':AVERAGE')
    lines.append('LINE:'+address+colors[i]+':'+label)
    
arguments = [graphsPath+'all'+'-::::'+'.png','--end','now','--start',\
    'end-::::','--title','::-::','--width',str(width)]
for d in defs:
    arguments.append(d)
for l in lines:
    arguments.append(l)
    
rrdtool.graph(replaceArguments(arguments,'1h','Past hour'))
rrdtool.graph(replaceArguments(arguments,'3h','Past 3 hours'))
rrdtool.graph(replaceArguments(arguments,'1d','Past day'))
rrdtool.graph(replaceArguments(arguments,'1w','Past week'))
rrdtool.graph(replaceArguments(arguments,'1m','Past month'))
rrdtool.graph(replaceArguments(arguments,'1y','Past year'))
