<script>
    import { onMount } from 'svelte';
  
    // Define locked variables
    let understand_locked = true;
    let apply_locked = true;
    let practice_locked = true;
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
    .button-study {
      background-color: orange;
      border-radius: 0; /* Override btn class */
    }
    .button-evaluate {
      background-color: darkgreen;
      border-radius: 0; /* Override btn class */
    }
    .button-study:hover {
      background-color: darkorange;
    }
    .button-evaluate:hover {
      background-color: green;
    }
    .practice-button-container {
      position: relative;
      width: calc(3 * 250px + 2 * 2rem); /* Width of three cards plus the gaps between them */
    }
    .practice-button {
      width: 100%;
      text-align: center;
      font-size: 1.5rem;
      padding: 1rem;
      margin-top: 2rem;
      position: relative; /* For positioning the lock icon */
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
    .button-locked {
      background-color: gray;
      cursor: not-allowed;
      bottom: 20%;
    }
    .lock-overlay {
      position: absolute;
      top: 62%;
      left: 50%;
      transform: translate(-50%, -50%);
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .lock-overlay::after {
      content: '🔒';
      font-size: 3rem;
      color: rgba(0, 0, 0, 0.5);
    }
  </style>
  
  <div class="center-container">
    <div class="card-container">
      <div class="card">
        <h1 class="card-header">Learn</h1>
        <p class="card-content">Gain new knowledge and familiarity with key terms.</p>
        <div class="button-container">
          <a href="/study-learn" class="btn button-study">Study</a>
          <a href="/evaluate" class="btn button-evaluate">Evaluate</a>
        </div>
      </div>
      <div class="card {understand_locked ? 'locked' : ''}">
        <h1 class="card-header">Understand</h1>
        <p class="card-content">Deepen your comprehension and grasp complex concepts.</p>
        {#if !understand_locked}
        <div class="button-container">
          <a href="/study" class="btn button-study">Study</a>
          <a href="/evaluate" class="btn button-evaluate">Evaluate</a>
        </div>
        {/if}
      </div>
      <div class="card {apply_locked ? 'locked' : ''}">
        <h1 class="card-header">Apply</h1>
        <p class="card-content">Put your knowledge to use and solve real-world problems.</p>
        {#if !apply_locked}
        <div class="button-container">
          <a href="/study" class="btn button-study">Study</a>
          <a href="/evaluate" class="btn button-evaluate">Evaluate</a>
        </div>
        {/if}
      </div>
    </div>
    <div class="practice-button-container">
      <a href="/practice" class="btn variant-filled-surface practice-button {practice_locked ? 'button-locked' : ''}">
        Practice exam questions
      </a>
      {#if practice_locked}
      <div class="lock-overlay"></div>
      {/if}
    </div>
  </div>
  