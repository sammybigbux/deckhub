import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  extensions: ['.svelte'],
  preprocess: [vitePreprocess()],
  
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: 'index.html' // Ensures SPA behavior
    }),
    prerender: {
      entries: ['*'] // Ensures that all routes are prerendered at build time
    }
  }
};

export default config;
