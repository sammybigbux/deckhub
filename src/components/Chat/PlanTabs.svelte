<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let activePlan: "CHOICE" | "FREE" = "CHOICE";
  let activeHoveredPlan: "CHOICE" | "FREE" = activePlan;
  $: isFreeHovered = activeHoveredPlan === "FREE";

  const handleActivePlan = (plan: "CHOICE" | "FREE") => {
    activePlan = plan;
    activeHoveredPlan = plan;

    dispatch("planChange", { plan });
  };

  const handleHoveredActivePlan = (plan: "CHOICE" | "FREE") => {
    activeHoveredPlan = plan;
  };
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="flex items-center lg:justify-center">
  <!-- First Plan (Multiple Choice) -->
  <div
    class="group relative flex items-center justify-center"
    class:p-2={!isFreeHovered}
    class:p-0={isFreeHovered}
    on:mouseenter={() => handleHoveredActivePlan("CHOICE")}
    on:mouseleave={() => handleHoveredActivePlan(activePlan)}
  >
    <button
      class="primary-blue text-xs font-semibold leading-[20px] rounded-3xl px-3 py-2 transition-all duration-300 ease-in-out"
      class:opacity-0={isFreeHovered}
      class:w-0={isFreeHovered}
      class:!p-0={isFreeHovered}
      class:opacity-100={!isFreeHovered}
      class:w-[116px]={!isFreeHovered}
      class:h-9={!isFreeHovered}
      on:click={() => handleActivePlan("CHOICE")}
    >
      <span class:hidden={isFreeHovered} class="text-nowrap"
        >Multiple Choice</span
      >
    </button>
    <div
      class="aspect-square rounded-full bg-primary-600 transition-all duration-300 ease-in-out"
      class:opacity-100={isFreeHovered}
      class:w-5={isFreeHovered}
      class:opacity-0={!isFreeHovered}
      class:w-0={!isFreeHovered}
    />
  </div>

  <!-- Second Plan (Free Response) -->
  <div
    class="group relative flex items-center justify-center"
    class:p-2={isFreeHovered}
    class:p-0={!isFreeHovered}
    on:mouseenter={() => handleHoveredActivePlan("FREE")}
    on:mouseleave={() => handleHoveredActivePlan(activePlan)}
  >
    <button
      class="primary-purple text-xs font-semibold leading-[20px] rounded-3xl px-3 py-2 transition-all duration-300 ease-in-out"
      class:opacity-100={isFreeHovered}
      class:w-[116px]={isFreeHovered}
      class:h-9={isFreeHovered}
      class:opacity-0={!isFreeHovered}
      class:w-0={!isFreeHovered}
      class:!p-0={!isFreeHovered}
      on:click={() => handleActivePlan("FREE")}
    >
      <span class:hidden={!isFreeHovered} class="text-nowrap">
        Free response
      </span>
    </button>
    <div
      class="aspect-square rounded-full bg-tertiary-600 transition-all duration-300 ease-in-out"
      class:opacity-100={!isFreeHovered}
      class:w-5={!isFreeHovered}
      class:opacity-0={isFreeHovered}
      class:w-0={isFreeHovered}
    />
  </div>
</div>
