// Function to delete a note
function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}

// Function to load the selected note for editing
function editNote(noteId, noteData) {
    alert("Edit Note function called for Note ID: " + noteId);
    // Load the note data into the textarea
    document.getElementById('note').value = noteData;
    // Set the noteId in the hidden field
    document.getElementById('noteId').value = noteId;
    // Change the button text to 'Update Note'
    document.getElementById('submitButton').innerText = 'Update Note';
}
