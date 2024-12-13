<script>
  import { fade, slide } from 'svelte/transition';
  import { createCheckoutSession } from "$lib/stripe";
  import SectionAnimation from './SectionAnimation.svelte';
  import FamiliarityUnfamiliaritySection from './ReportHierarchy.svelte';

  // Props to receive data from the parent component
  export let correct_of_twenty = 0;
  export let incorrect_of_twenty = 0;

  const traditionalStudyTime = 30;

  $: timeTotal = Math.round(traditionalStudyTime * (incorrect_of_twenty / 10));
  $: timeSaved = traditionalStudyTime - timeTotal;
  $: moneySaved = `$${(timeSaved * 20).toFixed(2)}`;


  function get_task_from_hours() {
    const hours = Math.round(parseFloat(timeSaved)); // Round to the nearest whole number

    switch (hours) {
      case 1:
        return "clean your kitchen thoroughly, including the fridge 🧼";
      case 2:
        return "watch Remember the Titans";
      case 3:
        return "watch the Fellowship of the Ring 🧙‍♂️💍🚶🗡️🚶‍♂️";
      case 4:
        return "read the entirety of the Great Gatsby";
      case 5:
        return "read the entirety of Exhalation by Ted Chiang (which we highly recommend)";
      case 6:
        return "read the entirety of the Song of Achilles by Madeline Miller 🗡️🛡️😠";
      case 7:
        return "deep-clean your apartment, top to bottom";
      case 8:
        return "take a full day off work to relax and recharge";
      case 9:
        return "watch the entire Lord of the Rings trilogy (theatrical cut) 🧙‍♂️💍🚶🗡️🚶‍♂️";
      case 10:
        return "watch all eight Star Wars movies (the good ones at least)";
      case 11:
        return "read Catch-22 by Joseph Heller";
      case 12:
        return "watch the entire Lord of the Rings trilogy (extended editions) 🧙‍♂️💍🚶🗡️🚶‍♂️";
      case 13:
        return "read Harry Potter and the Goblet of Fire";
      case 14:
        return "read Harry Potter and the Order of the Phoenix";
      case 15:
        return "listen to the Ready Player One audiobook 🔑🕹️👦";
      case 16:
        return "listen to the entirety of the Guns, Germs, and Steal audiobook";
      case 17:
        return "listen to the Night Watch by Terry Pratchett audiobook";
      case 18:
        return "run all the way from San Francisco to San Jose and back 🌉🏃‍♂️🏙️";
      case 19:
        return "take an overnight train ride to somewhere new and interesting";
      case 20:
        return "take a full weekend off to relax and recharge";
      case 21:
        return "run all the way from San Francisco to San Jose and back 🌉🏃‍♂️🏙️";
      case 22:
        return "listen to the Secret History by Donna Tart audiobook";
      case 23:
        return "listen to the entire Three Musketeers audiobook";
      case 24:
        return "take three full workdays off to relax and recharge 💤🛌";
      default:
        return "take on a project or adventure you’ve always wanted to try!";
    }
  }



  export let strongHierarchy = {
    "Section 1": {
      "Concept 1": ["Term 1", "Term 2"],
      "Concept 2": ["Term 3", "Term 4"],
    },
    "Section 2": {
      "Concept 3": ["Term 5", "Term 6"],
      "Concept 4": ["Term 7", "Term 8"],
    },
  };

  export let weakHierarchy = {
    "Section 1": {
      "Concept 1": ["Term 1", "Term 2"],
      "Concept 2": ["Term 3", "Term 4"],
    },
    "Section 2": {
      "Concept 3": ["Term 5", "Term 6"],
      "Concept 4": ["Term 7", "Term 8"],
    }};

//   const length_of_strong = Math.min(strongConcepts.length, strongTerms.length);
// const length_of_weak = Math.min(weakConcepts.length, weakTerms.length);

// // Truncate the longer arrays to match the length of the shorter arrays
// strongConcepts = strongConcepts.slice(0, length_of_strong);
// strongTerms = strongTerms.slice(0, length_of_strong);
// weakConcepts = weakConcepts.slice(0, length_of_weak);
// weakTerms = weakTerms.slice(0, length_of_weak);

  let showTitle = false;
  let showConcepts = false;
  let showTimeInfo = false;
  let showButtons = false;

  // Trigger animations sequentially on mount
  $: {
    setTimeout(() => (showTitle = true), 100); // Title appears at 100ms
    setTimeout(() => (showConcepts = true), 1100); // Concepts/Terms at 1100ms
    setTimeout(() => (showTimeInfo = true), 2100); // Time info at 2100ms
    setTimeout(() => (showButtons = true), 3100); // Buttons at 3100ms
  }

  async function handlePurchase() {
    const product_name = "AWS Certified Solutions Architect";
    const productId = "prod_QxWysKGQWOT3ft";
    const priceId = "price_1Q5bu4FKyW9aNIed3s7e8GYF";

    // Call the function from the stripe.js file
    await createCheckoutSession(productId, priceId, product_name);
  }



  let showScreen = 1;

  function toggleScreen(up=true) {
    if (up) {
      showScreen+=1;
    } else {
      showScreen-=1;
    }
  }
</script>

<div class="bg-surface-100-800-token w-full h-full min-h-screen flex flex-col justify-between p-6">
  <!-- Slide Container -->
  <div class="relative w-full h-full overflow-hidden">
    <!-- Screen One: Title + Concepts/Terms -->
    {#if showScreen === 1}
      <div class="absolute w-full h-full flex flex-col justify-between" transition:slide="{{ duration: 500 }}">
        <!-- Title -->
        <div class="flex items-start justify-center 2xl:mt-8">
          <h1 in:fade={{ duration: 1000 }} class="font-bold text-2xl sm:text-3xl lg:text-5xl text-center">
            You got <span class="text-primary-500 font-bold">{correct_of_twenty}</span> questions correct
          </h1>
        </div>

        <FamiliarityUnfamiliaritySection
        scope="strong"
        hierarchy={strongHierarchy}
      />
        <!-- Right Arrow Button -->
        <div class="absolute right-6 bottom-6">
          <button class="rounded-full p-4 bg-primary-500 text-white" on:click={toggleScreen}>
            →
          </button>
        </div>
      </div>
    {/if}
    {#if showScreen === 2}
    <div class="absolute w-full h-full flex flex-col justify-between" transition:slide="{{ duration: 500 }}">
      <!-- Title -->
      <div class="flex items-start justify-center 2xl:mt-8">
        <h1 in:fade={{ duration: 1000 }} class="font-bold text-2xl sm:text-3xl lg:text-5xl text-center">
          You got <span class="text-tertiary-500 font-bold">{incorrect_of_twenty}</span> questions incorrect
        </h1>
      </div>

      <FamiliarityUnfamiliaritySection
        scope="weak"
        hierarchy={weakHierarchy}
      />

      <!-- Right Arrow Button -->
      <div class="absolute right-6 bottom-6">
        <button class="rounded-full p-4 bg-tertiary-500 text-white" on:click={toggleScreen}>
          →
        </button>
      </div>
    </div>
    {/if}
    <!-- Screen Two: Predicted Time Saved + Buttons -->
    {#if showScreen === 3}
    <div class="absolute w-full h-full flex flex-col justify-between" transition:slide="{{ duration: 500 }}">
      <!-- Predicted Time Information -->
      <div class="w-full flex flex-col items-center justify-center flex-grow margin px-5">
        <p class="font-bold text-2xl sm:text-3xl lg:text-5xl text-center">
          Based on your answers, we estimate studying will take <span class="text-warning-400">30 hours</span> with traditional methods, but just <span class="text-warning-400">{timeTotal} hours</span> with Deckhub.
        </p>
        <p class="text-base sm:text-lg lg:text-xl text-center mt-2 text-muted 2xl:pt-10 pt-4">
          (If you make $20.00 per hour then that's <span class="text-warning-400">{moneySaved} </span> saved 💸)
        </p>
        <p class="text-base sm:text-lg lg:text-xl text-center mt-2 text-muted 2xl:pt-10 pt-4">
          (That’s <span class="text-warning-400">{timeSaved} hours saved</span>, enough to {get_task_from_hours()}!)
        </p>
      </div>

      <p class="font-bold text-2xl sm:text-3xl lg:text-5xl text-center fade-in">
        Continue?
      </p>
    
      <!-- Animation Section -->
      <div class="w-full flex section-animation-wrapper mt-4">
        <SectionAnimation />
      </div>
      
      <!-- Buttons -->
      <div class="w-full flex justify-center gap-4 mb-8">
        <button on:click={() => (window.location.href = '/about')} class="button outline-blue w-[233px]">Learn more</button>
        <button 
          class="button primary-blue w-[233px]" 
          on:click={handlePurchase}
        >
          Full version
        </button>
      </div>
    </div>
    {/if}
  </div>
</div>

<style>
.section-animation-wrapper {
  position: relative; /* Keeps its relative positioning within the layout */
  display: flex; /* Ensures child elements align properly */
  justify-content: flex-start; /* Elements render left-to-right */
  align-items: center; /* Vertically aligns the animation */
  margin: 0 auto; /* Centers the wrapper horizontally */
  width: 725px; /* Doubled width to prevent overflow */
  height: 150px; /* Slightly taller to account for bounce effect */
}

@keyframes fadeIn {
  from {
    opacity: 0; /* Start completely transparent */
  }
  to {
    opacity: 1; /* Fully visible */
  }
}

/* Modifier for delay (e.g., delay by 2 seconds) */
.fade-in {
  opacity: 0; /* Ensure the element starts invisible */
  animation: fadeIn 1s ease-in forwards; /* Define the animation */
  animation-delay: 8s; /* Delay the start of the animation by 10 seconds */
}


</style>

