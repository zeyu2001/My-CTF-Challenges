# Mission Control - Solution

**Author**: zeyu2001

**Category**: Pwn

Compilation: `gcc -static -z execstack -z norelro -fno-stack-protector -o mission_control mission_control.c -m32`

This is a classic string format vulnerability. To get the flag, users must overwrite the `secret_code` global variable.

Since there is a `strncmp()` check, players must calculate the following: [The value we want] - [The bytes alredy wrote] = [The value to set].

To get the address of `secret_code`:

```
$ objdump -t mission_control | grep secret_code
080dffbc g     O .bss	00000004 secret_code
```

After running `solve.py`, we will have an interactive shell.

```
[*] Switching to interactive mode
$ cat flag.txt
STC{1_l0v3_f0rm4t_st1ngs_0ab7a4af7bb1343810ccde8244031f2f}$ 
$  
```