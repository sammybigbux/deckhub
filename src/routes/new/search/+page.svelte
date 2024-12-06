<script lang="ts">
  import { writable, derived } from "svelte/store";
  import { isLoggedIn, idToken, userName } from "$lib/firebase"; // Import auth and userName here
  import { onMount } from "svelte";
  import { userDecks } from "../../../stores/auth";
  import { createCheckoutSession } from "$lib/stripe";
  import ArrowDown from "../../../assets/icons/arrow-down.svg";
  import SearchBar from "../../../components/SearchBar.svelte";
  import DeckCard from "../../../components/DeckCard.svelte";
  import { demoDeckDetails, DUMMY_CARDS } from "../demoDeck";

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
  let openId: string | null = null;

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

  function handleView(deckId?: string) {
    window.location.href = `/new/learn/${deckId}`;
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

<div
  class="py-[40px] px-8 lg:px-[50px] 2xl:px-[402px] flex flex-col items-center justify-center"
>
  <h1 class="font-bold text-4xl mb-[40px] max-2xl:mb-[25px]">Marketplace</h1>
  <SearchBar
    placeholder="Search"
    bind:value={$searchQuery}
    onInput={handleInput}
  />

  <button
    class="flex items-center gap-2 text-[16px] font-bold text-primary-500 capitalize ml-auto mt-6 mb-[73px] max-2xl:mb-5"
  >
    filter
    <figure><img src={ArrowDown} alt="arrow" class="w-2" /></figure>
  </button>

  <ul class="grid gap-[40px] 2xl:grid-cols-2">
    {#each [...$filteredDecks, ...DUMMY_CARDS] as deck}
      <DeckCard
        deck={{ ...deck, ...demoDeckDetails }}
        {openId}
        setOpenId={(id) => (openId = id)}
        handlePurchase={() => {
          if (
            ![...$userDecks, "AWS Certified Solutions Architect"].includes(
              deck.name
            )
          ) {
            handlePurchase(deck.name);
          } else {
            handleView(deck.name);
          }
        }}
        isOwned={[...$userDecks, "AWS Certified Solutions Architect"].includes(
          deck.name
        )}
      />
    {/each}
  </ul>
</div>
