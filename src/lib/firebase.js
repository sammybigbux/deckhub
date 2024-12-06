import { initializeApp } from "firebase/app";

import {
    getAuth,
    signInWithPopup,
    GoogleAuthProvider,
    onAuthStateChanged,
    signOut,
} from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { writable } from "svelte/store";
import { userDecks } from "../stores/auth";
import { get } from "svelte/store";

const base_url = import.meta.env.VITE_BASE_URL;

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyC-ZOP0oH3IISFl3Qwzc7rGnbEB5VwYOps",
    authDomain: "deckhubapp.firebaseapp.com",
    projectId: "deckhubapp",
    storageBucket: "deckhubapp.appspot.com",
    messagingSenderId: "1086653848406",
    appId: "1:1086653848406:web:ad7fa7ec34c3061cc694f7",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Create stores for the authentication state and user information
export const isLoggedIn = writable(false); // Set to false initially
export let userName = writable("");
export let userEmail = writable("");
export let idToken = writable(""); // Store the Firebase ID token
export const userId = writable(null); // New store to track the user ID
export const stripeCustomerIdStore = writable(null); // New store to track the Stripe customer ID

// Utility function to check if localStorage is available
function isLocalStorageAvailable() {
    try {
        const test = "__localStorageTest__";
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
    } catch (error) {
        return false;
    }
}

// Subscribe to `idToken` and `userId` to persist them across refreshes
if (isLocalStorageAvailable()) {
    idToken.subscribe((token) => {
        if (token) {
            localStorage.setItem("idToken", token);
        } else {
            localStorage.removeItem("idToken");
        }
    });

    userId.subscribe((id) => {
        if (id) {
            localStorage.setItem("userId", id);
        } else {
            localStorage.removeItem("userId");
        }
    });

    // On page load, check if `idToken` and `userId` exist in localStorage
    const storedToken = localStorage.getItem("idToken");
    if (storedToken) {
        idToken.set(storedToken);
    }

    const storedUserId = localStorage.getItem("userId");
    if (storedUserId) {
        userId.set(storedUserId);
    }
}

// Listen for authentication state changes
onAuthStateChanged(auth, async (user) => {
    if (user) {
        const token = await user.getIdToken();
        idToken.set(token);
        isLoggedIn.set(true);
        userName.set(user.displayName || "User");
        userEmail.set(user.email || "");
        userId.set(user.uid); // Set the user ID in the store
    } else {
        isLoggedIn.set(false);
        userName.set("");
        userEmail.set("");
        idToken.set("");
        userId.set(null); // Clear the user ID when logged out
        userDecks.set([]); // Clear user decks
    }
	console.log("User id changed:", get(userId));
});

// Function to handle Google login
export async function loginWithGoogle() {
    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        console.log("User signed in:", user);

        // Fetch and set the ID token
        const token = await user.getIdToken();
        idToken.set(token);

        // Update stores
        isLoggedIn.set(true);
        userName.set(user.displayName || "User");
        userEmail.set(user.email || "");

        // Call the backend to create the user if it doesn't exist and get Stripe customer ID
        const stripeCustomerId = await createUserOnBackend(
            user.uid,
            user.displayName,
            user.email,
            token
        );
        if (stripeCustomerId) {
            stripeCustomerIdStore.set(stripeCustomerId); // Store the Stripe customer ID for later use
            console.log(
                "Stripe customer ID successfully set on login:",
                stripeCustomerId
            );
        }
    } catch (error) {
        console.error("Error during sign-in:", error);
    }
}

// Function to create a user on the backend if it doesn't exist
async function createUserOnBackend(userId, displayName, email, idToken) {
    try {
        const response = await fetch(
            `${base_url}/create_user_if_not_exists`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${idToken}`,
                },
                body: JSON.stringify({
                    display_name: displayName,
                    email: email,
                    user_id: userId,
                }),
            }
        );

        const result = await response.json();
        console.log(result.message);

        // Return the Stripe customer ID
        return result.stripe_customer_id;
    } catch (error) {
        console.error("Error creating user on backend:", error);
        return null;
    }
}

// Function to handle logout
export async function logout() {
    try {
        await signOut(auth);
        console.log("User signed out");
        isLoggedIn.set(false);
        userName.set("");
        userEmail.set("");
        idToken.set("");
        userDecks.set([]);
        stripeCustomerIdStore.set(null);
        userId.set(null); // Clear userId on logout
    } catch (error) {
        console.error("Error during sign-out:", error);
    }
}

export { auth, provider, db }; // Export auth, provider, and db if needed elsewhere
