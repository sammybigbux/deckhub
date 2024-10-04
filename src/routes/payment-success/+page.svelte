<script>
    // Import the functions you need from the SDKs you need
    import { initializeApp } from "firebase/app";
    import { getAuth } from "firebase/auth";
    // TODO: Add SDKs for Firebase products that you want to use
    // https://firebase.google.com/docs/web/setup#available-libraries
    
    // Your web app's Firebase configuration
    const firebaseConfig = {
      apiKey: "AIzaSyC-ZOP0oH3IISFl3Qwzc7rGnbEB5VwYOps",
      authDomain: "deckhubapp.firebaseapp.com",
      projectId: "deckhubapp",
      storageBucket: "deckhubapp.appspot.com",
      messagingSenderId: "1086653848406",
      appId: "1:1086653848406:web:ad7fa7ec34c3061cc694f7"
    };
    
    // Initialize Firebase
    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    </script>
    
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
        font-size: 2.5rem;
        text-align: left;
      }
      .card-content {
        text-align: left;
      }
      .button-container {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px; /* Optional: add some space between content and buttons */
      }
      .btn {
        margin-left: 10px; /* Add space between buttons */
      }
      .bg-primary-500 {
        background-color: #007bff;
        color: white;
      }
      .bg-secondary-500 {
        background-color: #6c757d;
        color: white;
      }
    </style>
    
    <div class="center-container">
      <div class="card p-4">
        <h1 class="card-header">Thanks for your purchase</h1>
        <p class="card-content p-4">You can find this product on the "My Decks" page. If you have any feedback please don't hesitate to submit it on the feedback page. We take feedback very seriously and will try to implement a fix / feature within 48 hours of being notified!</p>
        <div class="button-container">
          <a href="/my-cards"><button type="button" class="btn bg-primary-500 card-hover">My Decks</button></a>
          <a href="/bounty"><button type="button" class="btn bg-secondary-500 card-hover">Feedback</button></a>
        </div>
      </div>
    </div>
    