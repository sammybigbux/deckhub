<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fade } from "svelte/transition";
  import Button from "../Button.svelte";
  import { totalCompleted, totalIncorrect, total_questions, solvedTerms, totalTerms } from "../../stores/random_store";

  export let activeDifficulty: "EASY" | "NORMAL" | "HARD" = "EASY";
  export let isFreePlan: boolean = false;
  export let remainingFreeQuestions: number = 3;
  export let termsIncorrect = 0;
  export let module = "apply";
  export let specificity = "";

  // Reactive store bindings
  $: totalCompletedValue = $totalCompleted;
  $: totalIncorrectValue = $totalIncorrect;
  $: solvedTermsValue = $solvedTerms;

  // Apply module calculations
  const initialTime = 30 * 3600; // 30 hours in seconds
  const decrementPerCorrectAnswer = initialTime / 359;

  // Reactive calculations for filtered time
  $: filteredTimeInSeconds = 30 * $total_questions;
  $: filteredTimeInSecondsSpecificity = 30 * $totalTerms;

  // Reactive total time calculations
  $: totalTime = Math.max(
    0,
    initialTime - (totalCompletedValue - totalIncorrectValue) * decrementPerCorrectAnswer
  );

  // Reactive time left for filtered module
  $: timeLeftFiltered = filteredTimeInSeconds - totalCompletedValue * 30;
  $: timeLeftFilteredSpecificity = filteredTimeInSecondsSpecificity - solvedTermsValue * 30;

  // Time display variables
  $: timeDisplayTraditional = formatTime(initialTime);
  $: timeDisplayDeckhub = formatTime(totalTime);
  $: timeSaved = initialTime - totalTime;
  $: timeDisplaySaved = formatTime(timeSaved);
  $: timeDisplayFilteredModule = formatTime(timeLeftFiltered);
  $: timeDisplayFilteredSpecificity = formatTime(timeLeftFilteredSpecificity);
  
  // Previous difficulty tracking
  $: prevDifficulty = activeDifficulty;
  $: showDifficulties = false;

  function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600); // Hours stay as-is, rounded down.
    const minutes = Math.round((seconds % 3600) / 60); // Round minutes to the nearest whole number.

    // Handle edge case where rounding minutes results in 60.
    if (minutes === 60) {
      return `${hours + 1}:00`; // Add 1 to hours and reset minutes to 00.
    }

    return `${hours}:${minutes.toString().padStart(2, "0")}`;
  }
</script>


<style>
  .container {
    position: fixed;
    top: 100px;
    right: 12px;
    width: 210px; /* Slightly increased width */
    padding: 16px;
    background-color: #28344c;
    border-radius: 8px;
    color: #ffffff;
    font-family: sans-serif;
  }

  .title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
    text-align: center;
    line-height: 3.0; /* Increased line spacing */
  }

  .time-row {
    display: flex;
    align-items: center;
    padding: 8px 0;
  }

  .label {
    display: flex;
    align-items: center;
    font-size: 16px; /* 16px font size */
    font-weight: bold; /* Bold font weight */
    font-family: 'Inter', sans-serif; /* Ensure 'Inter' is applied */
    flex-grow: 1; /* Ensures labels align to the left */
    gap: 0.5rem; /* Consistent gap for icon and text */
  }

  .time-value {
    font-size: 2rem;
    font-weight: bold;
  }

  .separator {
    border-top: 1px solid #4a5568;
    margin: 8px 0;
  }

  .traditional {
    color: #60a5fa;
  }

  .deckhub {
    color: #7250d4;
  }

  .saved {
    color: #48bb78;
  }
</style>

<div class="container">
  {#if module === "Diagnostic"}
    <!-- Title -->
    <div class="title ">Estimated study time of:</div>

    <!-- Traditional Methods Time -->
    <div class="time-row traditional">
      <span class="label">
        Covering Everything
      </span>
      <span class="time-value">{timeDisplayTraditional}</span>
    </div>

    <div class="separator"></div>

    <!-- Deckhub Time -->
    <div class="time-row deckhub">
      <span class="label">
        Deckhub Targeted Study
      </span>
      <span class="time-value">{timeDisplayDeckhub}</span>
    </div>

    <div class="separator"></div>

    <!-- Time Saved -->
    <div class="time-row saved">
      <span class="label">Time Saved:</span>
      <span class="time-value">{timeDisplaySaved}</span>
    </div>
  {:else}
  <div class="title ">Estimated time remaining:</div>

  <!-- Traditional Methods Time -->
  <div class="time-row traditional">
    <span class="label">
      {specificity[0].toUpperCase() + specificity.slice(1)}
    </span>
    <span class="time-value">{timeDisplayFilteredSpecificity}</span>
  </div>

  <div class="separator"></div>

  <!-- Deckhub Time -->
  <div class="time-row deckhub">
    <span class="label">
      Overall
    </span>
    <span class="time-value">{timeDisplayFilteredModule}</span>
  </div>

  <div class="separator"></div>
  
  {/if}
</div>
