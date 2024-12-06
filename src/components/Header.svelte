<script>
  import { AppBar } from "@skeletonlabs/skeleton";
  import { loginWithGoogle, isLoggedIn } from "$lib/firebase";
  import { page } from "$app/stores";
  import CloseIcon from "../assets/icons/close.svg";
  import Sidebar from "./Sidebar.svelte";

  $: currentPath = $page.url.pathname;

  const activeClass = "!bg-primary-800 !border-none hover:!bg-primary-500";
  let showSidebar = false;

  function toggleSidebar() {
    showSidebar = !showSidebar;
  }

  // let showDropdown = false;

  // function toggleDropdown() {
  //   showDropdown = !showDropdown;
  // }
</script>

<AppBar class="px-12 py-3 !bg-transparent">
  <svelte:fragment slot="lead">
    <div class="flex items-center gap-[40px]">
      <a href="/" class="text-2xl font-bold leading=[36px] text-interface-50"
        >DeckHub</a
      >

      {#if currentPath !== "/new/login"}
        <div class="flex items-center gap-6">
          <!-- <a
            href="/new/search"
            class={`button outline-blue ${currentPath === "/new/search" ? `${activeClass}` : ""}`}
          >
            Marketplace
          </a> -->
          <a
            href="/about"
            class={`button outline-blue ${currentPath === "/about" ? `${activeClass}` : ""}`}
          >
            About
          </a>
        </div>
      {/if}
    </div>
  </svelte:fragment>
  <svelte:fragment slot="trail">
    <nav class="items-center gap-6 hidden lg:flex">
      <!-- {#if $isLoggedIn} -->
      {#if currentPath !== "/new/login"}
        <a
          href="/new/learn/AWS Certified Solutions Architect"
          class={`button outline-blue ${currentPath === "/new/learn/AWS Certified Solutions Architect" ? `${activeClass}` : ""}`}
          >Study</a
        >
        <a
          href="/new/bounty"
          class={`button outline-blue ${currentPath === "/new/bounty" ? `${activeClass}` : ""}`}
          >Feedback</a
        >
        <!-- <a
          href="/user-info"
          class={`button outline-blue ${currentPath === "/user-info" ? `${activeClass}` : ""}`}
          >Account</a
        > -->
      {/if}
      <!-- <button class="profile-icon" on:click={toggleDropdown}>
        <img src="/user_icon.png" alt="Profile" />
      </button> -->
      <!-- {#if showDropdown}
        <div class="dropdown">
          <a href="/user-info#tab0">Payment Information</a>
          <a href="/user-info#tab1">Past Orders</a>
          <a href="/user-info#tab2">Funding</a>
          <a href="/user-info#tab3" on:click={logout}>Log out</a>
        </div>
      {/if} -->
      <!-- {:else} -->
      <!-- {#if currentPath !== "/new/login"}
        <button class="button outline-blue" on:click={loginWithGoogle}
          >Log in</button
        >
      {/if} -->
      <!-- {/if} -->
    </nav>

    <button on:click={toggleSidebar} class="lg:hidden">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="w-6 h-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M4 6h16M4 12h16M4 18h16"
        />
      </svg>
    </button>
  </svelte:fragment>

  <Sidebar onClose={toggleSidebar} open={showSidebar} />
</AppBar>

<!-- <style>
  .login-btn {
    margin-left: 8px;
  }
  .profile-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #ccc;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .dropdown {
    position: absolute;
    top: 50px;
    right: 0;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    padding: 10px;
    z-index: 1000;
  }
  .dropdown a {
    padding: 10px;
    text-decoration: none;
    color: black;
    border-bottom: 1px solid #eee;
  }
  .dropdown a:last-child {
    border-bottom: none;
  }
  .dropdown a:hover {
    background-color: #f5f5f5;
  }
</style> -->
