// Script to handle navigation and iframe loading
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for navigation links
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Refresh iframes if needed
    document.querySelectorAll('iframe').forEach(iframe => {
        iframe.addEventListener('load', function() {
            // Optional: Add any iframe loaded functionality here
            console.log('Iframe loaded:', iframe.src);
        });
    });
});