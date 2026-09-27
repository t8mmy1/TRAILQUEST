/**
 * Trail Quest - Messages Handler
 * Handles message notifications with auto-dismissal
 */

document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.alert');
    const DISPLAY_TIME = 5000; // Time in milliseconds (5 seconds)
    
    // Function to close a message
    function closeMessage(message) {
        message.classList.add('fade-out');
        setTimeout(() => {
            message.style.display = 'none';
        }, 300); // Match this with the CSS animation time
    }
    
    // Add click event to all close buttons
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            closeMessage(this.parentElement);
        });
    });
    
    // Auto dismiss messages after timeout
    messages.forEach(message => {
        setTimeout(() => {
            closeMessage(message);
        }, DISPLAY_TIME);
    });
}); 