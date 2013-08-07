<?php
include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";

$alias = $_GET["alias"];
$address = $_GET["address"];
$graph = isset($_GET["graph"]);

if(strpos($alias,':') !== false){
    echo '<meta http-equiv="refresh" content="3; url=/owdir.php">';
    echo 'Alias contains invalid character \':\'<br>';
    echo '<a href="/owdir.php">Click here</a> if you are not redirected in 3 seconds.';
    exit(1);
}else{
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
        $line = $values[0].':'.$values[1].':'.$values[2].':'.$values[3];
    }
}

unset($line);
$sFile = fopen($sensorsFile,'w');

foreach($fileArray as $line)
    fwrite($sFile,$line."\n");
fclose($sFile);
?>
