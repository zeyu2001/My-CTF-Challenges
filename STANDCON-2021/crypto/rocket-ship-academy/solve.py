from Crypto.Util.number import long_to_bytes
from pwn import *
from decimal import *
import re

getcontext().prec = 100000000

pattern = "n = (\d+)\ne = (\d+)\nc = (\d+)"

conn = remote('localhost', '12345')
received = conn.recv().decode()

matches = re.search(pattern, received)
n, e, c = int(matches[1]), int(matches[2]), int(matches[3])

print('n =', n)
print('e =', e)
print('c =', c)
print()

ciphertext = Decimal(c) * ((2 ** Decimal(e)) % Decimal(n)) % Decimal(n)
print('Ciphertext:', ciphertext)

conn.send(str(ciphertext) + '\r\n')

received = conn.recv().decode()
matches = re.search("Decrypted: (\d+)\n", received)

decrypted = int(matches[1])
print()

print(long_to_bytes(Decimal(decrypted) / 2))
