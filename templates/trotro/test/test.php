<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

<html>
<head>
<title>Untitled</title>
<style type="text/css">

</style>
</head>
<body>
<a href="pill.html" class="a" >pilas</a>
<?php

$name = $_POST['name'];
$id = $_POST['ID'];
$telephone = $_POST['telephone'];
$submit = $_POST['submit'];


echo "the test is on <br/>";
mysql_connect("localhost","root","1234") or die("could not connect to mysql");
mysql_select_db("marc_book") or die("db not valid");

$query="select * from author";
$result=mysql_query($query) or die(mysql_error());
 
while($row=mysql_fetch_array($result))
{
 echo "name: ";
 echo $row["name"];
 echo "<br>\n";
 echo "<br>".$row["phone"]."<br>";
}





?>
</body>
</html>
