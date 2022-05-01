# Pigeon Aircraft Takeoff - Solution

**Author**: zeyu2001

**Category**: Web

The goal of this challenge was to leak the admin user's launch code, which is stored in their browser's `localStorage`.

Players should notice that a GET request parameter `search` can be supplied to "search" for the note (i.e. check if it starts with the given input). 

If a match is found from the search, then a button with ID `clear-output-button` is inserted into the DOM.

```javascript
// Search for notes
if (location.search) {
    const query = (new URLSearchParams(location.search.substring(1))).get('search');
    const note = search(query);
    if (note) {
        output.innerText = note;
        clearOutputDiv.innerHTML = "<button type='submit' id='clear-output-button'>Clear</button>";
        document.getElementById("clear-output-button").onclick = () => {
            output.innerText = "Output cleared. Try searching again.";
            clearOutputDiv.innerHTML = "";
        }
    }
    else {
        output.innerText = "No note found.";
        clearOutputDiv.innerHTML = "";
    }
}
```

This allows us to perform an XS Leak, using the presence of the ID element as an oracle. Solve script [here](./solve.html).

Reference: https://portswigger.net/research/xs-leak-leaking-ids-using-focus