# The Pigeon Files - Solution

**Author**: zeyu2001

**Category**: Web

1. Notice that `mootools` JavaScript library is used. This is vulnerable to client-side prototype pollution.

```html
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/mootools/1.6.0/mootools-core.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/mootools-more/1.6.0/mootools-more-compressed.js"></script>
```

Refer to the [PoC](https://github.com/BlackFan/client-side-prototype-pollution/blob/master/pp/mootools-more.md).

2. Notice that if the request token is wrong, then the `request.accessGranted` attribute is never set and is thus undefined.

```javascript
if (note.startsWith(request.search)) {
    request.result = note;
}
else {
    request.result = null;
}

if (request.token === uuid) {
    request.accessGranted = true;
}

return request;
```

By exploiting the prototype pollution vulnerability, we are able to pollute the `accessGranted` attribute and prevent the access denied error.

```javascript
if (!request.accessGranted) {
    output.textContent = "Access denied.";
}
else if (!request.result) {
    output.textContent = "Note not found.";
}
else {
    output.textContent = request.result;
    setTimeout(() => {window.location.search = ""}, 5000);
}
```

3. Notice that the note is "found" as long as `note.startsWith(request.search)`. This, combined with the fact that a navigation occurs (redirection after 5 seconds of viewing the note) on a successful search allows us to perform an XS leak.

This attack is performed by inspecting `history.length` and is described [here](https://xsleaks.dev/docs/attacks/navigations/)

As long as a navigation has occured, i.e. `history.length === 3`, our substring exists in the flag.

Extract the full flag character by character: `SEE{w4k3_up_5h33pl3_1t's_obv10us}`.
