// Get all edit buttons
document.addEventListener('DOMContentLoaded', function() {
    
    const editButtons = document.querySelectorAll('.edit-btn');

    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.getAttribute('data-post-id');
            const postContainer = button.closest('.edit-container');
            const postText = postContainer.querySelector('.text').innerText;

            // Replace post content with a textarea
            const textarea = document.createElement('textarea');
            textarea.value = postText;
            postContainer.querySelector('.text').style.display = 'none';
            postContainer.appendChild(textarea);

            // Add a save button
            const saveButton = document.createElement('button');
            saveButton.innerText = 'Save';
            saveButton.classList.add('btn', 'btn-primary'); // Add Bootstrap classes
            saveButton.setAttribute('style', 'background-color: #007bff; color: #fff; border: none; padding: 4px 8px; font-size: 12px; cursor: pointer;');
            postContainer.appendChild(saveButton);

            // Remove the edit button
            button.style.display = 'none';

            // Add event listener to the save button
            saveButton.addEventListener('click', () => {
                const updatedText = textarea.value;

                // Send AJAX request to update the post
                fetch(`/edit/${postId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ text: updatedText })
                })
                    .then(response => response.json())
                    .then(data => {
                        // Update the post content with the updated text
                        postContainer.querySelector('.text').innerText = data.updated_text;
                        textarea.remove();
                        saveButton.remove();
                        postContainer.querySelector('.text').style.display = 'block';
                        
                        // Put back the edit button
                        button.style.display = 'inline-block';
                    })
                    .catch(error => {
                        console.log(error);
                    });
            });
        });
    });
});