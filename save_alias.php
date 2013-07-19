<?php

include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";

$alias = $_GET["alias"];
$address = $_GET["address"];

$ow = new OWNet($adapter);

$ow->set("/".$address."/alias",$alias);

unset($ow);

header("location: /owdir.php");
?>
