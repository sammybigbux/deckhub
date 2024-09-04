import { initializeApp } from 'firebase/app';
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, signOut } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { writable } from 'svelte/store'; 
import { userDecks } from '../stores/auth';

// Firebase configuration
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
const db = getFirestore(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Create stores for the authentication state and user information
export const isLoggedIn = writable(false); // Set to false initially
export let userName = writable("");
export let idToken = writable(""); // Store the Firebase ID token

// Utility function to check if localStorage is available
function isLocalStorageAvailable() {
    try {
        const test = '__localStorageTest__';
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
    } catch (error) {
        return false;
    }
}

// Subscribe to `idToken` to persist it across refreshes
if (isLocalStorageAvailable()) {
    idToken.subscribe((token) => {
        if (token) {
            localStorage.setItem('idToken', token);
        } else {
            localStorage.removeItem('idToken');
        }
    });

    // On page load, check if a token exists in localStorage
    const storedToken = localStorage.getItem('idToken');
    if (storedToken) {
        idToken.set(storedToken);
    }
}

// Listen for authentication state changes
onAuthStateChanged(auth, async (user) => {
    if (user) {
        const token = await user.getIdToken();
        idToken.set(token);
        isLoggedIn.set(true);
        userName.set(user.displayName || "User");
    } else {
        isLoggedIn.set(false);
        userName.set("");
        idToken.set("");
        userDecks.set([]); // Clear user decks
    }
});

// Function to handle Google login
export async function loginWithGoogle() {
    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        console.log('User signed in:', user);
        
        // Fetch and set the ID token
        const token = await user.getIdToken();
        idToken.set(token);

        // Update stores
        isLoggedIn.set(true);
        userName.set(user.displayName || 'User');

        // Call the backend to create the user if it doesn't exist
        await createUserOnBackend(user.uid, user.displayName, token);
    } catch (error) {
        console.error('Error during sign-in:', error);
    }
}

// Function to create a user on the backend if it doesn't exist
async function createUserOnBackend(userId, displayName, idToken) {
    try {
        const response = await fetch('http://127.0.0.1:5000/create_user_if_not_exists', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${idToken}`
            },
            body: JSON.stringify({ display_name: displayName })
        });

        const result = await response.json();
        console.log(result.message);
    } catch (error) {
        console.error('Error creating user on backend:', error);
    }
}

// Function to handle logout
export async function logout() {
    try {
        await signOut(auth);
        console.log('User signed out');
        isLoggedIn.set(false);
        userName.set('');
        idToken.set('');
        userDecks.set([]);
    } catch (error) {
        console.error('Error during sign-out:', error);
    }
}

export { auth, provider, db }; // Export auth, provider, and db if needed elsewhere
