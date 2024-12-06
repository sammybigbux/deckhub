<script lang="ts">
  import { writable, derived } from "svelte/store";
  import { isLoggedIn, idToken, userName } from "$lib/firebase"; // Import auth and userName here
  import { onMount } from "svelte";
  import { userDecks } from "../../stores/auth";
  import { createCheckoutSession } from "$lib/stripe";

  const isLocalhost = false;
  const base_url = isLocalhost
    ? "http://localhost:8080" // Your local backend URL
    : "https://deckhub-backend-1086653848406.us-central1.run.app";

  let searchQuery = writable("");

  interface Deck {
    id?: string;
    icon: string;
    name: string;
    length: number;
    lastUpdated: Date;
  }

  let decks = writable<Deck[]>([]);
  let loaded = writable(false);
  userDecks.subscribe((value) => console.log("userDecks value:", value));

  // Derive userDisplayName from userName
  const userDisplayName = derived(userName, ($userName) =>
    $userName ? $userName.split(" ")[0] : "User"
  );
  console.log("userDisplayName derived from userName:", $userDisplayName);

  const filteredDecks = derived(
    [searchQuery, decks, isLoggedIn, userDecks],
    ([$searchQuery, $decks, $isLoggedIn, $userDecks]) => {
      // Filter decks
      if (!$isLoggedIn || !$userDecks) return [];
      return $decks.filter((deck) =>
        deck.name.toLowerCase().includes($searchQuery.toLowerCase())
      );
    }
  );

  function handleInput(event) {
    searchQuery.set(event.target.value);
  }

  async function handlePurchase(product_name) {
    const productId = "prod_QxWysKGQWOT3ft";
    const priceId = "price_1Q5bu4FKyW9aNIed3s7e8GYF";

    // Call the function from the stripe.js file
    await createCheckoutSession(productId, priceId, product_name);
  }

  onMount(async () => {
    try {
      console.log("Fetching all decks...");
      const response = await fetch(`${base_url}/get_decks`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch decks");
      }

      const deckData: Deck[] = await response.json();
      decks.set(deckData);
      console.log("All Deck Data:", deckData);

      // Wait for idToken to be set before fetching user decks
      idToken.subscribe(async (token) => {
        if (token && isLoggedIn) {
          console.log("Fetching user decks...");
          console.log(
            "Sending this authorization token to get_user_decks: ",
            token
          );

          const userResponse = await fetch(`${base_url}/get_user_decks`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          });

          if (!userResponse.ok) {
            throw new Error("Failed to fetch user decks");
          }

          const userDeckData = await userResponse.json();
          userDecks.set(userDeckData);

          loaded.set(true);
        } else {
          userDecks.set([]);
        }
      });
    } catch (e) {
      console.error("Error getting decks:", e);
    }
  });
</script>

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
      <div
        class="deck-item"
        class:bg-gradient-to-br={true}
        class:variant-gradient-warning-error={$userDecks.includes(deck.name)}
        class:variant-filled-tertiary={!$userDecks.includes(deck.name)}
      >
        <div class="deck-content">
          <div class="deck-icon">{deck.icon}</div>
          <div class="deck-info">
            <div class="deck-title">{deck.name}</div>
            <div class="deck-details">
              <span>{deck.length} cards</span>
            </div>
          </div>
        </div>
        <button
          class="btn"
          class:variant-filled-success={$userDecks.includes(deck.name)}
          class:variant-filled-error={!$userDecks.includes(deck.name)}
          on:click={() => {
            if (!$userDecks.includes(deck.name)) {
              handlePurchase(deck.name);
            }
          }}
        >
          {$userDecks.includes(deck.name) ? "Open" : "Purchase"}
        </button>
      </div>
    {/each}
  </ul>
</div>

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
