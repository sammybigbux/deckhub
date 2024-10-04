<script lang="ts">
    import '../app.postcss';
    import { AppShell, AppBar } from '@skeletonlabs/skeleton';

    // Highlight JS
    import hljs from 'highlight.js/lib/core';
    import 'highlight.js/styles/github-dark.css';
    import { storeHighlightJs } from '@skeletonlabs/skeleton';
    import xml from 'highlight.js/lib/languages/xml'; // for HTML
    import css from 'highlight.js/lib/languages/css';
    import javascript from 'highlight.js/lib/languages/javascript';
    import typescript from 'highlight.js/lib/languages/typescript';

    hljs.registerLanguage('xml', xml); // for HTML
    hljs.registerLanguage('css', css);
    hljs.registerLanguage('javascript', javascript);
    hljs.registerLanguage('typescript', typescript);
    storeHighlightJs.set(hljs);

    // Floating UI for Popups
    import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
    import { storePopup } from '@skeletonlabs/skeleton';
    storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

    import { loginWithGoogle, isLoggedIn, logout } from '$lib/firebase';

    // Dropdown visibility
    let showDropdown = false;

    function toggleDropdown() {
        showDropdown = !showDropdown;
    }
</script>

<style>
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
</style>

<!-- App Shell -->
<AppShell>
    <svelte:fragment slot="header">
        <!-- App Bar -->
        <AppBar>
            <svelte:fragment slot="lead">
                <a href="/"><strong class="text-xl uppercase">DECKHUB</strong></a>
            </svelte:fragment>
            <svelte:fragment slot="trail">
                <a
                    class="btn btn-md variant-glass-primary"
                    href="/search"
                >
                    Search
                </a>
                {#if $isLoggedIn}
                <a href="/my-cards">
                    <button class="btn btn-md variant-glass-secondary login-btn">
                        My Decks
                    </button>
                </a>
                <a href="/learn">
                    <button class="btn btn-md variant-glass-error login-btn">
                        Learn
                    </button>
                </a>
                <a
                    class="btn btn-md variant-glass-success"
                    href="/bounty"
                >
                    Bounty
                </a>
                <div class="profile-icon" on:click={toggleDropdown}>
                    <img src="/user_icon.png" alt="Profile" />
                </div>
                {#if showDropdown}
                    <div class="dropdown">
                        <!-- Each link has a hash that corresponds to a tab index -->
                        <a href="/user-info#tab0">Payment Information</a>
                        <a href="/user-info#tab1">Past Orders</a>
                        <a href="/user-info#tab2">Funding</a>
                        <a href="/user-info#tab3" on:click={logout}>Log out</a>
                    </div>
                {/if}
                {:else}
                    <button class="btn btn-md variant-glass-secondary login-btn" on:click={loginWithGoogle}>
                        Log in
                    </button>
                {/if}
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>
    <!-- Page Route Content -->
    <slot />
</AppShell>

