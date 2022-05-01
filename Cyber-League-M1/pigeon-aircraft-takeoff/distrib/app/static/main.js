const noteForm = document.getElementById("note");
const output = document.getElementById("output");
const clearOutputDiv = document.getElementById("clear-output-div")

noteForm.onsubmit = (e) => {
    e.preventDefault();
    window.localStorage.setItem("note", new FormData(noteForm).get("note"));

    Swal.fire(
        'Success!',
        `You have securely stored your launch codes.`,
        'success'
    )
};

const search = (search) => {
    const note = window.localStorage.getItem("note");

    if (!note) {
        Swal.fire(
            'Not found',
            'You need to submit a note first.',
            'error'
        )
        return null;
    }
    
    if (note.startsWith(search)) {
        return note;
    }

    return null;
};

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