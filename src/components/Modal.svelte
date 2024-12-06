<script lang="ts">
  import { fade } from "svelte/transition";

  export let open: boolean = false;
  export let onClose: () => void = () => (open = false);

  function handleOverlayClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (target.classList.contains("overlay")) {
      onClose();
    }
  }
</script>

{#if open}
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div
    in:fade={{ duration: 300 }}
    out:fade={{ duration: 300 }}
    class="fixed inset-0 bg-black/30 flex flex-col items-center justify-center gap-10 overlay z-40"
    on:click={handleOverlayClick}
  >
    <slot></slot>
  </div>
{/if}
