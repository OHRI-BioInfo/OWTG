<?php
include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";

$alias = $_GET["alias"];
$address = $_GET["address"];
$graph = isset($_GET["graph"]);

$ow = new OWNet($adapter);

#Set the alias
$ow->set("/".$address."/alias",$alias); 
#Copy the internal alias file to the external one, to preserve aliases
$fileData = $ow->read($aliasFile);
$fileData = str_replace("\r","",$fileData);
file_put_contents($externalAliasFile,$fileData);

unset($ow);

$fileArray = file($discoveredFile,FILE_IGNORE_NEW_LINES);

foreach($fileArray as &$line){
    $values = explode(':',$line);
    if($values[0] == $address){
        if($graph)
            $values[2] = 'y';
        else
            $values[2] = 'n';
        $line = $values[0].':'.$values[1].':'.$values[2];
    }
}

unset($line);
$dFile = fopen($discoveredFile,'w');

foreach($fileArray as $line)
    fwrite($dFile,$line."\n");

header("location: /owdir.php");
?>
