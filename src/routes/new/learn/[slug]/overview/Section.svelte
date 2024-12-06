<script lang="ts">
  import Button from "../../../../../components/Button.svelte";
  import VerticalLine from "./VerticalLine.svelte";

  export let title: string = "Section";
  export let isEndSection: boolean = false;
  export let isCompleted: boolean = false;
  export let isActive: boolean = false;
  export let handleSectionClick: () => void;
</script>

<Button
  variant={isCompleted
    ? "secondary-green"
    : isActive
      ? "secondary-blue"
      : "secondary-purple"}
  className="w-full !opacity-100 h-[44px]"
  disabled={!isActive}
  on:click={handleSectionClick}
>
  {title}
</Button>

{#if !isEndSection}
  <VerticalLine {isCompleted} />
{/if}
