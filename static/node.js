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
            savedNotesContainer.innerHTML += `<li>${note} <button onclick="deleteNote(${index})">Delete</button>
            <button onclick="downloadNoteAsTxt(${index})">Download</button></li>`;
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

// Function to download a note as a .txt file
function downloadNoteAsTxt(index) {
    let savedNotes = JSON.parse(localStorage.getItem('notes')) || [];
    let noteText = savedNotes[index];
    
    // Create a Blob object to represent the data as a file
    let blob = new Blob([noteText], { type: "text/plain" });
    
    // Create a temporary anchor element
    let anchor = document.createElement("a");
    anchor.download = "note_" + index + ".txt"; // Name of the downloaded file
    anchor.href = window.URL.createObjectURL(blob);
    anchor.style.display = "none"; // Hide the anchor element
    
    // Append the anchor to the body
    document.body.appendChild(anchor);
    
    // Trigger a click event on the anchor
    anchor.click();
    
    // Remove the anchor from the body
    document.body.removeChild(anchor);
}