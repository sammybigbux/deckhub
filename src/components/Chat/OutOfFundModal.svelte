<script>
  import CloseIcon from "../../assets/icons/close.svg";
  import WarningIcon from "../../assets/icons/warning.svg";
  import WarningRedIcon from "../../assets/icons/warning-red.svg";
  import Modal from "../Modal.svelte";
  import { fade } from "svelte/transition";
  import Button from "../Button.svelte";

  export let remainingFreeQuestions;

  $: open = remainingFreeQuestions === 1 || remainingFreeQuestions === 0;
  let delayedOpen = false;

  $: if (open) {
    setTimeout(() => {
      delayedOpen = true;
    }, 1000);
  } else {
    delayedOpen = false;
  }

  const handleClose = () => {
    open = false;
    delayedOpen = false;
  };
</script>

<Modal open={delayedOpen} onClose={handleClose}>
  <div
    class="p-6 w-[324px] bg-[#374151] rounded-3xl flex flex-col gap-2"
    in:fade
    out:fade
  >
    <button type="button" on:click={handleClose} class="self-end">
      <img src={CloseIcon} alt="close" width="10" height="10" />
    </button>

    <div class="flex flex-col gap-8 items-center justify-center">
      <h3 class="font-bold text-base leading-[20px]">
        {remainingFreeQuestions === 0
          ? "Out of funds."
          : "Only a few questions left..."}
      </h3>
      <figure class="shrink-0">
        <img
          src={remainingFreeQuestions === 0 ? WarningRedIcon : WarningIcon}
          alt="warning"
        />
      </figure>

      <p class="text-xs leading-[15px] text-center mt-2">
        {remainingFreeQuestions === 0
          ? "Set up auto recharge for hassle-free studying."
          : "Add to your credit balance soon to continue using smart mode."}
      </p>

      <div class="gap-4 flex flex-col items-center justify-center">
        {#if remainingFreeQuestions === 0}
          <button
            class="flex items-center justify-center gap-2 hover:underline text-primary-500"
          >
            <svg
              width="10"
              height="6"
              viewBox="0 0 10 6"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M3.5 6L0.5 3L3.5 0L4.2 0.7L2.4 2.5H8.5V0.5H9.5V3.5H2.4L4.2 5.3L3.5 6Z"
                fill="#3B82F6"
              />
            </svg>
            <span class="text-primary-500 text-xs leading-[15px]"
              >Return to Standard study mode</span
            >
          </button>
        {/if}
        <Button
          variant="primary-blue"
          className="w-full mt-2"
          handleClick={() => (window.location.href = "/user-info")}
          >Proceed to Payment</Button
        >
      </div>
    </div>
  </div>
</Modal>
