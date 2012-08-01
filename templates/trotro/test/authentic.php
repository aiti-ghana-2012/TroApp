<html>
<head>

<title>writing to database </title>

</head>
<body>

<?php

$name=$_POST['sname'];

$id_no=$_POST['id'];

$date_of_last_hosp_visit=$_POST['sdate'];

$name_of_physician=$_POST['physician'];




mysql_connect("localhost","root","1234") or die(mysql_error());

mysql_select_db("Nii") or die(mysql_error()) ;

$insert="insert into pat_inf (Patient Name,HIS/STUDENT #,Day Of Last Hospital Visit,Name Of Physician) values ('$name','$id_no','$date_of_last_hosp_visit','$name_of_physician')";

  mysql_query($insert) or die(mysql_error());
  
 

?>

these is the information log <br>

<?php

$query = "select * from pat_inf";

$result = mysql_query($query);



while($rows = mysql_fetch_array($result)) {
   echo "patient name =";
   echo $rows["Patient Name"];
   echo "<br>";
   echo "patient ID number = ";
   echo $rows["HIS/STUDENT #"];
   echo "<br>";
   echo "LAST HOSPITAL VISIT =";
   echo $rows["Day OF LAST HOSPITAL VISIT"];
   echo "<br>";
   echo "NAME OF PHYSICIAN =";
   echo $rows["NAME OF PHYSICIAN"];
   echo "<br>";
   
   	
	
	}

?>

</body>
</html>