document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Event listener for sending email
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#selected-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(email_id, mailbox) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);
    // Show the email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#selected-email-view').style.display = 'block';
    // Display HTML for email
    document.querySelector('#selected-email-view').innerHTML = `
    <ul class="list-group" style="list-style: none">
    <li><strong>From: </strong>${email.sender}</li>
    <li><strong>To: </strong>${email.recipients}</li>
    <li><strong>Subject: </strong>${email.subject}</li>
    <li><strong>Timestamp: </strong>${email.timestamp}</li>
    </ul>
    <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
    <hr>
    <p>${email.body}</p>
    <button class="btn btn-sm btn-outline-secondary" id="archive_btn">${email.archived ? "Unarchive" : "Archive"}</button>
    `;
    // Mark email as read
    if (!email.read){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }
    // Add ability to archive received emails
    if (mailbox === 'sent') {
      document.querySelector('#archive_btn').style.display = 'none';
    }
    else {
      document.querySelector('#archive_btn').addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method:'PUT',
          body:JSON.stringify({
            archived: !email.archived
          })
        })
        .then(() => load_mailbox('inbox'))
      });
    }
    // Handle click on 'Reply'
    document.querySelector('#reply').addEventListener('click', function() {
      compose_email();
      let subject = email.subject;
      if (!subject.startsWith('Re:')) {
        subject = 'Re: ' + subject;
      }
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
    });
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#selected-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails)
    // Loop through emails and display each email in a box
    emails.forEach(email => {
      const element = document.createElement('div');
      element.className = "list-group-item";
      element.innerHTML = `
      <h6>From: ${email.sender}</h6>
      <h5>${email.subject}</h5>
      <p>${email.timestamp}</p>
      `;
      // Change background color when read to white
      element.className = email.read ? "read" : "unread";
      // Open email when clicked on
      element.addEventListener('click', function() {
        view_email(email.id, mailbox)
      });
      document.querySelector('#emails-view').append(element);
    })
  });
}

function send_email(event) {
  
  event.preventDefault()

  // Store information for email
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send email via POST request to /emails route
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    load_mailbox('sent');
  });
}