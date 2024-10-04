<script lang="ts">
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    
    // Create writable store to manage active tab state
    const tabSet = writable(0);

    // Update tab based on the URL hash
    onMount(() => {
        const hash = window.location.hash;
        if (hash) {
            const tabIndex = parseInt(hash.replace('#tab', ''), 10);
            if (!isNaN(tabIndex)) {
                tabSet.set(tabIndex);
            }
        }
    });
</script>

<style>
  body, html {
    margin: 0;
    padding: 0;
    height: 100%;
  }

  .center-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    height: 100vh;
    padding-top: 15vh; /* Adjust top position of card */
  }

  .card {
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    width: 100%;
    max-width: 800px; /* Adjust the card width */
  }

  /* Card header with tab navigation */
  .card-header {
    display: flex;
    justify-content: space-around;
    padding-bottom: 16px;
    border-bottom: 2px solid #f0f0f0;
  }

  /* Style for individual tabs */
  .tab {
    cursor: pointer;
    padding: 10px 20px;
    border: 1px solid transparent;
    border-radius: 5px;
    transition: background-color 0.2s, color 0.2s;
    background-color: #2c4a66; /* Darker gray for tab boxes */
  }

  .tab-active {
    background-color: #007bff; /* Active tab background */
    color: white;
    font-weight: bold;
  }

  .tab:hover {
    background-color: #554c4c; /* Slightly darker on hover */
  }

  .card-content {
    padding: 20px;
  }

  .bg-primary-500 {
    background-color: #007bff;
    color: white;
  }

  .bg-secondary-500 {
    background-color: #6c757d;
    color: white;
  }

</style>

<div class="center-container">
  <div class="card">
    <!-- Tabs Header -->
    <div class="card-header">
        <div class="tab {($tabSet === 0) ? 'tab-active' : ''}" on:click={() => tabSet.set(0)}>
            Payment Information
        </div>
        <div class="tab {($tabSet === 1) ? 'tab-active' : ''}" on:click={() => tabSet.set(1)}>
            Past Orders
        </div>
        <div class="tab {($tabSet === 2) ? 'tab-active' : ''}" on:click={() => tabSet.set(2)}>
            Funding
        </div>
        <div class="tab {($tabSet === 3) ? 'tab-active' : ''}" on:click={() => tabSet.set(3)}>
            Log out
        </div>
    </div>

    <!-- Tab Content -->
    <div class="card-content">
      {#if $tabSet === 0}
        <div class="tab-content">
            <h2>Payment Information</h2>
            <p>Here you will see your payment information.</p>
        </div>
      {/if}

      {#if $tabSet === 1}
        <div class="tab-content">
            <h2>Past Orders</h2>
            <p>Here you will see your past orders.</p>
        </div>
      {/if}

      {#if $tabSet === 2}
        <div class="tab-content">
            <h2>Funding</h2>
            <p>Here you will manage your funding options.</p>
        </div>
      {/if}

      {#if $tabSet === 3}
        <div class="tab-content">
            <h2>Log out</h2>
            <p>You will log out of your account here.</p>
        </div>
      {/if}
    </div>
  </div>
</div>
