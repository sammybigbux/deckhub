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

    import { loginWithGoogle, isLoggedIn, logout } from '$lib/firebase'
</script>

<style>
    .login-btn {
        margin-left: 8px;
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
                <button class="btn btn-md variant-glass-tertiary login-btn" on:click={logout}>
                    Log out
                </button>
                {:else}
                    <button class="btn btn-md variant-glass-secondary login-btn" on:click={loginWithGoogle}>
                        Log in
                    </button>
                {/if}
                <a
                    class="btn btn-md variant-glass-success"
                    href="https://github.com/sammybigbux/deckhub/blob/main/README.md"
                    target="_blank"
                    rel="noreferrer"
                >
                    GitHub
                </a>
            </svelte:fragment>
        </AppBar>
    </svelte:fragment>
    <!-- Page Route Content -->
    <slot />
</AppShell>
