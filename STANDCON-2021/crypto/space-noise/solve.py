from Crypto.Util.number import long_to_bytes
from scapy.all import *

packets = rdpcap("space_noise.pcap")

FLAGS = {
    'FIN': 0x01,
    'SYN': 0x02,
    'RST': 0x04,
    'PSH': 0x08,
    'ACK': 0x10,
    'URG': 0x20,
    'ECE': 0x40,
    'CWR': 0x80
}

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

morse_code = ''

for p in packets:
    if p['TCP'].flags == 'R':
        morse_code += '.'
    elif p['TCP'].flags == 'U':
        morse_code += '-'
    elif p['TCP'].flags == 'S':
        morse_code += ' '

message = ''
curr = ''

print(morse_code)

for char in morse_code:

    if char != ' ':
        curr += char

    else:
        for char in MORSE_CODE_DICT:
            if MORSE_CODE_DICT[char] == curr:
                message += char
            
        curr = ''

print(message)
print(long_to_bytes(int(message, 16)).decode())