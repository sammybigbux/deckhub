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

    import { initializeApp } from 'firebase/app';
    import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from 'firebase/auth';
    import { isLoggedIn } from '../stores/auth'; // Import the shared store

	const firebaseConfig = {
		apiKey: "AIzaSyC-ZOP0oH3IISFl3Qwzc7rGnbEB5VwYOps",
		authDomain: "deckhubapp.firebaseapp.com",
		projectId: "deckhubapp",
		storageBucket: "deckhubapp.appspot.com",
		messagingSenderId: "1086653848406",
		appId: "1:1086653848406:web:ad7fa7ec34c3061cc694f7"
	};

    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    const provider = new GoogleAuthProvider();

    async function loginWithGoogle() {
        try {
            const result = await signInWithPopup(auth, provider);
            const user = result.user;
            console.log('User signed in:', user);
            isLoggedIn.set(true);
        } catch (error) {
            console.error('Error during sign-in:', error);
        }
    }

    onAuthStateChanged(auth, (user) => {
        if (user) {
            isLoggedIn.set(true);
        } else {
            isLoggedIn.set(false);
        }
    });
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
                    class="btn btn-md variant-ghost-primary"
                    href="/search"
                    target="_blank"
                    rel="noreferrer"
                >
                    Search
                </a>
                {#if $isLoggedIn}
                    <button class="btn btn-md variant-ghost-secondary login-btn">
                        My Decks
                    </button>
                {:else}
                    <button class="btn btn-md variant-ghost-secondary login-btn" on:click={loginWithGoogle}>
                        Log in
                    </button>
                {/if}
                <a
                    class="btn btn-md variant-ghost-tertiary"
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
