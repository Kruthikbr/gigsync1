// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Toggle between sign in and sign up forms
function toggleForms() {
    const signInForm = document.getElementById('signin-form');
    const signUpForm = document.getElementById('signup-form');
    
    if (signInForm.classList.contains('form-active')) {
        signInForm.classList.remove('form-active');
        signInForm.classList.add('signup-form');
        signUpForm.classList.remove('signup-form');
        signUpForm.classList.add('form-active');
    } else {
        signUpForm.classList.remove('form-active');
        signUpForm.classList.add('signup-form');
        signInForm.classList.remove('signup-form');
        signInForm.classList.add('form-active');
    }
}

// Confirm Password Validation
document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.querySelector("#signup-form form");
    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            const password = document.getElementById("signup-password").value;
            const confirmPassword = document.getElementById("signup-confirm-password").value;
            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                event.preventDefault(); // Prevent form submission
            }
        });
    }
});