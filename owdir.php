<html>
<head>
    <style type="text/css">
    table{
        border-collapse:collapse;
        border:1px solid black;
    }th,td{
        border: 1px solid black;
        padding: 4px;
    }
    input.alarms{
        width: 4em;
        margin-right:auto;
        margin-left:auto;
        text-align:center;
        display:block;
    }
    input.alias{
        width: 8.5em;
    }
    </style>
    <meta http-equiv="refresh" content="16">
</head>
<body>
<?php
include "settings.php";
include "Sensor.php";
include "/opt/owfs/share/php/OWNet/ownet.php";
$ow = new OWNet($adapter);

function isAddressOnline($address){
	global $ow;
    #Get directory listing, separate into an array
    $directoryArray = explode(",",$ow->dir("/")["data"]);
    foreach ($directoryArray as $currentDir){
        #We don't want to include this directory, 
        #as although it has a "temperature" file, it is not a device
        if($currentDir == "/simultaneous")
            continue;
        if($ow->read($currentDir."/temperature") != NULL){
            if($ow->read($currentDir."/address") == $address)
                return True;
        }
    }
    return False;
}

function getSensors(){
    global $sensorsFile;
    global $ow;
    
    $sensorArray = array();
    $fileArray = file($sensorsFile,FILE_IGNORE_NEW_LINES);
    foreach($fileArray as $line){
        if($line[0] == '#')
            continue;
        $discoveredArray = explode(":",$line);
        $newSensor = new Sensor();
        $newSensor->alias = $discoveredArray[0];
        $newSensor->address = $discoveredArray[1];
        $newSensor->timestamp = intval($discoveredArray[2]);
        if($discoveredArray[3] == 'y')
            $newSensor->graph = True;
        else
            $newSensor->graph = False;
        $newSensor->minAlarm = floatval($discoveredArray[4]);
        $newSensor->maxAlarm = floatval($discoveredArray[5]);
        $newSensor->online = isAddressOnline($newSensor->address);
        
        $sensorArray[] = $newSensor;
    }
    return $sensorArray;
}

echo "<table>\n";
$i=1;
echo "<th>Device Address</th><th>Discovery Date</th><th>Temperature</th><th>Online</th>";
echo "<th>Alias</th><th>Min. Alarm</th><th>Max. Alarm</th><th>Graph?</th><th>Modify</th>\n";
foreach(getSensors() as $curSensor){
    $online = 'No'; #String to describe online status
    $checked = ''; #If this is set to "checked", then the checkbox will be checked
    if($curSensor->online == True)
        $online = 'Yes';
    if($curSensor->graph == True)
        $checked = ' checked';
    if($i%2 == 0)
        echo "<tr style=\"background-color:lightgrey;\">\n";
    else
        echo "<tr>\n";
    echo "<td><a href=\"showgraphs.php?address=".$curSensor->address."\">".$curSensor->address."</a></td>\n";
    echo "<td>".date("d M Y H:i:s T",$curSensor->timestamp)."</td>\n";
    echo "<td>".$ow->read("/".$curSensor->address."/temperature")."</td>\n";
    echo "<td>".$online."</td>\n";
    echo "<form name=\"form".$i."\" action=\"update_sensor.php\" method=\"get\">\n";
    echo "<input type=\"hidden\" name=\"address\" value=\"".$curSensor->address."\" />\n";
    echo "<td><input name=\"alias\" type=\"text\" value=\"".$curSensor->alias."\" class=\"alias\"></td>\n";
    echo "<td><input name=\"minAlarm\" type=\"number\" value=\"".$curSensor->minAlarm."\" class=\"alarms\"></td>";
    echo "<td><input name=\"maxAlarm\" type=\"number\" value=\"".$curSensor->maxAlarm."\" class=\"alarms\"></td>";
    echo "<td><input name=\"graph\" type=\"checkbox\" value=\"graph\" ".$checked."></td>\n";
    echo "<td><input type=\"submit\" value=\"Modify\"></td></form>\n";
    echo "</tr>\n";
    $i++;
}
echo "</table>\n";

unset($ow);

?>
</body>
</html>
