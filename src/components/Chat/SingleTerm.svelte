<script>
  export let title = "";
  export let message =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
  export let concepts = [];
  export let restTerms = [];
  export let handleTermClick = () => {};
  export let handleRTClick = () => {};
</script>

<div class="flex flex-col gap-8 text-white">
  <div class="flex flex-col gap-[28px] w-full">
    <h4 class="font-bold leading-[20px] text-base">{title}</h4>
    <p class="text-xs leading-[20px] w-full">{message}</p>
  </div>

  {#if restTerms.length}
    <div
      class="bg-interface-900 p-4 flex flex-col gap-6 items-center justify-center w-full rounded-[32px]"
    >
      <h4 class="font-bold leading-[20px] text-base">Commonly associated with</h4>
      <ul class="flex flex-wrap gap-4 max-w-[750px] justify-center">
        {#each concepts as term (term)}
          <li>
            <button
              class="outline-blue text-xs font-semibold leading-[20px] px-5 py-3 rounded-3xl"
              on:click={() => handleRTClick(term)}
            >
              {term}
            </button>
          </li>
        {/each}
      </ul>
      <h4 class="font-bold leading-[20px] text-base">Other terms related to this question</h4>
      <ul class="flex flex-wrap gap-4 max-w-[750px] justify-center">
        {#each restTerms.slice(0, 3) as term (term)}
          <li>
            <button
              class="outline-blue text-xs font-semibold leading-[20px] px-5 py-3 rounded-3xl"
              on:click={() => handleTermClick(term)}
            >
              {term}
            </button>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</div>

