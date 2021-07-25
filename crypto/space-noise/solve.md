# Space Noise - Solution

**Author**: zeyu2001

**Category**: Crypto / Forensics

This is a covert TCP channel (morse code). The protocol is as follows:

- RST = .
- URG = -
- SYN = I have finished sending a character.
- PSH = I acknowledge this character. Send the next character.

Decoding the morse code gives the flag in hex.

Solver script in `solve.py`.