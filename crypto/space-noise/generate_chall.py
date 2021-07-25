from Crypto.Util.number import bytes_to_long
from scapy.all import *

SENDER = "192.168.1.1"
RECEIVER = "192.168.1.2"

MESSAGE = "STC{I believe that this Nation should commit itself to achieving the goal, before this decade is out, of landing a man on the Moon and returning him safely to Earth.}"

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

hex_message = hex(bytes_to_long(MESSAGE.encode()))[2:]

morse_code = ''
for char in hex_message:
    morse_code += MORSE_CODE_DICT[char.upper()] + ' '

print(morse_code)

packets = []
for char in morse_code:

    # RST = .
    # URG = -
    # SYN = I have finished sending a character.
    # PSH = I acknowledge this character. Send the next character.

    if char == '.':
        packets.append(IP(src=SENDER, dst=RECEIVER)/TCP(dport=1337,flags="R"))

    elif char == '-':
        packets.append(IP(src=SENDER, dst=RECEIVER)/TCP(dport=1337,flags="U"))

    else:
        # 'Acknowledgement' for each character
        packets.append(IP(src=SENDER, dst=RECEIVER)/TCP(dport=1337,flags="S"))
        packets.append(IP(src=RECEIVER, dst=SENDER)/TCP(dport=1337,flags="P"))

wrpcap('space_noise.pcap', packets)