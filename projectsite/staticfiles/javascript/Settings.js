// FAQ js

       // Tab functionality
        const tabs = document.querySelectorAll('.tab');
        const sections = document.querySelectorAll('.faq-section');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabId = tab.getAttribute('data-tab');
                
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                tab.classList.add('active');
                
                // Show all sections for "all" tab
                if (tabId === 'all') {
                    sections.forEach(section => {
                        section.style.display = 'block';
                    });
                } else {
                    // Show only the selected section
                    sections.forEach(section => {
                        if (section.id === tabId) {
                            section.style.display = 'block';
                        } else {
                            section.style.display = 'none';
                        }
                    });
                }
            });
        });

        // Search functionality
        const searchInput = document.getElementById('search-input');
        const faqItems = document.querySelectorAll('.faq-item');
        const noResultsElem = document.createElement('div');
        noResultsElem.className = 'no-results';
        noResultsElem.style.textAlign = 'center';
        noResultsElem.style.padding = '2rem';
        noResultsElem.style.color = '#6b7280';
        noResultsElem.style.fontSize = '1.125rem';
        noResultsElem.style.display = 'none';
        noResultsElem.style.width = '100%';
        noResultsElem.style.gridColumn = '1 / -1';
        noResultsElem.innerHTML = 'No results found. Please try a different search term.';
        
        document.querySelector('.faq-container').appendChild(noResultsElem);

        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            let foundResults = false;
            
            faqItems.forEach(item => {
                const question = item.querySelector('.faq-question').textContent.toLowerCase();
                const answer = item.querySelector('.faq-answer').textContent.toLowerCase();
                
                if (question.includes(searchTerm) || answer.includes(searchTerm)) {
                    item.style.display = 'block';
                    foundResults = true;
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Show/hide sections based on search results
            sections.forEach(section => {
                const visibleItems = section.querySelectorAll('.faq-item[style="display: block"]');
                
                if (visibleItems.length > 0 || searchTerm === '') {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
            
            // Show or hide no results message
            if (!foundResults && searchTerm !== '') {
                noResultsElem.style.display = 'block';
            } else {
                noResultsElem.style.display = 'none';
            }
        });
        
        // Add search clear button
        const searchContainer = document.querySelector('.search-container');
        const clearButton = document.createElement('button');
        clearButton.textContent = '×';
        clearButton.style.position = 'absolute';
        clearButton.style.right = '12px';
        clearButton.style.top = '50%';
        clearButton.style.transform = 'translateY(-50%)';
        clearButton.style.border = 'none';
        clearButton.style.background = 'none';
        clearButton.style.fontSize = '20px';
        clearButton.style.fontWeight = 'bold';
        clearButton.style.color = '#6b7280';
        clearButton.style.cursor = 'pointer';
        clearButton.style.display = 'none';
        clearButton.style.padding = '0 10px';
        
        searchContainer.appendChild(clearButton);
        
        searchInput.addEventListener('input', function() {
            clearButton.style.display = this.value ? 'block' : 'none';
        });
        
        clearButton.addEventListener('click', function() {
            searchInput.value = '';
            searchInput.dispatchEvent(new Event('input'));
            clearButton.style.display = 'none';
            searchInput.focus();
        });