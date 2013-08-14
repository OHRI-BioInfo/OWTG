<html>
<body>
<?php
include "settings.php";
$address = $_GET["address"];

echo "<img src=".$graphsDir.$address."-1h.png>";
echo "<img src=".$graphsDir.$address."-3h.png><br>";
echo "<img src=".$graphsDir.$address."-1d.png>";
echo "<img src=".$graphsDir.$address."-1w.png><br>";
echo "<img src=".$graphsDir.$address."-1m.png>";
echo "<img src=".$graphsDir.$address."-1y.png>";
echo "<span id=\"end\"></span>"
?>
</body>
</html>
