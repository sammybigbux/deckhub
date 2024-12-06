<script lang="ts">
  import ProgressBar from "../../components/ProgressBar.svelte";
  import Button from "../../components/Button.svelte";
  import CompletedIcon from "../../assets/icons/check-circle.svg";
  import LockIcon from "../../assets/icons/Lock-Icon.svg";
  import Star from "../../assets/icons/star.svg";

  export let isLocked: boolean = false;
  export let title: string = "Learn";
  export let description: string =
    "Gain new knowledge and familiarity with key terms.";
  export let progressValue: number = 0;
  export let progressMax: number = 0;
  export let standardLink: string = "/learn-multiple";
  export let smartLink: string = "/learn-open";
  export let viewLink: string = "";

  let isCompleted = progressValue === progressMax;

  const handleView = () => {
    window.location.href = viewLink;
  };
</script>

<li>
  <div
    class="relative rounded-3xl px-4 py-6 w-[300px] h-[280px] min-h-[280px] flex flex-col items-center gap-6 text-center mb-6 {isLocked
      ? 'bg-[#1E40AF]/10 text-interface-400'
      : isCompleted
        ? 'bg-[#075B3F]/10 text-interface-50'
        : 'bg-[#3B82F6]/10 duration-300 group-hover:h-[355px] text-interface-50'}"
  >
    <h1 class="title {isLocked ? '!text-interface-400' : ''}">{title}</h1>
    <p class="text-xs leading-[20px]">{description}</p>

    {#if isCompleted}
      <div
        class="flex flex-col gap-6 items-center justify-center w-full mt-auto"
      >
        <figure><img src={CompletedIcon} alt="completed" /></figure>
        <Button
          variant="primary-green"
          handleClick={handleView}
          className="w-full"
        >
          View
        </Button>
      </div>
    {:else if isLocked}
      <figure class="opacity-85"><img src={LockIcon} alt="Locked" /></figure>
    {:else}
      <div
        class="flex flex-col gap-6 items-center w-full text-interface-50 mt-[80px] duration-300 group-hover:mt-0"
      >
        <Button
          variant="primary-green"
          handleClick={handleView}
          className="w-full"
        >
          Overview
        </Button>
        <div
          class="absolute bottom-6 inset-x-0 flex flex-col gap-6 items-center duration-300 transition-opacity opacity-0 group-hover:opacity-100"
        >
          <div class="h-[1px] w-full bg-[#56C0F0]/25" />
          <p class="title">Study</p>
          <div class="flex gap-4 items-center mt-2">
            <a href={standardLink} class="button primary-blue w-full"
              >Standard</a
            >
            <a
              href={smartLink}
              class="button primary-purple w-full flex items-center gap-1"
            >
              <img src={Star} alt="star" />
              <span>Smart</span>
            </a>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <ProgressBar
    max={progressMax}
    value={progressValue}
    {isLocked}
    containerBg="rgba(30,64,175,0.1)"
  />
</li>
