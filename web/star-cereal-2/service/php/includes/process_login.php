<?php

session_start();

function exec_query($email, $pass)
{
	$conn = new mysqli("starcereal_mysql_2", getenv("MYSQL_USER"), getenv("MYSQL_PASS"), "starcereal");

	// Check connection
	if ($conn->connect_error) {
		die("Connection failed. Please inform CTF creators.");
	}
	
	$result = $conn->query("SELECT email, password FROM admins WHERE email='" . $email . "' AND password='" . $pass . "';");
	return $result;
}

if ($_SERVER['HTTP_X_FORWARDED_FOR'] != '172.16.2.24')
{
	header('HTTP/1.0 403 Forbidden');
	die('<h1>Forbidden</h1><p>Only admins allowed to login.</p>');
}

$_SESSION['admin'] = false;

// Handle form submission
if (isset($_POST['email']) && isset($_POST['pass']))
{
	$result = exec_query($_POST['email'], $_POST['pass']);	

	if ($result && $row = $result->fetch_assoc()) {
		if ($row['email'] == $_POST['email'] && $row['password'])
		{
			$_SESSION['admin'] = true;
		}
	}
}

?>
