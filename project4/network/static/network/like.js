// Get at like buttons
document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');

    // Add event listeners for 'click' on like button
    likeButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Get info about the post
            const postId = button.getAttribute('data-post-id');
            const likeCountElement = button.previousElementSibling;

            // Send AJAX request to update the like status
            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({action:'like'})
            })
            .then(response => response.json())
            .then(data => {
                // Update the like count
                const updatedLikeCount = data.like_count;
                likeCountElement.textContent = updatedLikeCount;

                // Update the like button text based on like status
                const isLiked = data.is_liked;
                if (isLiked) {
                    button.textContent = 'Unlike';
                } else {
                    button.textContent = 'Like';
                }
                })
            .catch(error => {
                console.log(error);
            });
        });
    });
});