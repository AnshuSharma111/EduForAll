document.addEventListener('DOMContentLoaded', () => {
    // Load saved notes from localStorage
    loadSavedNotes();
});

const plusIcon = document.getElementById('plusIcon');
const slider = document.getElementById('slider');
const noteInput = document.getElementById('noteInput');
const savedNotesContainer = document.getElementById('savedNotes');

// Toggle slider on plus icon click
plusIcon.addEventListener('click', toggleSlider);

// Close slider on close icon click
function closeSlider() {
    slider.style.right = '-350px';
}

// Toggle slider visibility
function toggleSlider() {
    const currentRight = parseInt(getComputedStyle(slider).right);
    slider.style.right = currentRight === 0 ? '-300px' : '0';
}

// Add a new note to the slider content
function addNote() {
    const noteText = noteInput.value.trim();

    if (noteText !== '') {
        // Save the note to localStorage
        saveNoteToLocalStorage(noteText);

        // Display the saved notes
        loadSavedNotes();

        // Clear the input after adding the note
        noteInput.value = '';
    }
}

// Save note to localStorage
function saveNoteToLocalStorage(noteText) {
    console.log('Saving note:', noteText);
    let savedNotes = JSON.parse(localStorage.getItem('notes')) || [];
    savedNotes.push(noteText);
    localStorage.setItem('notes', JSON.stringify(savedNotes));
    console.log('Note saved successfully.');
}


// Load saved notes from localStorage
function loadSavedNotes() {
    const savedNotes = JSON.parse(localStorage.getItem('notes')) || [];
    savedNotesContainer.innerHTML = '';
    if (savedNotes.length > 0) {
        savedNotesContainer.innerHTML = '<ul>';
        savedNotes.forEach((note, index) => {
            savedNotesContainer.innerHTML += `<li>${note} <button onclick="deleteNote(${index})">Delete</button></li>`;
        });
        savedNotesContainer.innerHTML += '</ul>';
    }
}

// Delete a note from localStorage and reload the notes
function deleteNote(index) {
    let savedNotes = JSON.parse(localStorage.getItem('notes')) || [];
    savedNotes.splice(index, 1);
    localStorage.setItem('notes', JSON.stringify(savedNotes));

    // Reload notes
    loadSavedNotes();
}