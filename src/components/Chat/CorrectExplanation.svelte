<script>
  export let isCorrect = true;
  export let relatedTerms = [];
  export let handleTermClick = (term) => {};
  export let correct_response_elaboration = ""
  export let incorrect_response_elaboration = ""
</script>

<div class="flex flex-col items-center justify-center gap-4 text-white">
  {#if isCorrect}
    <div class="primary-blue font-bold py-3 text-center rounded-3xl w-full text-base">
      Correct Explanation
    </div>
  {:else}
    <div class="primary-red font-bold py-3 text-center rounded-3xl w-full text-base">
      Correct Explanation
    </div>
  {/if}

  <div
    class="px-4 py-3 rounded-3xl w-full border border-[#56C0F0]/25 text-xs leading-[20px]"
  >
    {#if isCorrect}
      {correct_response_elaboration}
    {:else}
      {incorrect_response_elaboration}
    {/if}
  </div>

  <div class="bg-interface-900 p-4 flex flex-col gap-6 items-center justify-center w-full rounded-[32px]">
    <h4 class="font-bold leading-[20px] text-base">Related Terms</h4>

    <ul class="flex flex-wrap gap-4 max-w-[299px] justify-center">
      {#each relatedTerms as term (term)}
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
</div>
