<script lang='ts'>

    // Subscribe to the userName store
    $: userDisplayName = $userName ? $userName.split(' ')[0] : ''; // Access the value using $userName 
    import { writable, derived } from 'svelte/store';
    import { userName, auth, db, isLoggedIn } from '$lib/firebase';
    import { collection, getDocs, doc, getDoc } from 'firebase/firestore';
    import { onMount } from 'svelte';

    let searchQuery = writable('');

    interface Deck { // Define the structure of your Deck object
        id?: string; // Optional if you're using Firestore generated IDs
        icon: string;
        name: string;
        length: number;
        lastUpdated: Date;
        // ... other properties of your Card object ...
    }

    let decks = writable<Deck[]>([]);

    const filteredDecks = derived(
        [searchQuery, decks, isLoggedIn, userName], // Add userName as dependency 
        ([$searchQuery, $decks, $isLoggedIn, $userName]) => {

        if (!$isLoggedIn) { 
            return []; 
        }

        // Get the currently logged in user
        const currentUser = auth.currentUser;

        if (!currentUser) {
            console.log("No current user")
            return [];
        }

        // Get the user's owned deck names (adjust property name if needed)
        const userDecks = currentUser.decks_owned; 

        // Filter decks
        return $decks.filter(deck => 
            userDecks.includes(deck.name) && // Check by name
            deck.name.toLowerCase().includes($searchQuery.toLowerCase())
        );
        }
    );

    function handleInput(event) {
        searchQuery.set(event.target.value);
    }
    onMount(async () => {
        try {
            const querySnapshot = await getDocs(collection(db, 'decks'));
            const deckData: Deck[] = querySnapshot.docs.map((doc) => ({
                ...doc.data(), 
                id: doc.id,
                icon: doc.data().icon as string, // Make sure this is a string in Firestore
                name: doc.data().name as string, // Make sure this is a string in Firestore
                length: doc.data().length as number, // Make sure this is a number in Firestore
                lastUpdated: doc.data().lastUpdated.toDate(), // Assuming lastUpdated is a Firestore Timestamp
            }));
            decks.set(deckData);
        } catch (e) {
            console.error('Error getting documents: ', e);
        }
    });
</script>

<style>
    h1 {
    font-size: 3em; /* Adjust font size as needed */
    text-align: center; /* Center the text */
    padding-bottom: 35px;
    }
    .search-container {
        padding: 16px;
    }
    .search-bar {
        width: 100%;
        padding: 8px;
        margin-bottom: 16px;
        font-size: 1em;
        border: 1px solid #ccc;
        border-radius: 4px;
        color: black; /* Ensure the search bar text is black */
    }
    .deck-list {
        list-style-type: none;
        padding: 0;
    }
    .deck-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px;
        border-bottom: 1px solid #eee;
        background-color: #333; /* Darker Skeleton UI color */
        border-radius: 8px;
        margin-bottom: 8px;
        transition: background 0.3s;
        color: #fff; /* White text for contrast */
    }
    .deck-item:hover {
        background: #444; /* Slightly lighter Skeleton UI color */
    }
    .deck-content {
        display: flex;
        align-items: center;
        flex: 1;
    }
    .deck-icon {
        font-size: 1.5em;
        margin-right: 12px;
    }
    .deck-info {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }
    .deck-title {
        font-size: 1em;
        color: #fff; /* Ensure title text is white */
        flex: 1;
    }
    .deck-details {
        display: flex;
        flex-direction: column;
        font-size: 0.9em;
        color: #ddd; /* Slightly lighter text for details */
        margin-left: auto; /* Push details to the right */
    }
    .btn {
        margin-left: 12px; /* Add some space between details and button */
    }
    @media (max-width: 600px) {
        .deck-title {
            font-size: 0.9em;
        }
        .deck-details {
            font-size: 0.8em;
        }
    }
</style>

<div class="search-container">
    <h1>{userDisplayName}'s Decks</h1>
    <input
        type="text"
        class="search-bar"
        placeholder="Search decks..."
        on:input={handleInput}
    />
    <ul class="deck-list">
        {#each $filteredDecks as deck}
            <div class="deck-item bg-gradient-to-br variant-gradient-tertiary-secondary">
                <div class="deck-content">
                    <div class="deck-icon">{deck.icon}</div>
                    <div class="deck-info">
                        <div class="deck-title">{deck.name}</div>
                        <div class="deck-details">
                            <span>{deck.length} cards</span>
                            <span>{new Intl.DateTimeFormat('en-US', { 
                                month: '2-digit', 
                                day: '2-digit', 
                                year: 'numeric' 
                            }).format(deck.lastUpdated)}</span>
                        </div>
                    </div>
                </div>
                {#if $isLoggedIn}
                    <a href="/my-cards"><button class="btn bg-primary-500 card-hover">Buy</button></a>
                {:else}
                    <button class="btn bg-primary-500 card-hover">Login to download</button>
                {/if}
            </div>
        {/each}
    </ul>
</div>