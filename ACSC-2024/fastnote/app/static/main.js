const api = {};
const addNoteForm = document.getElementById('add-note');
const myNotesDiv = document.getElementById('notes');
const shareUrl = document.getElementById('share-url');

const saved = [];
const notes = [];

const notesToHTML = (notes) => {
  return notes.map((note, idx) => `
    <div data-note-id="${idx}">
      ${note}
      <button class="contrast outline" data-idx="${idx}">Delete</button>
    </div>
  `).join('');
}

const addNote = (title, content, isBatched = false) => {

  saved.push({
    'action': 'add',
    'title': title,
    'content': content
  })
  shareUrl.href = `${window.location.origin}?s=${btoa(JSON.stringify(saved))}`;

  const noteId = api.addNote(
    title,
    content
  );

  if (noteId < 0) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Note was too long!",
    });
    return;
  }

  if (!isBatched) {
    api.populateNoteHTML(api.populateNoteHTMLCallback);
    renderNotes();
  }
}

const renderNotes = () => {
  const html = notes.length > 0 ? notesToHTML(notes) : '<p>No notes yet</p>';
  myNotesDiv.innerHTML = html;
  const deleteButtons = document.querySelectorAll('[data-idx]');
  deleteButtons.forEach((button) => {
    button.addEventListener('click', (e) => {
      const noteId = e.target.dataset.idx;
      api.deleteNote(noteId, api.deleteNoteCallback)
    });
  });
}

const populateNoteHTML = (noteHTML, idx) => {
  notes[idx] = UTF8ToString(noteHTML);
}

const deleteNote = (noteId, isBatched = false) => {
  saved.push({
    'action': 'delete',
    'noteId': noteId
  })
  shareUrl.href = `${window.location.origin}?s=${btoa(JSON.stringify(saved))}`;

  if (!isBatched) {
    notes.splice(noteId, 1);
    renderNotes();
  }
}

const main = () => {
  addNoteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    
    addNote(title, content)
    addNoteForm.reset();
  })

  serialized = new URLSearchParams(window.location.search).get('s');
  if (serialized) {
    todo = JSON.parse(atob(serialized));

    todo.forEach((step) => {
      if (step.action == 'add') {
        addNote(
          step.title,
          step.content,
          true
        );
      } else if (step.action == 'delete') {
        api.deleteNote(
          step.noteId,
          api.deleteNoteCallback,
          true
        );
      }
    });
    api.populateNoteHTML(api.populateNoteHTMLCallback);
    renderNotes();
  }
}

Module.onRuntimeInitialized = async (_) => {

  api.populateNoteHTMLCallback = Module.addFunction(populateNoteHTML,'iii');
  api.deleteNoteCallback = Module.addFunction(deleteNote,'vi');

  api.addNote = Module.cwrap('addNote', 'number', ['string', 'string']);
  api.deleteNote = Module.cwrap('deleteNote', 'number', ['number', 'number']);
  api.populateNoteHTML = Module.cwrap('populateNoteHTML', null, ['number']);

  main();
};