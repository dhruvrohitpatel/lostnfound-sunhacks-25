// DOM elements
const form = document.getElementById('collectionForm');
const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn.querySelector('.btn-text');
const btnLoader = submitBtn.querySelector('.btn-loader');
const successMessage = document.getElementById('successMessage');

// File upload handling
imageInput.addEventListener('change', handleImageUpload);

function handleImageUpload(event) {
    const file = event.target.files[0];
    
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file.');
            return;
        }
        
        // Validate file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            alert('File size must be less than 10MB.');
            return;
        }
        
        // Create preview
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.innerHTML = `
                <img src="${e.target.result}" alt="Preview" />
                <div style="margin-top: 0.5rem; font-size: 0.875rem; color: #9ca3af;">
                    ${file.name} (${formatFileSize(file.size)})
                </div>
            `;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Drag and drop functionality
const fileLabel = document.querySelector('.file-label');

fileLabel.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#3b82f6';
    fileLabel.style.background = '#1e1e1e';
});

fileLabel.addEventListener('dragleave', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#2d2d2d';
    fileLabel.style.background = '#1a1a1a';
});

fileLabel.addEventListener('drop', (e) => {
    e.preventDefault();
    fileLabel.style.borderColor = '#2d2d2d';
    fileLabel.style.background = '#1a1a1a';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageInput.files = files;
        handleImageUpload({ target: { files: files } });
    }
});

// Form submission
form.addEventListener('submit', handleFormSubmit);

async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Show loading state
    setLoadingState(true);
    
    try {
        const formData = new FormData(form);
        
        // Add timestamp
        formData.append('timestamp', new Date().toISOString());
        
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            showSuccessMessage();
            form.reset();
            imagePreview.style.display = 'none';
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Submission failed');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Failed to submit. Please try again.');
    } finally {
        setLoadingState(false);
    }
}

function setLoadingState(loading) {
    submitBtn.disabled = loading;
    
    if (loading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
    } else {
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }
}

function showSuccessMessage() {
    form.style.display = 'none';
    successMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds and reset form
    setTimeout(() => {
        successMessage.style.display = 'none';
        form.style.display = 'block';
    }, 5000);
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Input validation
const textInput = document.getElementById('textInput');
const nameInput = document.getElementById('nameInput');

textInput.addEventListener('input', validateForm);
imageInput.addEventListener('change', validateForm);
nameInput.addEventListener('input', validateForm);

function validateForm() {
    const hasText = textInput.value.trim().length > 0;
    const hasImage = imageInput.files.length > 0;
    
    // Enable submit button if either text or image is provided
    submitBtn.disabled = !(hasText || hasImage);
}

// Initialize form validation
validateForm();

// Add some interactive feedback
const inputs = document.querySelectorAll('.input, .textarea');
inputs.forEach(input => {
    input.addEventListener('focus', () => {
        input.parentElement.style.transform = 'scale(1.02)';
        input.parentElement.style.transition = 'transform 0.2s ease';
    });
    
    input.addEventListener('blur', () => {
        input.parentElement.style.transform = 'scale(1)';
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!submitBtn.disabled) {
            form.dispatchEvent(new Event('submit'));
        }
    }
});

// Add smooth scrolling for better UX
document.documentElement.style.scrollBehavior = 'smooth';
