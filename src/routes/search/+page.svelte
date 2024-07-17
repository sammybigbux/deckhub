<script lang="ts">
    import { writable, derived } from 'svelte/store';
    import { auth, db, isLoggedIn } from '$lib/firebase';
    import { collection, getDocs, doc, getDoc } from 'firebase/firestore';
    import { onMount } from 'svelte';
    import { userDecks } from '../../stores/auth';

    let searchQuery = writable('');

    interface Deck {
        id?: string;
        icon: string;
        name: string;
        length: number;
        lastUpdated: Date;
    }

    let decks = writable<Deck[]>([]);

    const filteredDecks = derived(
        [searchQuery, decks, isLoggedIn, userDecks],
        ([$searchQuery, $decks, $isLoggedIn, $userDecks]) => {
            // Filter decks
            return $decks.filter(deck =>
                deck.name.toLowerCase().includes($searchQuery.toLowerCase())
            );
        }
    );

    function handleInput(event) {
        searchQuery.set(event.target.value);
    }

    async function handleBuyClick(deckName: string) {
        // Implement the buy logic here
    }

    onMount(async () => {
        try {
            // Fetch all decks
            const querySnapshot = await getDocs(collection(db, 'decks'));
            const deckData: Deck[] = querySnapshot.docs.map((doc) => ({
                ...doc.data(),
                id: doc.id,
                icon: doc.data().icon as string,
                name: doc.data().name as string,
                length: doc.data().length as number,
                lastUpdated: doc.data().lastUpdated.toDate(),
            }));
            decks.set(deckData);

            // Fetch user-owned decks
            const currentUser = auth.currentUser;
            if (currentUser) {
                const userDoc = await getDoc(doc(db, 'users', currentUser.uid));
                if (userDoc.exists()) {
                    const userData = userDoc.data();
                    userDecks.set(userData.decks_owned || []);
                } else {
                    console.log('No such user document!');
                }
            } else {
                console.log('No current user');
            }
        } catch (e) {
            console.error('Error getting documents: ', e);
        }
    });
</script>

<style>
    .owned-deck {
        background-color: #e0ffe0; /* Example color for owned decks */
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
    <input
        type="text"
        class="search-bar"
        placeholder="Search decks..."
        on:input={handleInput}
    />
    <ul class="deck-list">
        {#each $filteredDecks as deck}
            <div class="deck-item { $userDecks.includes(deck.name) ? 'variant-gradient-warning-error' : ''} bg-gradient-to-br variant-gradient-tertiary-secondary">
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
                    {#if $userDecks.includes(deck.name)}
                        <a href="/my-cards" class="btn bg-success-500 card-hover">My Cards</a>
                    {:else}
                        <button 
                            class="btn bg-success-500 card-hover" 
                            on:click={() => handleBuyClick(deck.name)} 
                        >
                            Purchase
                        </button>
                    {/if}
                {:else}
                    <button class="btn bg-primary-500 card-hover">
                        Login to download
                    </button>
                {/if}
            </div>
        {/each}
    </ul>
</div>
