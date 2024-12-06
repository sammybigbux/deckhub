<script>
  export let question = "";
  export let options = [];
  export let correctOption = 0;
  export let relatedTerms = [];
  export let handleOptionClick = (
    chosenIndex,
    correctIndex,
    answer,
    relatedTerms
  ) => {};
  export let sectionName = ""
</script>

<div class="flex flex-col gap-6 text-white">
  <div class="flex flex-col gap-4">
    <h4 class="font-bold leading-[20px] text-base">Question - {sectionName}</h4>
    <p class="text-xs leading-[20px] font-bold">{question}</p>
  </div>

  <ul class="flex flex-col gap-2">
    {#each options as option, index (option)}
      <li>
        <button
          class="outline-blue text-xs leading-[20px] px-4 py-2 w-full rounded-[16px] text-left font-normal"
          on:click={() =>
            handleOptionClick(index, correctOption, option, relatedTerms)}
        >
          {@html option}
        </button>
      </li>
    {/each}
  </ul>
</div>
