<script lang="ts">
    import { writable, derived } from 'svelte/store';
    import { isLoggedIn, idToken, userName } from '$lib/firebase';
    import { onMount } from 'svelte';

    let searchQuery = writable('');

    interface Deck {
        id?: string;
        icon?: string;
        name?: string;
        length?: number;
        lastUpdated?: Date;
    }

    let allDecks = writable<Deck[]>([]);
    let userOwnedDeckNames = writable<string[]>([]);

    const filteredDecks = derived(
        [searchQuery, allDecks, userOwnedDeckNames],
        ([$searchQuery, $allDecks, $userOwnedDeckNames]) => {
            let userDecks = $allDecks.filter(deck => 
                deck.name && $userOwnedDeckNames.includes(deck.name)
            );
            if ($searchQuery.trim() === '') {
                return userDecks;
            } else {
                return userDecks.filter(deck =>
                    deck.name && deck.name.toLowerCase().includes($searchQuery.toLowerCase())
                );
            }
        }
    );

    function handleInput(event) {
        searchQuery.set(event.target.value);
    }

    onMount(async () => {
        try {
            // Fetch all decks from the backend
            console.log('Fetching all decks...');
            const decksResponse = await fetch('http://127.0.0.1:5000/get_decks', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!decksResponse.ok) {
                throw new Error('Failed to fetch decks');
            }

            const deckData = await decksResponse.json();
            console.log('All Deck Data:', deckData);

            // Convert lastUpdated from Firestore Timestamp to JS Date
            const convertedDecks: Deck[] = deckData.map((deck: any) => ({
                ...deck,
                lastUpdated: deck.lastUpdated ? new Date(deck.lastUpdated.seconds * 1000) : new Date(), // Convert to JS Date
            }));

            allDecks.set(convertedDecks);

            // Wait for idToken to be set before fetching user-owned decks
            idToken.subscribe(async (token) => {
                if (token && isLoggedIn) {
                    console.log('Fetching user decks...');
                    console.log('Sending this authorization token to get_user_decks: ', token);

                    const userResponse = await fetch('http://127.0.0.1:5000/get_user_decks', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (!userResponse.ok) {
                        throw new Error('Failed to fetch user decks');
                    }

                    const userDeckNames = await userResponse.json();
                    console.log('User Deck Names:', userDeckNames);

                    userOwnedDeckNames.set(userDeckNames);
                } else {
                    userOwnedDeckNames.set([]);
                }
            });

        } catch (e) {
            console.error('Error getting decks:', e);
        }
    });

    // Access the value using $userName and derive userDisplayName
    const userDisplayName = derived(userName, $userName => $userName.split(' ')[0]);
    console.log('userDisplayName derived from userName:', $userDisplayName);
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
    <h1>{$userDisplayName}'s Decks</h1>
    <input
        type="text"
        class="search-bar"
        placeholder="Search decks..."
        on:input={handleInput}
    />
    <ul class="deck-list">
        {#each $filteredDecks as deck}
            <div class="deck-item bg-gradient-to-br variant-gradient-warning-error">
                <div class="deck-content">
                    <div class="deck-icon">{deck.icon}</div>
                    <div class="deck-info">
                        <div class="deck-title">{deck.name}</div>
                        <div class="deck-details">
                            <span>{deck.length} ideas</span>
                        </div>
                    </div>
                </div>
                <button class="btn bg-success-500 card-hover">Download</button>
            </div>
        {/each}
    </ul>
</div>
