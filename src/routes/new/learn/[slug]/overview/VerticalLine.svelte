<script>
  import DotedLine from "../../../../../assets/learn-overview/dotted-line.png";

  export let isCompleted = false;
</script>

{#if isCompleted}
  <div class="border h-6 border-primary-600" />
{:else}
  <figure><img src={DotedLine} alt="vertical line" /></figure>
{/if}
