<script lang="ts">
  import { writable, derived } from "svelte/store";
  import { isLoggedIn, idToken, userName } from "$lib/firebase";
  import { onMount } from "svelte";
  import SearchBar from "../../../components/SearchBar.svelte";
  import ArrowDown from "../../../assets/icons/arrow-down.svg";
  import DeckCard from "../../../components/DeckCard.svelte";
  import { demoDeckDetails, DUMMY_CARDS } from "../demoDeck";

  let searchQuery = writable("");

  interface Deck {
    id?: string;
    icon?: string;
    name?: string;
    length?: number;
    lastUpdated?: Date;
  }

  let allDecks = writable<Deck[]>([]);
  let userOwnedDeckNames = writable<string[]>([]);
  let openId: string | null = null;

  const filteredDecks = derived(
    [searchQuery, allDecks, userOwnedDeckNames],
    ([$searchQuery, $allDecks, $userOwnedDeckNames]) => {
      let userDecks = $allDecks.filter(
        (deck) => deck.name && $userOwnedDeckNames.includes(deck.name)
      );
      if ($searchQuery.trim() === "") {
        return userDecks;
      } else {
        return userDecks.filter(
          (deck) =>
            deck.name &&
            deck.name.toLowerCase().includes($searchQuery.toLowerCase())
        );
      }
    }
  );

  function handleInput(event) {
    searchQuery.set(event.target.value);
  }

  function handleView(deckId?: string) {
    window.location.href = `/new/learn/${deckId}`;
  }

  onMount(async () => {
    try {
      // Fetch all decks from the backend
      console.log("Fetching all decks...");
      const decksResponse = await fetch(
        "https://deckhub-backend-1086653848406.us-central1.run.app/get_decks",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!decksResponse.ok) {
        throw new Error("Failed to fetch decks");
      }

      const deckData = await decksResponse.json();
      console.log("All Deck Data:", deckData);

      // Convert lastUpdated from Firestore Timestamp to JS Date
      const convertedDecks: Deck[] = deckData.map((deck: any) => ({
        ...deck,
        lastUpdated: deck.lastUpdated
          ? new Date(deck.lastUpdated.seconds * 1000)
          : new Date(), // Convert to JS Date
      }));

      allDecks.set(convertedDecks);

      // Wait for idToken to be set before fetching user-owned decks
      idToken.subscribe(async (token) => {
        if (token && isLoggedIn) {
          console.log("Fetching user decks...");
          console.log(
            "Sending this authorization token to get_user_decks: ",
            token
          );

          const userResponse = await fetch(
            "https://deckhub-backend-1086653848406.us-central1.run.app/get_user_decks",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          );

          if (!userResponse.ok) {
            throw new Error("Failed to fetch user decks");
          }

          const userDeckNames = await userResponse.json();
          console.log("User Deck Names:", userDeckNames);

          userOwnedDeckNames.set(userDeckNames);
        } else {
          userOwnedDeckNames.set([]);
        }
      });
    } catch (e) {
      console.error("Error getting decks:", e);
    }
  });

  // Access the value using $userName and derive userDisplayName
  const userDisplayName = derived(
    userName,
    ($userName) => $userName.split(" ")[0]
  );
  console.log("userDisplayName derived from userName:", $userDisplayName);
</script>

<div
  class="py-[40px] px-8 lg:px-[50px] 2xl:px-[402px] flex flex-col items-center justify-center"
>
  <h1 class="font-bold text-4xl mb-[40px] max-2xl:mb-[25px]">My Decks</h1>
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
        deck={{
          ...deck,
          ...demoDeckDetails,
          estimatedEndDate: new Date(),
          completedSections: 100,
        }}
        {openId}
        setOpenId={(id) => (openId = id)}
        handlePurchase={() => handleView(deck.name)}
        isOwned={true}
      />
    {/each}
  </ul>
</div>
