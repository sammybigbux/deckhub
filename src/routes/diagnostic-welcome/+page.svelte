<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from '$app/navigation';
    import Button from "../../components/Button.svelte";
    const base_url = import.meta.env.VITE_BASE_URL;
  
    let animationClass = "";
  
    // Dummy title
    let title = "Welcome to Your Learning Journey";
  
    // Dummy function for openOverlay
    let openOverlay = () => {
      console.log("Learn More button clicked");
    };
  
    // Dummy variable to determine button state
    let isOwned = false;
  
    // Dummy function for handlePurchase
    function handleClick() {
      const slug = encodeURIComponent("AWS Certified Solutions Architect"); // Ensure the slug is URL-safe
      goto(`/new/learn/${slug}`); // Navigate to the dynamic route
    }
  
    // Add fade-in class on mount
    onMount(() => {
      setTimeout(() => (animationClass = "fade-in"), 0);
    });
  </script>
  
  <style>
    /* Keyframe animations for fade-in */
    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  
    /* General fade-in class */
    .fade-in {
      opacity: 0;
      animation: fadeIn 1s ease-in-out forwards;
    }
  
    /* Header, middle, and button-specific delays */
    .fade-in-header {
      animation-delay: 0s;
    }
  
    .fade-in-middle-1 {
      animation-delay: 1s;
    }
  
    .fade-in-middle-2 {
      animation-delay: 2s;
    }
  
    .fade-in-middle-3 {
      animation-delay: 3s;
    }
  
    .fade-in-button {
      animation-delay: 4s;
    }
  
    .custom-button-container {
      display: flex;
      justify-content: center; /* Center the button horizontally */
      width: 100%; /* Ensure full width for centering */
    }
  
    .content-container {
      max-width: 100%; /* Allow the container to extend fully */
      width: 100%;
      text-align: center;
      animation: fadeIn 1s ease-in-out forwards; /* Fade in the entire container */
    }
  
    .center-page {
      display: flex;
      justify-content: center;
      align-items: flex-start;
      height: 100vh;
      padding-top: 10vh; /* Bring content closer to the top */
    }
  
    h1 {
      font-size: 4rem; /* Larger title */
      line-height: 1.3;
      margin-bottom: 3rem; /* Space below the header */
    }
  
    .text-block {
      margin-bottom: 4rem; /* Space below the text block */
    }
  
    .text-block p {
      font-size: 1.6rem; /* Larger text */
      line-height: 2.2rem; /* Comfortable line height */
      margin: 1rem 0; /* Space between paragraphs */
    }
  </style>
  
  <div class="center-page">
    <div class="content-container">
      <!-- Header with fade-in -->
      <h1 class={`${animationClass} fade-in-header`}>
        {title}
      </h1>
  
      <!-- Text block with points fading in separately -->
      <div class="text-block">
        <p class={`${animationClass} fade-in-middle-1`}>Help us pinpoint your weak spots with a quick <span class="text-primary-500 font-bold">diagnostic test</span></p>
        <p class={`${animationClass} fade-in-middle-2`}>Discover your biggest strengths and areas to focus on with a <span class="text-primary-500 font-bold">personalized report</span></p>
        <p class={`${animationClass} fade-in-middle-3`}>Find out how long it would take to <span class="text-primary-500 font-bold">prepare for the certification</span></p>
      </div>
  
      <!-- Button with fade-in after 6 seconds -->
      <div class={`custom-button-container ${animationClass} fade-in-button`}>
        <Button
          variant="primary-blue"
          className="!min-w-0 !w-[350px] !h-[44px] lg:text-nowrap disabled:opacity-60 disabled:cursor-not-allowed"
          on:click={handleClick}
        >
          Get Started
        </Button>
      </div>
    </div>
  </div>
  