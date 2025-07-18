function toggleDetails(employeeId) {
    const details = document.getElementById(`details-${employeeId}`);
    const button = document.getElementById(`toggle-btn-${employeeId}`);

    if (details.style.display === 'none') {
        details.style.display = 'block';
        button.innerHTML = '<i class="fas fa-eye-slash"></i> Hide Profile';
    } else {
        details.style.display = 'none';
        button.innerHTML = '<i class="fas fa-eye"></i> View Profile';
    }
}