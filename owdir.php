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
    </style>
    <meta http-equiv="refresh" content="16">
</head>
<body>
<?php
include "settings.php";
include "/opt/owfs/share/php/OWNet/ownet.php";
$ow = new OWNet($adapter);

function getAddresses(){
	global $ow;
    #Get directory listing, separate into an array
    $addressArray;
    $directoryArray = explode(",",$ow->dir("/")["data"]);
    $i = 0;
    foreach ($directoryArray as $currentDir){
        #We don't want to include this directory, as it isn't a device
        if($currentDir == "/simultaneous")
            continue;
        if($ow->read($currentDir."/temperature") != NULL){
            $addressArray[$i] = $ow->read($currentDir."/address");
            $i++;
        }
    }
    return $addressArray;
}

$addressArray = getAddresses();
echo "<table>\n";
$i=1;
echo "<th>Device Address</th><th>Temperature</th></th><th>Alias</th><th>Modify</th>";
foreach($addressArray as $curAddress){
    if($i%2 == 0)
        echo "<tr style=\"background-color:lightgrey;\">\n";
    else
        echo "<tr>\n";
    echo "<td>".$curAddress."</td>\n";
    echo "<td>".$ow->read("/".$curAddress."/temperature")."</td>";
    echo "<form name=\"form".$i."\" action=\"save_alias.php\" method=\"get\">\n";
    echo "<input type=\"hidden\" name=\"address\" value=\"".$curAddress."\" />\n";
    echo "<td><input name=\"alias\" type=\"text\" value=\"".$ow->read("/".$curAddress."/alias")."\" /></td>\n";
    echo "<td><input type=\"submit\" value=\"Modify\" /></td></form>\n";
    echo "</tr>\n";
    $i++;
}
echo "</table>";

unset($ow);

?>
</body>
</html>
