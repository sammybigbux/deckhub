<script>
  import { fade } from 'svelte/transition';
  import { createCheckoutSession } from "$lib/stripe";

  // Props to receive data from the parent component
  export let correct_of_twenty = 0;
  export let strongConcepts = ["Concept 1", "Concept 2"];
  export let strongTerms = ["Term 1", "Term 2"];
  export let weakConcepts = ["Concept 3", "Concept 4"];
  export let weakTerms = ["Term 3", "Term 4"];
  export let timeSaved = '13 hours';
  export let timeTotal = '17 hours';

  let showTitle = false;
  let showConcepts = false;
  let showTimeInfo = false;
  let showButtons = false;

  // Trigger animations sequentially on mount
  $: {
    setTimeout(() => (showTitle = true), 100); // Title appears at 100ms
    setTimeout(() => (showConcepts = true), 1100); // Concepts/Terms at 700ms
    setTimeout(() => (showTimeInfo = true), 2100); // Time info at 1300ms
    setTimeout(() => (showButtons = true), 3100); // Buttons at 1900ms
  }

  async function handlePurchase() {
    const product_name = "AWS Certified Solutions Architect";
    const productId = "prod_QxWysKGQWOT3ft";
    const priceId = "price_1Q5bu4FKyW9aNIed3s7e8GYF";

    // Call the function from the stripe.js file
    await createCheckoutSession(productId, priceId, product_name);
  }
</script>

<div class="container">
  <!-- Title -->
  <div class="title-section">
    {#if showTitle}
      <h1 in:fade={{ duration: 1000 }} class="title">
        You got <span class="highlight">{correct_of_twenty}</span> questions correct
      </h1>
    {/if}
  </div>

  <!-- Familiarity and Unfamiliarity Section -->
  <div class="concepts-section">
    {#if showConcepts}
      <div in:fade={{ duration: 1000 }} class="concepts-container">
        <!-- Familiarity Section -->
        <div class="concept-group">
          <p class="concept-header">
            Showed <span class="highlight-familiarity">familiarity</span> with:
          </p>
          <div class="concept-items">
            <!-- Strong Concepts -->
            <div class="concept-card">
              <h3 class="concept-title">Concepts</h3>
              <ul class="concept-list">
                {#each strongConcepts as concept}
                  <li>{concept}</li>
                {/each}
              </ul>
            </div>

            <!-- Strong Terms -->
            <div class="concept-card">
              <h3 class="concept-title">Terms</h3>
              <ul class="concept-list">
                {#each strongTerms as term}
                  <li>{term}</li>
                {/each}
              </ul>
            </div>
          </div>
        </div>

        <!-- Unfamiliarity Section -->
        <div class="concept-group">
          <p class="concept-header">
            Showed <span class="highlight-unfamiliarity">unfamiliarity</span> with:
          </p>
          <div class="concept-items">
            <!-- Weak Concepts -->
            <div class="concept-card">
              <h3 class="concept-title">Concepts</h3>
              <ul class="concept-list">
                {#each weakConcepts as concept}
                  <li>{concept}</li>
                {/each}
              </ul>
            </div>

            <!-- Weak Terms -->
            <div class="concept-card">
              <h3 class="concept-title">Terms</h3>
              <ul class="concept-list">
                {#each weakTerms as term}
                  <li>{term}</li>
                {/each}
              </ul>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <!-- Time Information -->
  <div class="time-info-section">
    {#if showTimeInfo}
      <div in:fade={{ duration: 1000 }} class="time-info">
        <p>
          Predicted time saved: <span class="time-highlight">{timeSaved}</span>
        </p>
        <p>
          Total Time until Certification: <span class="time-highlight">{timeTotal}</span>
        </p>
      </div>
    {/if}
  </div>

  <!-- Action Buttons -->
  <div class="button-section">
    {#if showButtons}
      <div in:fade={{ duration: 1000 }} class="button-container">
        <button class="button outline">Learn more</button>
        <button class="button primary" on:click={handlePurchase}>Full version</button>
      </div>
    {/if}
  </div>
</div>

<style>
  .container {
    background: var(--surface-100-800-token);
    width: 100%;
    height: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1.5rem;
    gap: 0.25rem;
  }

  .title-section {
    height: 100px;
    display: flex;
    align-items: center;
  }

  .title {
    font-weight: bold;
    font-size: 1.875rem; /* text-3xl */
    line-height: 2.25rem;
    text-align: center;
  }

  .highlight {
    color: var(--primary-500);
    font-weight: bold;
  }

  .concepts-section {
    height: 300px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .concepts-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 3rem; /* gap-12 */
    width: 100%;
    max-width: 96rem; /* max-w-6xl */
  }

  .concept-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem; /* space-y-6 */
  }

  .concept-header {
    font-size: 1.75rem; /* text-lg */
    line-height: 2.25rem;
    text-align: center;
    font-weight: 500;
  }

  .highlight-familiarity {
    color: var(--primary-400);
    font-weight: bold;
  }

  .highlight-unfamiliarity {
    color: var(--tertiary-300);
    font-weight: bold;
  }

  .concept-items {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem; /* gap-6 */
    width: 100%;
  }

  .concept-card {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    text-align: center;
    min-width: 15.625rem; /* min-w-[250px] */
    gap: 1rem; /* space-y-4 */
  }

  .concept-title {
    font-weight: 600;
    font-size: 1.5rem; /* text-xl */
  }

  .time-info-section {
    height: 200px;
    display: flex;
    align-items: center;
  }

  .time-info {
    text-align: center;
    gap: 2rem; /* space-y-8 */
  }

  .time-info p {
    font-size: 1.25rem; /* text-xl */
    font-weight: bold;
  }

  .time-highlight {
    color: var(--warning-400);
  }

  .button-section {
    height: 100px;
    display: flex;
    align-items: center;
  }

  .button-container {
    display: flex;
    justify-content: center;
    gap: 1rem; /* gap-4 */
  }

  .button {
    width: 14.5625rem; /* w-[233px] */
  }

  .button.outline {
    background: transparent;
    border: 2px solid var(--blue);
    color: var(--blue);
  }

  .button.primary {
    background: var(--blue);
    color: white;
  }

  .concept-list {
    display: flex;
    flex-wrap: wrap; /* Allows wrapping horizontally */
    gap: 1rem; /* Adds spacing between items */
    max-height: 200px; /* Set the maximum height */
    overflow-y: auto; /* Allows vertical scrolling if needed */
    justify-content: center; /* Center items horizontally */
    padding: 0;
    margin: 0;
    list-style: none; /* Removes default list styling */
  }

  .concept-list li {
    white-space: nowrap; /* Prevents breaking words */
    padding: 0.25rem 0.5rem;
    background-color: var(--surface-100);
    border-radius: 0.25rem;
    font-size: 1rem;
  }
</style>
