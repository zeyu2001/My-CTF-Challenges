# WASMabism

**Author**: zeyu2001

**Category**: Web

Flag: `SEE{w4sm_c1rcl3_j3rk_83e774a0be90a3e01ea8e981e3224bf3}`

## Description

Down with the JS empire!

Note: the target page is `http://wasm.web.seetf.sg:1337`.

## Difficulty

Hard

## Solution

1. Use [solve/find.js](solve/find.js) to find a Unicode character such that when `.toLowerCase()` is called on it, it expands to 2 characters instead of 1.

The script yields the following result:

```
İ 304
```

2. Use this to bypass the length check and use the buffer overflow to overwrite the `funcPtr`. This allows us to set `censor` as the function to be called for the first iteration, giving us the `<` character needed for XSS.

Function pointers in WebAssembly are not addresses, but indices into a table of functions. The table is initialized with the functions in the order they are defined in the source code. The `clean` function has index 1, and the `censor` function has index 2.

The 4-byte index should therefore be written as `0x00000002`.

3. Use [solve/genPayload.py](solve/genPayload.py) to generate the XSS payload that results in `<iframe onload=eval(window.name)>` after sanitization. 

Our exploit page uses `window.open` to open the challenge page, and sets the `name` property of the window to the JavaScript payload. The `onload` event of the iframe will then execute the payload.