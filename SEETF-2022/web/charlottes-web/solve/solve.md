# Charlotte's Web - Solution

**Author**: zeyu2001

1. Prototype pollution in `utils.merge()`

2. Off-by-one error in `background.js` font validation allows us to pollute `utils.FONTS[10]`, bypassing the validation.

    ```javascript
    let settings = utils.merge(result, newSettings);

    // Validate fonts
    let valid = false;
    for (let i = 0; i <= utils.FONTS.length; i++) {
        if (settings.font === utils.FONTS[i]) {
            valid = true;
            break;
        }
    }
    ```

3. In `setFont.js`, the `credentials: include` option can be polluted in the `fetch()` call to use the credentials for `http://app/`.

    ```javascript
    // Load external fonts.
    const customStyle = JSON.parse(document.getElementById('page-style').innerText);
    utils.setStyle(document.body, utils.merge({fontFamily: 'custom'}, customStyle));
    document.getElementById('page-style').remove();

    fetch(font, {method: 'GET'}).then(response => response.text()).then(text => { 
        const style = document.createElement("style");
        style.textContent = text;
        document.head.appendChild(style);
    });
    ```

4. The output is placed in the exploit page's `style` element, and can be read by the attacker.