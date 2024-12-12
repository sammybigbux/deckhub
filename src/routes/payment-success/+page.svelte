<script>
    // Import the functions you need from the SDKs you need
    import { initializeApp } from "firebase/app";
    import { getAuth } from "firebase/auth";
    import { userId } from '../../lib/firebase';
    import { onMount } from 'svelte';
    import { get } from 'svelte/store';
    // TODO: Add SDKs for Firebase products that you want to use
    // https://firebase.google.com/docs/web/setup#available-libraries

    let payment_confirmed = false;
    const base_url = import.meta.env.VITE_BASE_URL;
    
    // Your web app's Firebase configuration
    const firebaseConfig = {
      apiKey: "AIzaSyC-ZOP0oH3IISFl3Qwzc7rGnbEB5VwYOps",
      authDomain: "deckhubapp.firebaseapp.com",
      projectId: "deckhubapp",
      storageBucket: "deckhubapp.appspot.com",
      messagingSenderId: "1086653848406",
      appId: "1:1086653848406:web:ad7fa7ec34c3061cc694f7"
    };

    async function confirm_payment() {
      const productName = "AWS Certified Solutions Architect";
      const userID = await getUserID();
      const response = await fetch(`${base_url}/confirm_payment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: userID, product_name: productName })
      });
      if (response.ok) {
      console.log("Post request successful");
      } else {
      console.error("Post request failed");
      }
    }

    async function getUserID() {
        return new Promise((resolve, reject) => {
            const uid = get(userId);  // Get current value of userId
            if (uid) {
                resolve(uid);  // If userID is already set, return it
            } else {
                // Wait for userID to be populated
                const unsubscribe = userId.subscribe(value => {
                    if (value) {
                        resolve(value);
                        unsubscribe();  // Unsubscribe once the userID is populated
                    }
                });
            }
        });
    }
    
    // Initialize Firebase
    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);

    onMount(async () => {
      if (!payment_confirmed) {
        confirm_payment();
        payment_confirmed = true;
      }
    });
    </script>
    
    <style>
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

        max-width: 600px; /* Optional: limit the width of the card */
      }
      .card-header {
        font-size: 2.5rem;
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

    </style>
    
    <div class="center-container">
      <div class="card p-4">
        <h1 class="card-header">Thanks for your purchase</h1>
        <p class="card-content p-4">You can navigate to the full version with the button below. If you have any feedback please don't hesitate to submit it on the feedback page. We take feedback very seriously and will try to implement a fix / feature within 48 hours of being notified!</p>
        <div class="button-container">
          <a href="/new/bounty"><button type="button" class="btn outline-blue card-hover">Feedback Page</button></a>
          <a href="/new/learn/AWS Certified Solutions Architect"><button type="button" class="btn primary-blue card-hover">Back to studying</button></a>
        </div>
      </div>
    </div>
    