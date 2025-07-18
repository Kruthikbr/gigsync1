const stars = document.querySelectorAll('.star');
const ratingInput = document.getElementById('rating-input');
const ratingText = document.getElementById('rating-text');
let selectedRating = 0;

const ratingDescriptions = [
    "Select your rating",
    "Poor - Very dissatisfied",
    "Fair - Somewhat dissatisfied",
    "Good - Satisfied",
    "Very Good - Happy with the work",
    "Excellent - Exceeded expectations"
];

stars.forEach(star => {
    star.addEventListener('click', () => {
        selectedRating = parseInt(star.getAttribute('data-rating'));
        ratingInput.value = selectedRating;
        updateStars();
        updateRatingText();
    });
    
    star.addEventListener('mouseover', () => {
        const hoverRating = parseInt(star.getAttribute('data-rating'));
        highlightStars(hoverRating);
    });
});

document.getElementById('stars').addEventListener('mouseout', () => {
    updateStars();
});

function highlightStars(rating) {
    stars.forEach(star => {
        const starRating = parseInt(star.getAttribute('data-rating'));
        star.classList.toggle('active', starRating <= rating);
        star.classList.toggle('fas', starRating <= rating);
        star.classList.toggle('far', starRating > rating);
    });
}

function updateStars() {
    highlightStars(selectedRating);
}

function updateRatingText() {
    ratingText.textContent = ratingDescriptions[selectedRating];
}