function showPayment(taskId, amount) {
    // Set the payment details
    document.getElementById('paymentAmount').textContent = '₹' + amount;
    // document.getElementById('paymentTaskId').textContent = taskId;
    
    // Generate QR code with payment information
    // In a real app, this would include payment processor details
    const qrData = `TaskPayment:${taskId}|Amount:₹{amount}|Timestamp:${Date.now()}`;
    document.getElementById('qrCodeImage').src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrData)}`;
    
    // Show the modal
    document.getElementById('paymentModal').style.display = "block";
    
    // Hide the QR code and show success after 10 seconds
    setTimeout(function() {
        document.getElementById('qrCodeContainer').style.display = "none";
        document.getElementById('paymentSuccess').style.display = "block";
        document.getElementById('paidAmount').textContent = '₹' + amount;
        
        // Close the modal after another 3 seconds
        setTimeout(function() {
            closeModal();
            // In a real app, you would send a request to your backend here
            // fetch(`/markAsPaid/${taskId}`, { method: 'POST' });
        }, 3000);
    }, 10000);
}

function closeModal() {
    document.getElementById('paymentModal').style.display = "none";
    // Reset the modal for next use
    document.getElementById('qrCodeContainer').style.display = "block";
    document.getElementById('paymentSuccess').style.display = "none";
}

// Close modal if clicked outside of it
window.onclick = function(event) {
    if (event.target == document.getElementById('paymentModal')) {
        closeModal();
    }
}

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
    if (searchInput) {
        searchInput.addEventListener('input', filterTasks);
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterTasks);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTasks);
    }
    
    // Initialize the filter on page load
    if (taskCards.length > 0) {
        filterTasks();
    }
});