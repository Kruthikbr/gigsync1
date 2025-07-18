// File upload preview functionality
document.getElementById('output-photos').addEventListener('change', function(e) {
    const files = e.target.files;
    const previewContainer = document.getElementById('file-preview');
    previewContainer.innerHTML = '';
    
    if (files.length > 0) {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (file.type.match('image.*')) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const previewItem = document.createElement('div');
                    previewItem.className = 'file-preview-item';
                    
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    
                    const removeBtn = document.createElement('span');
                    removeBtn.className = 'remove-btn';
                    removeBtn.innerHTML = '&times;';
                    removeBtn.addEventListener('click', function() {
                        previewItem.remove();
                        // You would also need to remove the file from the input
                    });
                    
                    previewItem.appendChild(img);
                    previewItem.appendChild(removeBtn);
                    previewContainer.appendChild(previewItem);
                }
                
                reader.readAsDataURL(file);
            }
        }
    }
});

// Drag and drop functionality
const fileUploadBtn = document.querySelector('.file-upload-btn');

fileUploadBtn.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadBtn.style.backgroundColor = '#e9ecef';
    fileUploadBtn.style.borderColor = 'var(--primary-color)';
});

fileUploadBtn.addEventListener('dragleave', () => {
    fileUploadBtn.style.backgroundColor = '#f8f9fa';
    fileUploadBtn.style.borderColor = '#ccc';
});

fileUploadBtn.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadBtn.style.backgroundColor = '#f8f9fa';
    fileUploadBtn.style.borderColor = '#ccc';
    
    const files = e.dataTransfer.files;
    document.getElementById('output-photos').files = files;
    
    // Trigger change event
    const event = new Event('change');
    document.getElementById('output-photos').dispatchEvent(event);
});