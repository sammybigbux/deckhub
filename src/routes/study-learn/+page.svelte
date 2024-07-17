<style>
    body, html {
      margin: 0;
      padding: 0;
      height: 100%;
    }
    .center-container {
      display: flex;
      justify-content: center;
      align-items: flex-start;
      height: 100vh;
      padding-top: 25vh; /* Position the card 25% from the top */
    }
    .card {
      padding: 20px; /* Adjust the padding as needed */
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
      width: 100%;
      max-width: 600px; /* Optional: limit the width of the card */
    }
    .card-header {
      font-size: 4rem; /* Increase the font size for the title */
      text-align: center;
      padding-bottom: 20px; /* Add more bottom padding */
    }
    .card-content {
        padding-top: 30px;
    }
    ul {
      list-style-type: disc; /* Ensure bullets are displayed */
      margin-left: 50px; /* Adjust as needed */
      padding-left: 0; /* Remove default padding */
    }
    ul li {
      margin-bottom: 10px; /* Adjust spacing between list items */
    }
    .button-container {
      display: flex;
      justify-content: flex-end;
      margin-top: 30px; /* Optional: add some space between content and buttons */
    }
    .btn {
      margin-left: 10px; /* Add space between buttons */
    }
    .bg-primary-500 {
      background-color: #007bff;
    }
    .bg-secondary-500 {
      background-color: #6c757d;
    }

  </style>
  
  <div class="center-container">
    <div class="card p-4">
      <h1 class="card-header">What to do?</h1>
      <p class="card-content p-4">
        At the <strong>Learn</strong> stage, your goal is to gain familiarity with the key terms:
      </p>
      <ul>
        <li>
          Select "Learn" on the flashcard deck
        </li>
        <li>
          Review the flashcards until you "finish" the deck (or feel confident enough to move on)
        </li>
        <li>
          Select the "Evaluate" option in the <a href="/learn"><strong>Learn Menu</strong></a>
        </li>
      </ul>
      <div class="button-container">
        <a href="https://quizlet.com/890590526/aws-saa-exam-concepts-flash-cards/?funnelUUID=fe8369eb-0bf9-44aa-a5e4-4891a6bf111a" class="btn bg-primary-500 card-hover">Get started</a>
        <a href="/learn" class="btn bg-secondary-500 card-hover">No thanks!</a>
      </div>
    </div>
  </div>
  