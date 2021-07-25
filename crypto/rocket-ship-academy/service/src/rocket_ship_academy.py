#!/usr/bin/env python

from Crypto.Util import number
from threading import Timer		
import signal


def extended_euclidean_algorithm(a, b):
	
	if a == 0:
		return b, 0, 1
	else:
		g, y, x = extended_euclidean_algorithm(b % a, a)
		return g, x - (b // a) * y, y
		
def find_public_key_exponent(euler_function):
	
	e = 65400
	
	while e <= 65537:
		gcd = extended_euclidean_algorithm(e, euler_function)[0]
		if gcd % n == 1 and e > 65400:
			return e
		e += 1

def modular_inverse(e, t):

	g, x, y = extended_euclidean_algorithm(e, t)
	
	if g != 1:
		raise Exception("Modular inverse does not exist")
	
	else:
		return x % t

class TimeoutExpired(Exception):
    pass

def alarm_handler(signum, frame):
    raise TimeoutExpired

def input_with_timeout(prompt, timeout):
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)

    try:
        return input(prompt)
        
    finally:
        signal.alarm(0)

p = number.getPrime(1024)
q = number.getPrime(1024)

n = p * q

e = find_public_key_exponent((p - 1) * (q - 1))
d = modular_inverse(e, (p - 1) * (q - 1))

with open('flag.txt', 'r') as f:
	flag = f.read()

c = pow(number.bytes_to_long(flag.encode()), e, n)

print('n =', n)
print('e =', e)
print('c =', c)

try:
	answer = input_with_timeout("Enter ciphertext:", 2)
    
except TimeoutExpired:
	print('\nSorry, times up!')

else:
	try:
		if int(answer) == c:
			print("It can't be that easy, can it?")
		
		else:
			decrypted = pow(int(answer), d, n)
			print("Decrypted:", decrypted)
		
	except Exception as e:
		print("Invalid ciphertext.")
