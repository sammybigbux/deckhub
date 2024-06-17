<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    let exam;

    $: {
        if ($page.data) {
            exam = $page.data.exam;
        }
    }

    onMount(() => {
        console.log("Received exam:", exam);
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
    padding-top: 10vh; /* Position the card 10% from the top */
  }
  .card {
    padding: 40px; /* Increased padding */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    width: 100%;
    max-width: 800px; /* Increased max-width */
    text-align: center; /* Center all text in the card */
  }
  .card-header {
    font-size: 2.5rem;
    line-height: 1; /* Add line height to avoid overlap */
    margin-bottom: 20px; /* Add bottom margin */
  }
  .card-content {
    margin-bottom: 30px; /* Ensure spacing between content and button */
  }
  .button-container {
    display: flex;
    justify-content: center; /* Center the button */
    margin-top: 20px; /* Optional: add some space between content and buttons */
  }
  .btn {
    margin-left: 10px; /* Add space between buttons */
  }
  .bg-primary-500 {
    background-color: #007bff;
    color: white;
    padding: 10px 20px; /* Add padding to the button */
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  .bg-primary-500:hover {
    background-color: #0056b3; /* Darker blue on hover */
  }
</style>

<main class="center-container">
    <div class="card">
        {#if exam}
            <h1 class="card-header">{exam.name}</h1>
            <div class="card-content">
                <div>
                    <span>{exam.icon}</span>
                    <span>{exam.length} cards</span>
                    <p> </p>
                    <span>Last Updated: {exam.lastUpdated}</span>
                </div>
            </div>
            <div class="button-container">
                <button type="button" class="btn bg-primary-500">Download file</button>
            </div>
        {/if}
    </div>
</main>
