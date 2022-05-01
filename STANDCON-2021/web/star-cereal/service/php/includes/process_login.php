<?php

session_start();

class SQL
{
	protected $query;
	
	function __construct()
	{
		$this->query = "SELECT email, password FROM starcereal.admins WHERE email=? AND password=?";
	}
	
	function exec_query($email, $pass)
	{
		$conn = new mysqli("starcereal_mysql_1", getenv("MYSQL_USER"), getenv("MYSQL_PASS"));

		// Check connection
		if ($conn->connect_error) {
			die("Connection failed. Please inform CTF creators.");
		}
		
		$stmt = $conn->prepare($this->query);

		// Sanity check
		if (! $stmt->bind_param("ss", $email, $pass))
		{
			return NULL;
		}
		
		$stmt->execute();
		$result = $stmt->get_result();
		
		return $result;
	}
	
}

class User
{
	public $email;
	public $password;
	
	protected $sql;
	
	function __construct($email, $password)
	{
		$this->email = $email;
		$this->password = $password;
		$this->sql = new SQL();
	}
	
	function __toString() 
	{
		return $this->email . ':' . $this->password;
	}
	
	function is_admin()
	{
		$result = $this->sql->exec_query($this->email, $this->password);
		
		if ($result && $row = $result->fetch_assoc()) {
			if ($row['email'] && $row['password'])
			{
				return true;
			}
		}
		return false;
	}
}


class Login
{
	public $user;
	public $mfa_token;
	
	protected $_correctValue;
	
	function __construct($user, $mfa_token)
	{
		$this->user = $user;
		$this->mfa_token = $mfa_token;
	}
	
	function verifyLogin()
	{
		$this->_correctValue = random_int(1e10, 1e11 - 1);
		if ($this->mfa_token === $this->_correctValue)
		{
			return $this->user->is_admin();
		}
	}
}

if(isset($_COOKIE["login"])){
	try
	{
		$login = unserialize(base64_decode(urldecode($_COOKIE["login"])));
		if ($login->verifyLogin())
		{
			$_SESSION['admin'] = true;
		}
		else
		{
			$_SESSION['admin'] = false;
		}
	}
	catch (Error $e)
	{
		$_SESSION['admin'] = false;
	}
}

?>
