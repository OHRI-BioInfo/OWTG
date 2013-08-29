<?php
/*
 * Copyright (C) 2013 OHRI 
 * This file is part of OWTG.
 * 
 * OWTG is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * OWTG is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with OWTG.  If not, see <http://www.gnu.org/licenses/>.
*/

include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";

$alias = $_GET["alias"];
$address = $_GET["address"];
$graph = isset($_GET["graph"]);
$minAlarm = $_GET["minAlarm"];
$maxAlarm = $_GET["maxAlarm"];

$error = false;
$fatal = false;
$redirect = "<meta http-equiv=\"refresh\" content=\"5; url=owdir.php\">\n";

if(strpos($alias,':') !== false){
    $error = true;
    $fatal = true;
    echo $redirect;
    echo "[".$address."][Error] Alias contains invalid character ':'<br>";
}
if($alias[0] == '#'){
    $error = true;
    $fatal = true;
    echo $redirect;
    echo "[".$address."][Error] Alias cannot start with '#'<br>";
}
if(preg_match("/[^0-9.]/",$minAlarm) == 1){
    $minAlarm = preg_replace("/[^0-9.]/",'',$minAlarm);
    $error = true;
    echo $redirect;
    echo "[".$address."][Warning] Minimum Alarm contained invalid characters which have been stripped.<br>\n";
    echo "[".$address."][Warning] Minimum Alarm set to ".$minAlarm."<br>";
}
if(preg_match("/[^0-9.]/",$maxAlarm) == 1){
    $maxAlarm = preg_replace("/[^0-9.]/",'',$maxAlarm);
    $error = true;
    echo $redirect;
    echo "[".$address."][Warning] Maximum Alarm contained invalid characters which have been stripped.<br>\n";
    echo "[".$address."][Warning] Maximum Alarm set to ".$maxAlarm."<br>";
}
if(floatval($maxAlarm) <= floatval($minAlarm)){
    $error = true;
    $fatal = true;
    echo "[".$address."][Error] Minimum Alarm cannot be greater than Maximum Alarm.<br>\n";
    echo $redirect;
}

if(!$error)
    header("location: owdir.php");
else{
    echo "<a href=\"owdir.php\">Click here</a> if you are not redirected in 5 seconds.</a>";
    if($fatal)
        exit(1);
}
$fileArray = file($sensorsFile,FILE_IGNORE_NEW_LINES);

foreach($fileArray as &$line){
    if($line[0] == '#')
        continue;
    $values = explode(':',$line);
    if($values[1] == $address){
        $values[0] = $alias;
        if($graph)
            $values[3] = 'y';
        else
            $values[3] = 'n';
        $values[4] = $minAlarm;
        $values[5] = $maxAlarm;
        $line = $values[0].':'.$values[1].':'.$values[2].':'.$values[3].':'.$values[4].':'.$values[5];
    }
}

unset($line);
$sFile = fopen($sensorsFile,'w');

foreach($fileArray as $line)
    fwrite($sFile,$line."\n");
fclose($sFile);
?>
