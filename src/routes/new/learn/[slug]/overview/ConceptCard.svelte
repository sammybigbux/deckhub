<script>
  import CheckIcon from "../../../../../assets/icons/check-circle.svg";
  import { term_from_overview, moduleName, active_section_title } from "../../../../../stores/random_store";
  import { goto } from '$app/navigation';

  export function onStudyClick(title) {
    term_from_overview.set(title);
    goto(`/new/learn/AWS%20Certified%20Solutions%20Architect/open?module=${$moduleName}&section=${$active_section_title}`);
  }
  export let isCompleted = false;
  export let title = "banana";
  export let isChat = false;
</script>

<div
  class="rounded-2xl px-4 py-2 flex items-center justify-between gap-5 {isCompleted
    ? 'bg-[rgba(86,192,240,0.1)]'
    : 'bg-[rgba(59,130,246,0.1)]'}"
>
  <div class="text-xs flex items-center gap-2">
    {#if !isCompleted}
      <span>{title}</span>
    {/if}
    {#if isCompleted}
      <figure class="w-3 aspect-square shrink-0">
        <img src={CheckIcon} alt="checked" class="w-3 aspect-square" />
      </figure>
      <span>{title}</span>
    {/if}
  </div>

  {#if !isCompleted}
    <div
      class="px-2 py-1 rounded-lg bg-primary-600 text-xs font-semibold transform transition duration-200 ease-in-out
        hover:bg-primary-700 hover:scale-105 hover:shadow-md cursor-pointer"
      on:click={() => onStudyClick(title)}
    >
      Study
    </div>
  {/if}
</div>
