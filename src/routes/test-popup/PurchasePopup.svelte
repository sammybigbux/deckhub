<script lang="ts">
  import type { SvelteComponent } from 'svelte';

  // Skeleton Modal Store
  import { getModalStore } from '@skeletonlabs/skeleton';

  // Props
  /** Title of the modal */
  export let title: string = "Default Title";

  /** Report content containing concepts, terms, and time saved */
  export let report_content: {
    "Concepts to review": string[];
    "Terms to review": string[];
    "time saved": string;
  } = {
    "Concepts to review": ["Concept A", "Concept B", "Concept C"],
    "Terms to review": ["Term 1", "Term 2", "Term 3"],
    "time saved": "2 hours"
  };

  const modalStore = getModalStore();
</script>

{#if $modalStore[0]}
  <div class="modal-example-fullscreen bg-surface-100-800-token w-screen h-screen p-4 flex flex-col items-center space-y-8">
    <!-- Modal Header -->
    <div class="text-center">
      <h2 class="h2 text-4xl font-bold mb-4">Final Report</h2>
      <h3 class="text-xl font-semibold text-gray-600">{title}</h3>
    </div>

    <!-- Report Content -->
    <div class="space-y-8 w-3/4">
      <!-- Concepts to Review -->
      <section>
        <h4 class="text-2xl font-bold text-primary-500 mb-4">Concepts to Review</h4>
        <ul class="list-disc list-inside space-y-2">
          {#each report_content["Concepts to review"] as concept}
            <li class="text-primary-500 text-lg font-medium">{concept}</li>
          {/each}
        </ul>
      </section>

      <!-- Terms to Review -->
      <section>
        <h4 class="text-2xl font-bold text-primary-500 mb-4">Terms to Review</h4>
        <ul class="list-disc list-inside space-y-2">
          {#each report_content["Terms to review"] as term}
            <li class="text-primary-500 text-lg font-medium">{term}</li>
          {/each}
        </ul>
      </section>

      <!-- Time Saved -->
      <section>
        <h4 class="text-2xl font-bold text-primary-green mb-4">Time Saved</h4>
        <p class="text-primary-green text-3xl font-bold">{report_content["time saved"]}</p>
      </section>
    </div>

    <!-- Close Button -->
    <button class="btn variant-filled" on:click={() => modalStore[0].close()}>× Close</button>
  </div>
{/if}
