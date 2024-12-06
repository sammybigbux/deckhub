<script lang="ts">
  import { page } from "$app/stores";
  import { get } from "svelte/store";
  import ExamOverlay from "./ExamOverlay.svelte";
  import Button from "./Button.svelte";
  import ProgressBar from "./ProgressBar.svelte";

  export let deck;
  export let isOwned = false;
  export let openId;
  export let setOpenId: (id: string | null) => void;
  export let handlePurchase: () => void;

  const isMyDecksPage = get(page).url.pathname.slice(1) === "new/my-cards";

  function openOverlay() {
    setOpenId(deck.id);
  }

  function closeOverlay() {
    setOpenId(null);
  }
</script>

<li class="w-full max-w-screen-lg flex flex-col mx-auto">
  <div
    class="rounded-3xl flex flex-col w-full h-full 3xl:max-w-[538px] bg-[rgba(59,130,246,0.1)] {isMyDecksPage
      ? 'mb-6'
      : ''}"
  >
    <ExamOverlay
      exam={deck}
      open={openId === deck.id}
      close={closeOverlay}
      purchase={handlePurchase}
      {isOwned}
    />

    <figure
      class="w-full h-[184px] aspect-[538/184] rounded-t-3xl overflow-hidden"
    >
      {#if deck.icon}
        <span class="w-full h-full flex items-center justify-center text-7xl">
          {deck.icon}
        </span>
      {:else}
        <img
          src={deck.image}
          alt={deck.name}
          class="w-full h-full object-cover"
        />
      {/if}
    </figure>

    <div class="p-6 flex flex-col gap-10 text-interface-50 max-2xl:gap-6">
      <div>
        <div class="flex items-start justify-between gap-5">
          <h3 class="!font-semibold text-2xl leading-[28px]">{deck.name}</h3>
          {#if !isMyDecksPage}
            <p class="font-semibold text-base leading-[20px] shrink-0">
              {deck.length} Sections
            </p>
          {/if}
          {#if isMyDecksPage}
            <p class="font-semibold text-base leading-[20px] shrink-0">
              {deck.completedSections === deck.length
                ? "Completed"
                : deck.estimatedEndDate.toLocaleDateString()}
            </p>
          {/if}
        </div>

        <p class="text-xs italic leading-[20px] mt-2">
          Last updated {new Date(deck.lastUpdated).toLocaleDateString()}
        </p>
      </div>

      <div class="flex items-center gap-6 w-full">
        <Button
          variant="outline-blue"
          className="w-[233px] h-[44px]"
          handleClick={openOverlay}
        >
          Learn More
        </Button>

        <Button
          variant={`${isOwned ? "primary-blue" : "primary-green"}`}
          className="w-[233px] h-[44px]"
          handleClick={handlePurchase}
        >
          {isOwned ? "View" : "Purchase"}
        </Button>
      </div>
    </div>
  </div>

  {#if isMyDecksPage}
    <ProgressBar value={+deck.completedSections} max={+deck.length} />
  {/if}
</li>
