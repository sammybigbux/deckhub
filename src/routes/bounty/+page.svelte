<script>
  import { onMount, onDestroy } from 'svelte';
  import { get } from 'svelte/store';
  import { isLoggedIn, auth} from '$lib/firebase';
  


  let requestText = '';
  let requests = [];
  let user = null;
  let unsubscribe;
  let isSubscribed = true;

  async function handleSubmit() {
      if (!get(isLoggedIn)) {
          alert('You need to be logged in to submit a request.');
          return;
      }

      try {
          const response = await fetch('http://127.0.0.1:5000/submit_request', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                  text: requestText,
                  user_id: user.uid,
              }),
          });

          const result = await response.json();
          if (response.status !== 200) {
              alert(result.error || 'Failed to submit the request.');
          } else {
              fetchRequests();
              requestText = ''; // Clear the input field
          }
      } catch (error) {
          console.error('Error submitting request:', error);
          alert('Failed to submit the request.');
      }
  }

  async function fetchRequests() {
    try {
        console.log("Starting fetch for requests...");
        const response = await fetch('http://127.0.0.1:5000/fetch_requests');
        
        console.log("Received response:", response);

        // Check if the response is OK (status 200)
        if (!response.ok) {
            console.error('Server responded with an error:', response.status, response.statusText);
            return;
        }

        console.log("Parsing JSON...");
        requests = await response.json();

        console.log("Requests received and parsed successfully:", requests);
    } catch (error) {
        console.error('Error fetching requests:', error);
    }
  }

  async function toggleUpvote(requestId) {
      try {
          await fetch('http://127.0.0.1:5000/toggle_upvote', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                  request_id: requestId,
                  user_id: user.uid,
              }),
          });

          fetchRequests();
      } catch (error) {
          console.error('Error toggling upvote:', error);
      }
  }

  onMount(() => {
      unsubscribe = auth.onAuthStateChanged((authUser) => {
          user = authUser;
          if (user) {
              fetchRequests();
          }
      });
  });

  onDestroy(() => {
      if (unsubscribe) {
          unsubscribe();
      }
  });
</script>

<style>
  .center-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 2rem;
  }
  .card {
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      padding: 1rem;
      max-width: 600px;
      width: 100%;
      margin-bottom: 2rem;
  }
  .request-card {
      display: flex;
      align-items: center;
      background-color: #007bff;
      border-radius: 4px;
      padding: 1rem;
      margin-bottom: 1rem;
      width: 100%;
      color: black;
  }
  .request-text {
      font-weight: bold;
      flex-grow: 1;
      margin: 0 1rem;
      color: white;
  }
  .input-container {
      display: flex;
      flex-direction: column;
      width: 100%;
  }
  .input-container input {
      width: 100%;
      padding: 1rem;
      margin-bottom: 1rem;
      border: 1px solid #0c0c0c;
      color: black;
      border-radius: 4px;
      font-size: 1rem;
  }
  .input-container button {
      width: 100%;
      padding: 1rem;
      font-size: 1rem;
  }
  .btn {
      cursor: pointer;
  }
  .btn-upvote {
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
  }
  .upvote-arrow {
      font-size: 2.5rem;
      color: gray;
  }
  .upvoted {
      color: orange;
  }
  .status {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      color: white;
      font-weight: bold;
  }
  .solved {
      background-color: green;
  }
  .unsolved {
      background-color: red;
  }
</style>

<main class="center-container">
  <div class="card p-4">
      <div class="input-container">
          <form on:submit|preventDefault={handleSubmit}>
              <input
                  type="text"
                  id="requestText"
                  bind:value={requestText}
                  placeholder="Enter the name of the exam"
                  required
              />
              <button type="submit" class="btn bg-primary-500 card-hover">Submit Request</button>
          </form>
      </div>
  </div>
  {#each requests as request}
      <div class="request-card">
          <button class="btn btn-upvote" on:click={() => toggleUpvote(request.id)}>
              <span class="upvote-arrow {request.subscribers.includes(user.uid) ? 'upvoted' : ''}">⬆</span>
              <span class="request-text">{request.upvotes}</span>
          </button>
          <div class="request-text">{request.text}</div>
          {#if request.solved}
              <div class="status solved">Solved</div>
          {:else}
              <div class="status unsolved">No Solution</div>
          {/if}
      </div>
  {/each}
</main>
