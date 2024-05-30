document.addEventListener('DOMContentLoaded', function() {
    const likeCountElements = document.querySelectorAll('.like-count');

    likeCountElements.forEach(likeCountElement => {
        const postId = likeCountElement.getAttribute('data-post-id');

        // Send AJAX request to fetch the initial like count
        fetch(`/like-count/${postId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Update the like count in the HTML
            const likeCount = data.like_count;
            likeCountElement.innerHTML = likeCount;
        })
        .catch(error => {
            console.log(error);
        });
    });
});