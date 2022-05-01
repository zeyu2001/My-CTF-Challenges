# STANDCON-Challenges
 
![Logo](logo.png) 

Here are my challenges for the STANDCON CTF, hosted by N0H4TS on 25 July. It was my first time writing challenges for a CTF, so please feel free to let me know if you have any feedback!

The Docker files are provided, so feel free to try the challenges again locally. Read the full solutions [here](https://zeyu2001.gitbook.io/ctfs/my-challenges/standcon-ctf-2021).

## Web
- [Space Station](web/space-station)
- [Star Cereal](web/star-cereal)
- [Star Cereal 2](web/star-cereal-2)

Space Station was a relatively simple challenge, requiring participants to identify an LFI vulnerability in the PHP-Proxy library. 

Star Cereal and Star Cereal 2 proved to be the more challenging. 

Star Cereal required knowledge of PHP deserialization and object injection, while Star Cereal 2 required some creative thinking to piece clues together. 

Star Cereal 2 went unsolved until the last hour of the CTF when additional hints were released.

## Pwn
- [Mission Control](pwn/mission-control)
- [Rocket Science](pwn/rocket-science)
- [Space University of Interior Design](pwn/space-university-of-interior-design)

Mission Control was a relatively simple challenge, requiring participants to overwrite a global variable through a format string vulnerability. 

Space University of Interior Design was a rather fun challenge, requiring participants to escalate privileges through SUID and SUDO misconfigurations. 

Rocket Science proved to be the most challenging. This challenge required participants to find information on the lambdaJSON library, read the source code, and exploit it independently.

## Cryptography
- [Rocket Ship Academy](crypto/rocket-ship-academy)
- [Space Noise](crypto/space-noise)

Rocket Ship Academy was a classic textbook RSA chosen-ciphertext attack.

Space Noise was a little more challenging, requiring participants to find patterns in the given PCAP file, and infer that a covert channel was implemented using morse code.