import { initializeApp } from 'firebase/app';
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, signOut } from 'firebase/auth';
import { getFirestore, doc, getDoc, setDoc } from 'firebase/firestore';
import { writable } from 'svelte/store'; 
import { userDecks } from '../stores/auth';

// Create a store for the authentication state
export const isLoggedIn = writable(false); // Initially assume not logged in
export let userName = writable("");

const firebaseConfig = {
    apiKey: "AIzaSyC-ZOP0oH3IISFl3Qwzc7rGnbEB5VwYOps",
    authDomain: "deckhubapp.firebaseapp.com",
    projectId: "deckhubapp",
    storageBucket: "deckhubapp.appspot.com",
    messagingSenderId: "1086653848406",
    appId: "1:1086653848406:web:ad7fa7ec34c3061cc694f7"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Export the authentication functions and provider
export async function loginWithGoogle() {
    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        console.log('User signed in:', user);
        isLoggedIn.set(true);
        userName.set(user.displayName || 'User'); 

        // Check if user exists in Firestore
        await createUserIfNotExists(user.uid, user.displayName);
        window.location.reload();

    } catch (error) {
        console.error('Error during sign-in:', error);
    }
}

async function createUserIfNotExists(userId, displayName) {
    const userRef = doc(db, 'users', userId);
    const userDoc = await getDoc(userRef);

    if (!userDoc.exists()) {
        // User doesn't exist, create a new document
        await setDoc(userRef, {
            displayName: displayName,
            decks_owned: [] // Initialize as an empty array
        });
        console.log("New user created in Firestore!");
    } else {
        console.log("User already exists in Firestore.");
    }
}

// Listen for authentication state changes (optional but recommended)
onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/auth.user.md
        isLoggedIn.set(true);
        userName.set(user.displayName || "User")
    } else {
        // User is signed out
        userName.set("")
        isLoggedIn.set(false);
    }
});

export async function logout() {
    try {
        await signOut(auth);
        console.log('User signed out');
        isLoggedIn.set(false);
        userName.set('');
        userDecks.set([]);
        window.location.reload(); // Force a refresh after signing out
    } catch (error) {
        console.error('Error during sign-out:', error);
    }
}

export {auth, provider, db}; // Export auth and provider if needed elsewhere