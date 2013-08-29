<?
include "settings.php";
$newEmail = str_replace('"',"\\\"",$_GET['email']);
$newEmail = str_replace("'","\\\'",$newEmail);
$argument = '"import owtg;owtg.datSet(\"email\",\"'.$newEmail.'\")"';
echo $argument;

exec("cd ".$etcDir."../bin;python -c ".$argument." 2>&1",$output);
print_r($output);
#header("location: owdir.php");
