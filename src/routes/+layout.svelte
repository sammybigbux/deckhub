<script lang="ts">
  import '../app.postcss';
  import { AppShell } from '@skeletonlabs/skeleton';
  import Header from '../components/Header.svelte';
  import { isLoggedIn } from '$lib/firebase';
  import { page } from "$app/stores";
  import { initializeStores, Modal } from '@skeletonlabs/skeleton';

  // Highlight JS
  import hljs from 'highlight.js/lib/core';
  import 'highlight.js/styles/github-dark.css';
  import { storeHighlightJs } from '@skeletonlabs/skeleton';
  import xml from 'highlight.js/lib/languages/xml'; // for HTML
  import css from 'highlight.js/lib/languages/css';
  import javascript from 'highlight.js/lib/languages/javascript';
  import typescript from 'highlight.js/lib/languages/typescript';

  hljs.registerLanguage('xml', xml);
  hljs.registerLanguage('css', css);
  hljs.registerLanguage('javascript', javascript);
  hljs.registerLanguage('typescript', typescript);
  storeHighlightJs.set(hljs);
  initializeStores();

  // Floating UI for Popups
  import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
  import { storePopup } from '@skeletonlabs/skeleton';
  storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

  let moduleName= "";
  let sectionName = "";

  $: slug = $page.params.slug;

  $: {
    const searchParams = new URLSearchParams($page.url.search);
    moduleName = searchParams.get("module");
    sectionName = searchParams.get("section");
  }
</script>

<!-- App Shell -->
<Modal>
</Modal>

<AppShell class="main-bg">
  
  {#if $isLoggedIn && !(moduleName && sectionName)} 
      <Header slot="header" />
  {/if}

  <!-- Page Route Content -->
  <slot />
</AppShell>
