<script>
  export let isCorrect = true;
  export let handleExplainClick = () => {};
  export let correct_response_explanation = "";
  export let incorrect_response_explanation = "";
</script>

<div class="flex flex-col items-center justify-center gap-4 text-white">
  {#if isCorrect}
    <div
      class="bg-primary-600 text-white font-bold py-3 text-center rounded-3xl w-full text-base"
    >
      Correct
    </div>
  {:else}
    <div
      class="bg-error-700 text-white font-bold py-3 text-center rounded-3xl w-full text-base"
    >
      Incorrect
    </div>
  {/if}

  <div
    class="px-4 py-3 rounded-3xl w-full border border-[#56C0F0]/25 text-xs leading-[20px]"
  >
  {#if isCorrect}
    {correct_response_explanation}
  {:else}
    {incorrect_response_explanation}
  {/if}
  </div>

  <button
    class="outline-blue text-xs font-semibold leading-[20px] px-5 py-3 w-full rounded-[16px] text-center"
    on:click={() => handleExplainClick()}>Explanation</button
  >
</div>
