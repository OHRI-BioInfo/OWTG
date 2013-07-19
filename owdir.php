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
</head>
<body>
<?php
include "settings.php";

#Connect to owserver
$init_result = init( $adapter );
if ( $init_result != '1' )
{
    echo "Could not initialize the 1-wire bus.\n";
    exit(1);
}

function getAddresses(){
    #Get directory listing, separate into an array
    $addressArray;
    $directoryArray = explode(",",get("/"));
    $i = 0;
    foreach ($directoryArray as $currentDir){
        #We don't want to include this directory, as it isn't a device
        if($currentDir == "simultaneous/")
            continue;
        if(get("/".$currentDir."temperature") != NULL){
            $addressArray[$i] = get("/".$currentDir."address");
            $i++;
        }
    }
    return $addressArray;
}

$addressArray = getAddresses();
echo "<table>\n";
$i=1;
echo "<th>Device Address</th><th>Alias</th><th>Modify</th>";
foreach($addressArray as $curAddress){
    if($i%2 == 0)
        echo "<tr style=\"background-color:lightgrey;\">\n";
    else
        echo "<tr>\n";
    echo "<td>".$curAddress."</td>\n";
    echo "<form name=\"form".$i."\" action=\"save_alias.php\" method=\"get\">\n";
    echo "<input type=\"hidden\" name=\"address\" value=\"".$curAddress."\" />\n";
    echo "<td><input name=\"alias\" type=\"text\" value=\"".get("/".$curAddress."/alias")."\" /></td>\n";
    echo "<td><input type=\"submit\" value=\"Modify\" /></td></form>\n";
    echo "</tr>\n";
    $i++;
}
echo "</table>";

finish();

?>
</body>
</html>
