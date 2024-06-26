<script>
    import { auth, isLoggedIn, db } from '$lib/firebase';
    import { collection, addDoc, updateDoc, getDocs, doc, query, where, getDocsFromServer, Timestamp } from 'firebase/firestore';
    import { onMount, onDestroy } from 'svelte';
    import { get } from 'svelte/store';
  
    let requestText = '';
    let requests = [];
    let user = null;
    let unsubscribe;
  
    async function handleSubmit() {
      if (!get(isLoggedIn)) {
        alert('You need to be logged in to submit a request.');
        return;
      }
  
      const fifteenMinutesAgo = new Date();
      fifteenMinutesAgo.setMinutes(fifteenMinutesAgo.getMinutes() - 15);
  
      // Query to check if the user has posted anything in the last 15 minutes
      const q = query(
        collection(db, 'requests'),
        where('subscribers', 'array-contains', user.uid),
        where('timestamp', '>=', Timestamp.fromDate(fifteenMinutesAgo))
      );
  
      const querySnapshot = await getDocsFromServer(q);
      if (!querySnapshot.empty) {
        alert('You can only submit one request every 15 minutes.');
        return;
      }
  
      try {
        const request = {
          upvotes: 1,
          solved: false,
          text: requestText,
          subscribers: [user.uid],
          timestamp: Timestamp.now()
        };
  
        await addDoc(collection(db, 'requests'), request);
        fetchRequests();
        requestText = ''; // Clear the input field
      } catch (error) {
        console.error('Error adding document: ', error);
        alert('Failed to submit the request.');
      }
    }
  
    async function fetchRequests() {
      const querySnapshot = await getDocs(collection(db, 'requests'));
      requests = querySnapshot.docs
        .map(doc => ({ id: doc.id, ...doc.data() }))
        .sort((a, b) => b.upvotes - a.upvotes);
    }
  
    async function toggleUpvote(requestId) {
      const requestDoc = doc(db, 'requests', requestId);
      const request = requests.find(r => r.id === requestId);
  
      if (request.subscribers.includes(user.uid)) {
        // Remove upvote
        request.upvotes--;
        request.subscribers = request.subscribers.filter(uid => uid !== user.uid);
      } else {
        // Add upvote
        request.upvotes++;
        request.subscribers.push(user.uid);
      }
  
      await updateDoc(requestDoc, {
        upvotes: request.upvotes,
        subscribers: request.subscribers
      });
  
      fetchRequests();
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
      background-color: #007bff; /* Same color as the submit request button */
      border-radius: 4px;
      padding: 1rem;
      margin-bottom: 1rem;
      width: 100%;
      color: black; /* Text color black */
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
      font-size: 2.5rem; /* Larger arrow */
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
  