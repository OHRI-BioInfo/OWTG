<!--
    Copyright (C) 2013 OHRI 

    This file is part of OWTG.

    OWTG is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OWTG is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with OWTG.  If not, see <http://www.gnu.org/licenses/>.
-->

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
