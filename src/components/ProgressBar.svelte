<script>
  export let value = 0;
  export let max = 0;
  export let isLocked = false;
  export let isActiveLabel = false;
  export let isVertical = true;
  export let containerBg = "rgba(59,130,246,0.1)";
  export let progressBg = "radial-gradient(at right, #57CFA7 0%, #0B8C61 100%)";
  export let borderRadius = "1.5rem"; // 24px
  export let height = "16px";
  export let width = "100%";
  export let labelSize = "16px";
  export let labelWeight = "600";
  export let labelName = "sections";
  export let containerClass = "";
  export let progressClass = "";

  $: isCompleted = value === max;

  $: label = `
      <span style="color: ${isActiveLabel && value ? "#0FBA81" : "#F9FAFB"};">
        ${value}
      </span> / ${max} ${labelName}`;
</script>

<div
  class="flex {isVertical
    ? 'flex-col gap-4'
    : 'flex-row gap-6'} items-center justify-center w-full text-interface-50 max-h-[52px] {`${containerClass}`}"
  style="border-radius: {borderRadius};"
>
  <div
    class="relative shrink-0 {progressClass}"
    style="background-color: {containerBg}; border-radius: {borderRadius}; height: {height}; width: {width};"
  >
    <div
      class="absolute inset-y-0 left-0 rounded-3xl duration-300 ease-linear {isCompleted
        ? ''
        : 'rounded-r-none'}"
      style="background: {progressBg}; width: {isLocked
        ? 0
        : (value / max) * 100}%;"
    />
  </div>
  <p
    class="shrink-0 {isLocked ? 'text-interface-400' : 'text-interface-50'}"
    style="font-size: {labelSize}; font-weight: {labelWeight};"
  >
    {#if isLocked}
      Locked
    {:else if isCompleted}
      Completed
    {:else}
      {@html label}
    {/if}
  </p>
</div>
