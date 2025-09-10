// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    // Set up navigation
    setupNavigation();
    
    // Set up interactive elements
    setupInteractiveElements();
    
    // Load user data if available
    loadUserData();
});

// Set up navigation between pages
function setupNavigation() {
    // Get all navigation items
    const navItems = document.querySelectorAll('.nav-item');
    
    // Add click event to each navigation item
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            navigateTo(page);
        });
    });
}

// Navigate to a specific page
function navigateTo(page) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(p => p.classList.remove('active'));
    
    // Show the selected page
    const selectedPage = document.getElementById(`${page}-page`);
    if (selectedPage) {
        selectedPage.classList.add('active');
    }
    
    // Update navigation active state
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        if (item.getAttribute('data-page') === page) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Set up interactive elements
function setupInteractiveElements() {
    // Hobby selection
    const hobbyItems = document.querySelectorAll('.hobby-item');
    hobbyItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('selected');
        });
    });
    
    // Mood selection
    const moodOptions = document.querySelectorAll('.mood-option');
    moodOptions.forEach(option => {
        option.addEventListener('click', function() {
            moodOptions.forEach(o => o.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    
    // Make life areas sortable
    const lifeAreas = document.getElementById('life-areas');
    if (lifeAreas) {
        setupSortable(lifeAreas);
    }
}

// Simple sortable implementation
function setupSortable(element) {
    let draggedItem = null;
    
    // Add event listeners to sortable items
    const items = element.querySelectorAll('.sortable-item');
    
    items.forEach(item => {
        // Drag start
        item.addEventListener('dragstart', function() {
            draggedItem = this;
            setTimeout(() => this.style.opacity = '0.5', 0);
        });
        
        // Drag end
        item.addEventListener('dragend', function() {
            this.style.opacity = '1';
            draggedItem = null;
        });
        
        // Make items draggable
        item.setAttribute('draggable', 'true');
        
        // Drag over
        item.addEventListener('dragover', function(e) {
            e.preventDefault();
        });
        
        // Drag enter
        item.addEventListener('dragenter', function(e) {
            e.preventDefault();
            if (this !== draggedItem) {
                this.style.borderTop = '2px solid #2E86AB';
            }
        });
        
        // Drag leave
        item.addEventListener('dragleave', function() {
            this.style.borderTop = '';
        });
        
        // Drop
        item.addEventListener('drop', function(e) {
            e.preventDefault();
            if (this !== draggedItem) {
                if (this.parentNode === draggedItem.parentNode) {
                    let children = Array.from(this.parentNode.children);
                    let draggedIndex = children.indexOf(draggedItem);
                    let targetIndex = children.indexOf(this);
                    
                    if (draggedIndex < targetIndex) {
                        this.parentNode.insertBefore(draggedItem, this.nextSibling);
                    } else {
                        this.parentNode.insertBefore(draggedItem, this);
                    }
                }
            }
            this.style.borderTop = '';
        });
    });
}

// Save profile data
function saveProfile() {
    const name = document.getElementById('name').value;
    const job = document.getElementById('job').value;
    
    // Get selected hobbies
    const selectedHobbies = [];
    document.querySelectorAll('.hobby-item.selected').forEach(hobby => {
        selectedHobbies.push(hobby.textContent);
    });
    
    // Get life areas order
    const lifeAreas = [];
    document.querySelectorAll('#life-areas .sortable-item').forEach(area => {
        lifeAreas.push(area.textContent);
    });
    
    // Create user data object
    const userData = {
        name: name,
        job: job,
        hobbies: selectedHobbies,
        lifeAreas: lifeAreas
    };
    
    // Save to localStorage
    localStorage.setItem('handyUserData', JSON.stringify(userData));
    
    // Show success message
    alert('Profile saved successfully!');
    
    // Navigate to goals page
    navigateTo('goals');
}

// Load user data from localStorage
function loadUserData() {
    const userDataString = localStorage.getItem('handyUserData');
    if (userDataString) {
        const userData = JSON.parse(userDataString);
        
        // Fill profile form
        if (document.getElementById('name')) {
            document.getElementById('name').value = userData.name || '';
        }
        
        if (document.getElementById('job')) {
            document.getElementById('job').value = userData.job || '';
        }
        
        // Select hobbies
        if (userData.hobbies) {
            document.querySelectorAll('.hobby-item').forEach(hobby => {
                if (userData.hobbies.includes(hobby.textContent)) {
                    hobby.classList.add('selected');
                }
            });
        }
        
        // Update life areas order (more complex, would need to rebuild the list)
    }
}

// Detect if the app is running on a mobile device
function isMobileDevice() {
    return (window.innerWidth <= 768);
}

// Add a class to the body if on mobile
if (isMobileDevice()) {
    document.body.classList.add('mobile');
}