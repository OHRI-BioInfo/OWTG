<?php
include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";

$alias = $_GET["alias"];
$address = $_GET["address"];

$ow = new OWNet($adapter);

#Set the alias
$ow->set("/".$address."/alias",$alias); 
#Copy the internal alias file to the external one, to preserve aliases
$fileData = $ow->read($aliasFile);
file_put_contents($externalAliasFile,$fileData);

unset($ow);

header("location: /owdir.php");
?>
