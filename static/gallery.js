// Utility function for date formatting
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

// Gallery page functionality
document.addEventListener('DOMContentLoaded', function() {
    const loadingMessage = document.getElementById('loadingMessage');
    const galleryGrid = document.getElementById('galleryGrid');
    const emptyMessage = document.getElementById('emptyMessage');
    
    // AI Search elements
    const aiSearchInput = document.getElementById('aiSearchInput');
    const aiSearchBtn = document.getElementById('aiSearchBtn');
    const searchSuggestions = document.getElementById('searchSuggestions');
    const suggestionsList = document.getElementById('suggestionsList');
    const searchResultsInfo = document.getElementById('searchResultsInfo');
    const resultsCount = document.getElementById('resultsCount');
    const clearSearchBtn = document.getElementById('clearSearchBtn');

    // Store original submissions for search functionality
    let originalSubmissions = [];
    let isSearchMode = false;

    // Load submissions when page loads
    loadSubmissions();
    
    // AI Search functionality
    setupAISearch();

    async function loadSubmissions() {
        try {
            const response = await fetch('/api/submissions');
            const data = await response.json();
            
            console.log('Loaded submissions from API:', data);
            
            loadingMessage.style.display = 'none';
            
            if (data.submissions && data.submissions.length > 0) {
                // Store a deep copy of the original submissions
                originalSubmissions = JSON.parse(JSON.stringify(data.submissions));
                console.log('Stored original submissions:', originalSubmissions.length);
                displaySubmissions(data.submissions);
                galleryGrid.style.display = 'grid';
                emptyMessage.style.display = 'none';
            } else {
                console.log('No submissions found');
                emptyMessage.style.display = 'block';
                galleryGrid.style.display = 'none';
            }
        } catch (error) {
            console.error('Error loading submissions:', error);
            loadingMessage.style.display = 'none';
            emptyMessage.style.display = 'block';
        }
    }

    function displaySubmissions(submissions) {
        console.log('Displaying submissions:', submissions.length);
        galleryGrid.innerHTML = '';
        
        if (submissions && submissions.length > 0) {
            submissions.forEach((submission, index) => {
                console.log(`Creating card ${index + 1}:`, submission.text || 'No text');
                const itemCard = createItemCard(submission);
                galleryGrid.appendChild(itemCard);
            });
        } else {
            console.log('No submissions to display');
        }
    }

    function createItemCard(submission) {
        const card = document.createElement('div');
        card.className = 'item-card';
        
        const hasImage = submission.image_path;
        const hasText = submission.text && submission.text.trim().length > 0;
        const isSearchResult = submission.isSearchResult;
        const searchScore = submission.searchScore;
        
        card.innerHTML = `
            <div class="item-image">
                ${hasImage ? 
                    `<img src="${submission.image_path}" alt="Item image" loading="lazy" class="clickable-image" data-submission='${JSON.stringify(submission)}'>` : 
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
                    ${isSearchResult ? `<span class="search-match-score">${searchScore}% match</span>` : ''}
                </div>
                ${hasText ? `<p class="item-description">${submission.text}</p>` : ''}
                ${submission.contact ? `<div class="item-contact">📞 ${submission.contact}</div>` : ''}
                ${isSearchResult && submission.match_reasons ? `<div class="match-reasons">${submission.match_reasons.join(', ')}</div>` : ''}
            </div>
        `;
        
        // Add click event listener to images
        if (hasImage) {
            const img = card.querySelector('.clickable-image');
            img.style.cursor = 'pointer';
            img.addEventListener('click', () => openModal(submission));
        }
        
        return card;
    }

    // Add smooth scrolling
    document.documentElement.style.scrollBehavior = 'smooth';
});

// Modal functions
function openModal(submission) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalDescription = document.getElementById('modalDescription');
    const modalAuthor = document.getElementById('modalAuthor');
    const modalContact = document.getElementById('modalContact');
    
    // Set image source
    modalImage.src = submission.image_path;
    modalImage.alt = submission.text || 'Item image';
    
    // Set description
    if (submission.text && submission.text.trim().length > 0) {
        modalDescription.textContent = submission.text;
        modalDescription.style.display = 'block';
    } else {
        modalDescription.style.display = 'none';
    }
    
    // Set author
    modalAuthor.textContent = `Posted by ${submission.name || 'Anonymous'} • ${formatDate(submission.timestamp)}`;
    
    // Set contact info
    if (submission.contact) {
        modalContact.innerHTML = `📞 ${submission.contact}`;
        modalContact.style.display = 'flex';
    } else {
        modalContact.style.display = 'none';
    }
    
    // Show modal
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restore scrolling
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// AI Search functionality
function setupAISearch() {
    const aiSearchInput = document.getElementById('aiSearchInput');
    const aiSearchBtn = document.getElementById('aiSearchBtn');
    const searchSuggestions = document.getElementById('searchSuggestions');
    const suggestionsList = document.getElementById('suggestionsList');
    const searchResultsInfo = document.getElementById('searchResultsInfo');
    const resultsCount = document.getElementById('resultsCount');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    
    // Store original submissions for search functionality
    let originalSubmissions = [];
    let isSearchMode = false;
    
    // Search button click handler
    aiSearchBtn.addEventListener('click', performAISearch);
    
    // Enter key handler for search input
    aiSearchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performAISearch();
        }
    });
    
    // Clear search button handler
    clearSearchBtn.addEventListener('click', function(e) {
        e.preventDefault();
        clearSearch();
    });
    
    // Input change handler for suggestions
    aiSearchInput.addEventListener('input', function() {
        if (this.value.trim().length > 2) {
            showSearchSuggestions();
        } else {
            hideSearchSuggestions();
        }
    });
    
    async function performAISearch() {
        const query = aiSearchInput.value.trim();
        if (!query) return;
        
        try {
            // Show loading state
            aiSearchBtn.disabled = true;
            aiSearchBtn.innerHTML = '<div class="spinner" style="width: 16px; height: 16px; border: 2px solid transparent; border-top: 2px solid currentColor; border-radius: 50%; animation: spin 1s linear infinite;"></div> Searching...';
            
            // Perform AI search
            const formData = new FormData();
            formData.append('query', query);
            formData.append('threshold', '0.3');
            
            const response = await fetch('/api/search', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Update UI with search results
                isSearchMode = true;
                displaySearchResults(data.results, data.suggestions);
                updateSearchResultsInfo(data.total_matches);
                hideSearchSuggestions();
            } else {
                console.error('Search failed:', data);
                alert('Search failed. Please try again.');
            }
            
        } catch (error) {
            console.error('Error performing AI search:', error);
            alert('Search failed. Please try again.');
        } finally {
            // Reset button state
            aiSearchBtn.disabled = false;
            aiSearchBtn.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
                    <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2"/>
                </svg>
                Search
            `;
        }
    }
    
    function displaySearchResults(results, suggestions) {
        const galleryGrid = document.getElementById('galleryGrid');
        const emptyMessage = document.getElementById('emptyMessage');
        
        
        // Hide empty message if showing
        emptyMessage.style.display = 'none';
        
        // Display search results
        if (results && results.length > 0) {
            // Add search highlighting to results
            const enhancedResults = results.map(result => {
                const enhanced = { ...result };
                // Add search match indicator
                enhanced.isSearchResult = true;
                enhanced.searchScore = Math.round(result.similarity_score * 100);
                return enhanced;
            });
            
            displaySubmissions(enhancedResults);
            galleryGrid.style.display = 'grid';
        } else {
            // Show no results message
            galleryGrid.innerHTML = `
                <div class="no-results-message" style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                    <h3 style="margin-bottom: 0.5rem; color: var(--text-primary);">No items found</h3>
                    <p style="margin-bottom: 1.5rem;">Try different keywords or be more specific</p>
                    <a href="#" onclick="clearSearch(); return false;" class="nav-link" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: var(--bg-primary); color: var(--text-primary); border: 2px solid var(--border-color); border-radius: 8px; font-weight: 500; text-decoration: none; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 12h18M9 6l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        Go back to main Gallery
                    </a>
                </div>
            `;
            galleryGrid.style.display = 'grid';
        }
        
        // Show suggestions if available
        if (suggestions && suggestions.length > 0) {
            showSuggestions(suggestions);
        }
    }
    
    function updateSearchResultsInfo(count) {
        resultsCount.textContent = count;
        searchResultsInfo.style.display = 'flex';
    }
    
    function showSuggestions(suggestions) {
        suggestionsList.innerHTML = '';
        suggestions.forEach(suggestion => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'suggestion-item';
            suggestionItem.textContent = suggestion;
            suggestionItem.addEventListener('click', function() {
                aiSearchInput.value = suggestion;
                performAISearch();
            });
            suggestionsList.appendChild(suggestionItem);
        });
        searchSuggestions.style.display = 'block';
    }
    
    function showSearchSuggestions() {
        // Show basic suggestions based on input
        const suggestions = [
            "black backpack",
            "phone case",
            "laptop charger",
            "keys",
            "wallet",
            "glasses"
        ];
        showSuggestions(suggestions);
    }
    
    function hideSearchSuggestions() {
        searchSuggestions.style.display = 'none';
    }
    
    function clearSearch() {
        console.log('Clearing search...');
        console.log('Original submissions count:', originalSubmissions.length);
        
        isSearchMode = false;
        aiSearchInput.value = '';
        searchResultsInfo.style.display = 'none';
        hideSearchSuggestions();
        
        // Clear any existing content
        galleryGrid.innerHTML = '';
        
        // Restore original submissions
        if (originalSubmissions && originalSubmissions.length > 0) {
            console.log('Restoring', originalSubmissions.length, 'original submissions');
            displaySubmissions(originalSubmissions);
            galleryGrid.style.display = 'grid';
            emptyMessage.style.display = 'none';
            
            // Show a brief confirmation message
            showTemporaryMessage(`✅ Showing all ${originalSubmissions.length} items`);
        } else {
            console.log('No original submissions to restore, showing empty message');
            emptyMessage.style.display = 'block';
            galleryGrid.style.display = 'none';
        }
        
        // Force a visual update
        galleryGrid.style.opacity = '0';
        setTimeout(() => {
            galleryGrid.style.opacity = '1';
        }, 100);
    }
    
    function showTemporaryMessage(message) {
        // Create a temporary message element
        const messageEl = document.createElement('div');
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--accent-color), #8b5cf6);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            animation: slideIn 0.3s ease;
        `;
        messageEl.textContent = message;
        
        // Add animation keyframes
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(messageEl);
        
        // Remove after 3 seconds
        setTimeout(() => {
            messageEl.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
                if (style.parentNode) {
                    style.parentNode.removeChild(style);
                }
            }, 300);
        }, 3000);
    }
    
    // Make clearSearch globally available
    window.clearSearch = clearSearch;
}

// Initialize AI search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupAISearch();
});
