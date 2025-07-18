// Simple form validation
document.querySelector('form').addEventListener('submit', function(e) {
    const title = document.getElementById('task-title').value.trim();
    const category = document.getElementById('task-category').value;
    const description = document.getElementById('task-description').value.trim();
    
    if (!title || !category || !description) {
        e.preventDefault();
        alert('Please fill in all required fields');
    }
});

// File upload display (if you add file upload functionality later)
document.querySelector('.file-upload-input')?.addEventListener('change', function(e) {
    const files = e.target.files;
    const fileNameDisplay = document.querySelector('.file-name');
    
    if (files.length > 0) {
        if (files.length === 1) {
            fileNameDisplay.textContent = files[0].name;
        } else {
            fileNameDisplay.textContent = `${files.length} files selected`;
        }
    } else {
        fileNameDisplay.textContent = 'No files selected';
    }
});