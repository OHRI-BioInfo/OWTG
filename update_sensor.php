<?php
include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";

$alias = $_GET["alias"];
$address = $_GET["address"];
$graph = isset($_GET["graph"]);
$minAlarm = $_GET["minAlarm"];
$maxAlarm = $_GET["maxAlarm"];

$error = false;
$redirect = "<meta http-equiv=\"refresh\" content=\"5; url=/owdir.php\">\n";


if(strpos($alias,':') !== false){
    $error = true;
    echo $redirect;
    echo '[".$address."][Error] Alias contains invalid character \':\'<br>';
    exit(1);
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
if(!$error){
    header("location: /owdir.php");
}else{
    echo "<a href=\"/owdir.php\">Click here</a> if you are not redirected in 5 seconds.</a>";
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
