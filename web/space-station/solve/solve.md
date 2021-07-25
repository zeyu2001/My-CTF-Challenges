# Space Station - Solution

**Author**: zeyu2001

**Category**: Web

## Finding the App

The page at `/` simply says `Hello Mars!`.

The app is at `http://whatever.domain.com/app/`. It should be relatively easy to find this endpoint since it is one of the first entries in the `dirb/wordlists/common.txt` wordlist: https://github.com/v0re/dirb/blob/master/wordlists/common.txt

`dirb` output:
```
...
GENERATED WORDS: 4612

---- Scanning URL: http://localhost:8100/ ----
==> DIRECTORY: http://localhost:8100/app/
```

## Exploiting LFI

Basically, the application is a PHP proxy that allows users to visit websites from it.

From the footer, we can find out that the application is "Powered by PHP-Proxy".

PHP-Proxy (all versions) suffers from a Local File Inclusion (LFI) vulnerability: https://github.com/Athlon1600/php-proxy-app/issues/135

Details: https://github.com/0xUhaw/CVE-Bins/tree/master/PHP-Proxy

The encryption key is generated as follows:

```php
Config::set('encryption_key', md5(Config::get('app_key').$_SERVER['REMOTE_ADDR']));
```

The URL is encrypted as follows:

```php
$url = str_rot_pass($url, $key);
```

The following encryption function is not secure enough. It simply takes every character of the key and adds it to the original plaintext. Since we know both the plaintext (the original URL) and the ciphertext (the `q=` parameter), we can easily reverse-engineer the key.

```php
// rotate each string character based on corresponding ascii values from some key
function str_rot_pass($str, $key, $decrypt = false){
	
	// if key happens to be shorter than the data
	$key_len = strlen($key);
	
	$result = str_repeat(' ', strlen($str));
	
	for($i=0; $i<strlen($str); $i++){

		if($decrypt){
			$ascii = ord($str[$i]) - ord($key[$i % $key_len]);
		} else {
			$ascii = ord($str[$i]) + ord($key[$i % $key_len]);
		}
	
		$result[$i] = chr($ascii);
	}
	
	return $result;
}
```

Then, after getting the key, it is simply a matter of encrypting `file:///var/www/html/flag.txt` since the `file://` protocol is not explicitly banned.

```
➜  solve git:(zeyu2001/develop) ✗ python3 solve.py
STC{l0cal_f1l3_1nclus10n_328d47c2ac5b2389ddc47e5500d30e04}
```