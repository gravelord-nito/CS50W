document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('','',''));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

  // email composition eventlistener
  document.querySelector('#compose-form').onsubmit = () => { // can also use eventlistener using 'submit' this will be added to whatever default function you used

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      
      //console.log(result);
      if(result.message === undefined){
        alert(result.error);
      }
      else{    
        load_mailbox('sent');
      }
    })
    
    return false; // don't forget this in form submitting idiot, this makes so that nothing will be returned to server from the html form itself
  };
}

function load_mail(id){

  function rarchive(isar){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !isar
      })
    })
    .then(() => load_mailbox(isar ? 'inbox':'archive'));
  }
  
  document.querySelector('#emails-view').innerHTML = "";

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

    const emailDiv = document.createElement("div");
    emailDiv.style.border = "1px solid black";
    emailDiv.style.padding = "10px";
    emailDiv.style.marginBottom = "10px";
    emailDiv.style.display = 'flex';
    emailDiv.style.flexDirection = 'column';
  
    const sender = document.createElement("p");
    sender.style.fontWeight = "bold";
    sender.innerHTML = `<strong>From: </strong>${email.sender}`;
    emailDiv.appendChild(sender);
  
    const recipient = document.createElement("p");
    recipient.innerHTML = `<strong>To: </strong>${email.recipients[0]}`;
    emailDiv.appendChild(recipient);
  
    const subject = document.createElement("p");
    subject.innerHTML = `<strong>Subject: </strong>${email.subject}`;
    emailDiv.appendChild(subject);
  
    const timestamp = document.createElement("p");
    subject.innerHTML = `<strong>Timestamp: </strong>${email.subject}`;
    emailDiv.appendChild(timestamp);

    if(email.sender !== document.querySelector('h2').innerHTML){
      const buttons = document.createElement("div");

      const replybutt = document.createElement("button");
      replybutt.className = "btn btn-sm btn-outline-primary";
      replybutt.innerHTML = "REPLY";
      replybutt.onclick = () => compose_email(email.sender, (email.subject.slice(0, 3) === 'RE:' ? '':'RE: ') + email.subject, 'On ' + email.timestamp + ' ' + email.sender + ' wrote:\n' + email.body + '\n');
      buttons.appendChild(replybutt);
      
      const archivebutt = document.createElement("button");
      archivebutt.className = "btn btn-sm btn-outline-primary";
      archivebutt.innerHTML = "ARCHIVE/ UNARCCHIVE";
      archivebutt.onclick = () => rarchive(email.archived);
      buttons.appendChild(archivebutt);
      
      emailDiv.appendChild(buttons);
    }
  
    const bodyDiv = document.createElement("div");
    bodyDiv.innerText = email.body;
    bodyDiv.style.borderTop = "1px solid black";
    bodyDiv.style.marginTop = "10px";
    bodyDiv.style.paddingTop = "10px";
    emailDiv.appendChild(bodyDiv);
  
    document.querySelector('#emails-view').append(emailDiv);

    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // fetch and Show mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    //console.log(emails);
    emails.forEach(function(email){

      // create a div element
      const div = document.createElement("div");
      if(email.read){
        div.style.backgroundColor = "gray";
      }
      
      // add the sender property to the div element with bold styling
      const sender = document.createElement("b");
      sender.innerHTML = email.sender;
      div.appendChild(sender);

      // add the subject property to the div element
      const subject = document.createElement("p");
      subject.innerHTML = email.subject;
      subject.style.flexGrow = 10;
      subject.style.paddingLeft = "10px";
      div.appendChild(subject);

      // add the timestamp property to the div element with gray color
      const timestamp = document.createElement("p");
      timestamp.innerHTML = email.timestamp;
      timestamp.style.color = "gray";
      div.appendChild(timestamp);

      // add some CSS styling to the div element
      div.style.border = "1px solid black";
      div.style.padding = "10px";
      div.style.margin = "10px";
      div.style.display = "flex";
      div.style.flexDirection = "row";
      div.style.alignItems = "baseline";

      // add the element to the page
      div.addEventListener('click', () => load_mail(email.id));
      document.querySelector('#emails-view').append(div);
    });
  });
}