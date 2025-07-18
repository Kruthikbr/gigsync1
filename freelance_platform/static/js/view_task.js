// Form validation (if present on this page)
document.querySelector('form')?.addEventListener('submit', function(e) {
    const title = document.getElementById('task-title')?.value.trim();
    const category = document.getElementById('task-category')?.value;
    const description = document.getElementById('task-description')?.value.trim();
    
    if (title !== undefined && (!title || !category || !description)) {
        e.preventDefault();
        alert('Please fill in all required fields');
    }
});

// File upload display (if present on this page)
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

// Main task filtering functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded - initializing task filtering');
    
    // Get DOM elements
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const statusFilter = document.getElementById('statusFilter'); 
    const taskCards = document.querySelectorAll('.task-card');
    const noResults = document.getElementById('noResults');
    
    // Log elements to debug
    console.log('Search input:', searchInput);
    console.log('Category filter:', categoryFilter);
    console.log('Status filter:', statusFilter);
    console.log('Task cards found:', taskCards.length);
    console.log('No results element:', noResults);
    
    // Main filter function
    function filterTasks() {
        console.log('Running filter tasks');
        const searchTerm = searchInput.value.toLowerCase();
        const categoryValue = categoryFilter.value.toLowerCase();
        const statusValue = statusFilter.value.toLowerCase();
        
        console.log('Filtering with:', { searchTerm, categoryValue, statusValue });
        
        let visibleCount = 0;
        
        // Loop through all tasks and filter
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
            
            // Show or hide the card
            if (matchesSearch && matchesCategory && matchesStatus) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show "no results" message if needed
        if (visibleCount === 0) {
            noResults.style.display = 'flex';
        } else {
            noResults.style.display = 'none';
        }
        
        console.log('Visible task count:', visibleCount);
    }
    
    // Add event listeners to search and filter elements
    if (searchInput) {
        searchInput.addEventListener('input', filterTasks);
        console.log('Added input listener to search');
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterTasks);
        console.log('Added change listener to category filter');
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTasks);
        console.log('Added change listener to status filter');
    }
    
    // Initialize the filter on page load
    filterTasks();
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
});