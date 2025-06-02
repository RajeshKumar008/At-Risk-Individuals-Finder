// JavaScript for interactivity
document.addEventListener("DOMContentLoaded", function() {
    // Add fade-in effect to all elements with the 'fade-in' class
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.classList.add('visible');
    });

    // Form validation for file upload in complaint form
    const complaintForm = document.querySelector('form');
    if (complaintForm) {
        complaintForm.addEventListener('submit', function(event) {
            const photoInput = document.getElementById('photo');
            if (!photoInput.files.length) {
                alert("Please upload a photo of the missing person.");
                event.preventDefault();
            }
        });
    }

    // Interactive hover effect on complaint list items
    const listItems = document.querySelectorAll('.list-group-item');
    listItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.classList.add('hovered');
        });
        item.addEventListener('mouseleave', () => {
            item.classList.remove('hovered');
        });
    });
});
