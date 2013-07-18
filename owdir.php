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
error_reporting(E_ALL);
$aliasFile = "/settings/alias/list";
$adapter = "localhost:4304";

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

function findAlias($address){
    global $aliasFile;
    $aliasArray = preg_split("/[=\n]/",get($aliasFile),-1,PREG_SPLIT_NO_EMPTY);
    $i = 0;
    foreach($aliasArray as $curString){
        if($curString == $address){
            return $aliasArray[$i+1];
        }
        $i++;
    }
    return "";
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
    echo "<td>".$curAddress."</td>";
    echo "<td>".findAlias($curAddress)."</td>";
    echo "<td>button</td>";
    echo "</tr>";
    $i++;
}
echo "</table>";

finish();

?>
</body>
</html>
