<?php
include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";

$alias = $_GET["alias"];
$address = $_GET["address"];
$graph = isset($_GET["graph"]);
$minAlarm = $_GET["minAlarm"];
$maxAlarm = $_GET["maxAlarm"];

$error = False;
$errorStuff ="<meta http-equiv=\"refresh\" content=\"3; url=/owdir.php\">\n
<a href=\"/owdir.php\">Click here</a> if you are not redirected in 3 seconds.";


if(strpos($alias,':') !== false){
    $error = True;
    echo '[".$address."][Error] Alias contains invalid character \':\'<br>';
    echo $errorStuff;
    exit(1);
}
if(preg_match('[^0-9.]',$minAlarm)){
    $minAlarm = preg_replace('[^0-9.]','',$minAlarm);
    $error = True;
    echo "[".$address."][Warning] Minimum Alarm contained invalid characters which have been stripped.<br>\n";
    echo "[".$address."][Warning] Minimum Alarm set to ".$minAlarm;
    echo $errorStuff;
}
if(preg_match('[^0-9.]',$maxAlarm)){
    $maxAlarm = preg_replace('[^0-9.]','',$maxAlarm);
    $error = True;
    echo "[".$address."][Warning] Maximum Alarm contained invalid characters which have been stripped.<br>\n";
    echo "[".$address."][Warning] Maximum Alarm set to ".$maxAlarm;
    echo $errorStuff;
}
if(!$error){
    header("location: /owdir.php");
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
