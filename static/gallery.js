// Gallery page functionality
document.addEventListener('DOMContentLoaded', function() {
    const loadingMessage = document.getElementById('loadingMessage');
    const galleryGrid = document.getElementById('galleryGrid');
    const emptyMessage = document.getElementById('emptyMessage');

    // Load submissions when page loads
    loadSubmissions();

    async function loadSubmissions() {
        try {
            const response = await fetch('/api/submissions');
            const data = await response.json();
            
            loadingMessage.style.display = 'none';
            
            if (data.submissions && data.submissions.length > 0) {
                displaySubmissions(data.submissions);
                galleryGrid.style.display = 'grid';
            } else {
                emptyMessage.style.display = 'block';
            }
        } catch (error) {
            console.error('Error loading submissions:', error);
            loadingMessage.style.display = 'none';
            emptyMessage.style.display = 'block';
        }
    }

    function displaySubmissions(submissions) {
        galleryGrid.innerHTML = '';
        
        submissions.forEach(submission => {
            const itemCard = createItemCard(submission);
            galleryGrid.appendChild(itemCard);
        });
    }

    function createItemCard(submission) {
        const card = document.createElement('div');
        card.className = 'item-card';
        
        const hasImage = submission.image_path;
        const hasText = submission.text && submission.text.trim().length > 0;
        
        card.innerHTML = `
            <div class="item-image">
                ${hasImage ? 
                    `<img src="${submission.image_path}" alt="Item image" loading="lazy">` : 
                    `<div class="no-image">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                            <circle cx="8.5" cy="8.5" r="1.5" stroke="currentColor" stroke-width="2"/>
                            <polyline points="21,15 16,10 5,21" stroke="currentColor" stroke-width="2"/>
                        </svg>
                    </div>`
                }
            </div>
            <div class="item-content">
                <div class="item-meta">
                    <span class="item-author">${submission.name || 'Anonymous'}</span>
                    <span class="item-date">${formatDate(submission.timestamp)}</span>
                </div>
                ${hasText ? `<p class="item-description">${submission.text}</p>` : ''}
                ${submission.image_filename ? `<div class="item-filename">${submission.image_filename}</div>` : ''}
            </div>
        `;
        
        return card;
    }

    function formatDate(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
        
        if (diffInHours < 1) {
            return 'Just now';
        } else if (diffInHours < 24) {
            return `${diffInHours}h ago`;
        } else {
            const diffInDays = Math.floor(diffInHours / 24);
            return `${diffInDays}d ago`;
        }
    }

    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
});
