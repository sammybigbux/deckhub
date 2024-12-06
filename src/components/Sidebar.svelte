<script>
  import { page } from "$app/stores";
  import CloseIcon from "../assets/icons/close.svg";
  const activeClass = "!bg-primary-800 !border-none hover:!bg-primary-500";

  $: currentPath = $page.url.pathname;

  export let open = false;
  export let onClose = () => {
    open = !open;
  };
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="fixed inset-0 bg-black/50 z-10"
  on:click={onClose}
  style="display: {open ? 'block' : 'none'}"
/>
<aside
  class="fixed top-0 h-full bg-[#111827] duration-500 {open
    ? 'left-0 '
    : '-left-full ease-in-out'} w-64 p-6 pt-20 z-50 shadow-lg"
>
  <button class="absolute right-4 top-6" on:click={onClose}>
    <img
      src={CloseIcon}
      alt="close"
      class="w-4 aspect-square"
      width="16"
      height="16"
    />
  </button>

  <nav class="flex flex-col gap-6">
    <a
      href="/new/search"
      class={`button outline-blue ${currentPath === "/new/search" ? activeClass : ""}`}
      on:click={onClose}>Marketplace</a
    >
    <a
      href="/about"
      class={`button outline-blue ${currentPath === "/about" ? activeClass : ""}`}
      on:click={onClose}>About</a
    >
    <a
      href="/new/my-cards"
      class={`button outline-blue ${currentPath === "/new/my-cards" ? activeClass : ""}`}
      on:click={onClose}>My Decks</a
    >
    <a
      href="/new/bounty"
      class={`button outline-blue ${currentPath === "/new/bounty" ? activeClass : ""}`}
      on:click={onClose}>Bounty</a
    >
    <a
      href="/user-info"
      class={`button outline-blue ${currentPath === "/user-info" ? activeClass : ""}`}
      on:click={onClose}>Account</a
    >
  </nav>
</aside>
