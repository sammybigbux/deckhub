<script>
  import { onMount } from 'svelte';
  import { Avatar, ProgressBar } from '@skeletonlabs/skeleton';

  // Define locked variables
  let understand_locked = false;
  let apply_locked = false;

  // Progress data for each section
  let learnProgress = { solvedTerms: 0, totalTerms: 0 };
  let understandProgress = { solvedTerms: 0, totalTerms: 0 };
  let applyProgress = { solvedTerms: 0, totalTerms: 0 };

  // Function to retrieve terms data from different endpoints
  async function retrieveTermsData(endpoint, progress) {
      const response = await fetch(endpoint, { method: 'GET', headers: { 'Content-Type': 'application/json' } });
      const data = await response.json();
      progress.totalTerms = data.totalTerms;
      progress.solvedTerms = data.solvedTerms;

      // Check progress to unlock next section
      if (progress === learnProgress && progress.solvedTerms === progress.totalTerms) {
          understand_locked = true; // Unlock the Understand section
      }
      if (progress === understandProgress && progress.solvedTerms === progress.totalTerms) {
          apply_locked = true; //   Unlock the Apply section
      }
  }

  // On mount, fetch progress data for each section
//   onMount(async () => {
//       await retrieveTermsData('http://localhost:5000/get_terms_data', learnProgress);
//       await retrieveTermsData('http://localhost:5001/get_terms_data', understandProgress);
//       await retrieveTermsData('http://localhost:5003/get_terms_data', applyProgress);
//   });
</script>

<style>
    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        gap: 2rem; /* Space between the cards and the button */
    }
    .card-container {
        display: flex;
        justify-content: center;
        gap: 2rem; /* Space between the cards */
    }
    .card {
        position: relative; /* For positioning the lock icon */
        width: 250px;
        height: 250px;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
    }
    .card-header {
        font-size: 2rem; /* Bigger title */
        text-align: center;
        margin: 1rem 0;
    }
    .card-content {
        flex-grow: 1;
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .button-container {
        display: flex;
        width: 100%;
        height: 50%;
    }
    .button-container a {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        text-decoration: none;
        transition: background-color 0.3s ease;
        font-size: 1.2rem; /* Better styled text */
        font-weight: bold;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }

    /* Learn Module Buttons */
    .learn-standard {
        background-color: #287B99; /* Even darker Teal for Easy */
        border-radius: 0; /* Keeps the shape of the card */
    }
    .learn-turbo {
        background-color: #004C4C; /* Even darker Intense Teal for Hard */
        border-radius: 0; /* Keeps the shape of the card */
    }
    .learn-standard:hover {
        background-color: #1F6278;
    }
    .learn-turbo:hover {
        background-color: #003636;
    }

    /* Understand Module Buttons */
    .understand-study {
        background-color: #8366B3; /* Even darker Lavender for Easy */
        border-radius: 0; /* Keeps the shape of the card */
    }
    .understand-evaluate {
        background-color: #520052; /* Even darker Deep Violet for Hard */
        border-radius: 0; /* Keeps the shape of the card */
    }
    .understand-study:hover {
        background-color: #6B5190;
    }
    .understand-evaluate:hover {
        background-color: #3D003D;
    }

    /* Apply Module Buttons */
    .apply-study {
        background-color: #CC6F5E; /* Even darker Coral for Easy */
        border-radius: 0; /* Keeps the shape of the card */
    }
    .apply-evaluate {
        background-color: #B03D2C; /* Even darker Rich Coral for Hard */
        border-radius: 0; /* Keeps the shape of the card */
    }
    .apply-study:hover {
        background-color: #A6564A;
    }
    .apply-evaluate:hover {
        background-color: #993429;
    }


  
    .locked {
        position: relative;
    }
    .locked .card-content {
        margin-bottom: 3rem; /* Space for lock icon */
    }
    .locked::after {
        content: '🔒';
        font-size: 3rem;
        color: rgba(0, 0, 0, 0.5);
        position: absolute;
        bottom: 10%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .progress-bars-container {
        display: flex;
        justify-content: center;
        gap: 2rem; /* Space between the progress bars */
        margin-top: 0.25rem; /* Further reduced space between the cards and progress bars */
    }
    .progress-bar {
        width: 250px; /* Same width as the card */
    }
  </style>

<div class="center-container">
    <div class="card-container">
        <!-- Learn Module Card -->
        <div class="card">
            <h1 class="card-header">Learn</h1>
            <p class="card-content">Gain new knowledge and familiarity with key terms.</p>
            <div class="button-container">
                <a href="/learn-multiple" class="btn learn-standard">Standard</a>
                <a href="/learn-open" class="btn learn-turbo">Smart</a>
            </div>
        </div>
  
        <!-- Understand Module Card -->
        <div class="card {understand_locked ? 'locked' : ''}">
            <h1 class="card-header">Understand</h1>
            <p class="card-content">Deepen your comprehension and grasp complex concepts.</p>
            {#if !understand_locked}
            <div class="button-container">
                <a href="/understand-multiple" class="btn understand-study">Standard</a>
                <a href="/understand-open" class="btn understand-evaluate">Smart</a>
            </div>
            {/if}
        </div>
  
        <!-- Apply Module Card -->
        <div class="card {apply_locked ? 'locked' : ''}">
            <h1 class="card-header">Apply</h1>
            <p class="card-content">Put your knowledge to use and solve real-world problems.</p>
            {#if !apply_locked}
            <div class="button-container">
                <a href="/apply-multiple" class="btn apply-study">Standard</a>
                <a href="/apply-open" class="btn apply-evaluate">Smart</a>
            </div>
            {/if}
        </div>
    </div>
  <!-- <div class="progress-bars-container">
      <div class="progress-bar">
          <ProgressBar
              value={learnProgress.solvedTerms}
              max={learnProgress.totalTerms}
              height="h-6"
              rounded="rounded-md"
              transition="transition-[width]"
              meter={learnProgress.solvedTerms === learnProgress.totalTerms ? 'bg-green-500' : 'bg-yellow-500'}
              track="bg-surface-200"
              labelledby="progress-label"
          />
      </div>
      <div class="progress-bar">
          {#if !understand_locked}
              <ProgressBar
                  value={understandProgress.solvedTerms}
                  max={understandProgress.totalTerms}
                  height="h-6"
                  rounded="rounded-md"
                  transition="transition-[width]"
                  meter={understandProgress.solvedTerms === understandProgress.totalTerms ? 'bg-green-500' : 'bg-yellow-500'}
                  track="bg-surface-200"
                  labelledby="progress-label"
              />
          {/if}
      </div>
      <div class="progress-bar">
          {#if !apply_locked}
              <ProgressBar
                  value={applyProgress.solvedTerms}
                  max={applyProgress.totalTerms}
                  height="h-6"
                  rounded="rounded-md"
                  transition="transition-[width]"
                  meter={applyProgress.solvedTerms === applyProgress.totalTerms ? 'bg-green-500' : 'bg-yellow-500'}
                  track="bg-surface-200"
                  labelledby="progress-label"
              />
          {/if}
      </div>
  </div> -->
</div>
