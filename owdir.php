<html>
<head>
</head>
<body>
<?php
error_reporting(E_ALL);
$adapter = "localhost:4304";

#Connect to owserver
$init_result = init( $adapter );
if ( $init_result != '1' )
{
    echo "could not initialize the 1-wire bus.\n";
    exit(1);
}

function getAddresses(){
    #Get directory listing, separate into an array
    $addressArray;
    $directoryArray = explode(",",get('/'));
    $i = 0;
    foreach ($directoryArray as $currentDir){
        if($currentDir == "simultaneous") #Due to a bug, reading simultaneous crashes owserver
            continue;
        if(get("/".$currentDir."temperature") != NULL){
            $addressArray[$i] = get("/".$currentDir."address");
            $i++;
        }
    }
    return $addressArray;
}
getAddresses();
finish();

?>
</body>
</html>
