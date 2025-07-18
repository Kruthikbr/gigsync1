// Simple form validation
document.querySelector('form')?.addEventListener('submit', function(e) {
    const title = document.getElementById('task-title')?.value.trim();
    const category = document.getElementById('task-category')?.value;
    const description = document.getElementById('task-description')?.value.trim();
    
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

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const statusFilter = document.getElementById('statusFilter');
    const taskCards = document.querySelectorAll('.task-card');
    const noResults = document.getElementById('noResults');
    
    function filterTasks() {
        const searchTerm = searchInput.value.toLowerCase();
        const categoryValue = categoryFilter.value.toLowerCase();
        const statusValue = statusFilter.value.toLowerCase();
        
        let visibleCount = 0;
        
        taskCards.forEach(card => {
            const title = card.getAttribute('data-title').toLowerCase();
            const description = card.getAttribute('data-description').toLowerCase();
            const category = card.getAttribute('data-category').toLowerCase();
            const status = card.getAttribute('data-status').toLowerCase();
            const skills = card.getAttribute('data-skills').toLowerCase();
            
            // Check if card matches all filters
            const matchesSearch = searchTerm === '' || 
                                    title.includes(searchTerm) || 
                                    description.includes(searchTerm) || 
                                    skills.includes(searchTerm);
                                    
            const matchesCategory = categoryValue === '' || category === categoryValue;
            const matchesStatus = statusValue === '' || status === statusValue;
            
            if (matchesSearch && matchesCategory && matchesStatus) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show or hide "No results" message
        if (visibleCount === 0) {
            noResults.style.display = 'block';
        } else {
            noResults.style.display = 'none';
        }
    }
    
    // Add event listeners to search and filter elements
    searchInput.addEventListener('input', filterTasks);
    categoryFilter.addEventListener('change', filterTasks);
    statusFilter.addEventListener('change', filterTasks);
    
    // Initialize the filter on page load
    filterTasks();
});