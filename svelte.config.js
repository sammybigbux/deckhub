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
      entries: [
        '/', // Your homepage
        '/new/learn/AWS%20Certified%20Solutions%20Architect',
        '/new/learn/AWS%20Certified%20Solutions%20Architect/overview',
        '/new/learn/AWS%20Certified%20Solutions%20Architect/open'
      ]
    }
  }
};

export default config;
