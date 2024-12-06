<script>
	import { onMount, onDestroy } from "svelte";
	import { get } from "svelte/store";
	import { isLoggedIn, auth } from "$lib/firebase";
	import Button from "../../../components/Button.svelte";
	import ArrowDown from "../../../assets/icons/arrow-down.svg";
	import RequestCard from "./RequestCard.svelte";

	const base_url = import.meta.env.VITE_BASE_URL;

	let requestText = "";
	let requests = [];
	let user = null;
	let unsubscribe;
	let isSubscribed = true;
	let toggleFilter = true;

	function handleToggleClick() {
		toggleFilter = !toggleFilter;

		if (toggleFilter) {
			// Sort by upvotes
			requests = requests.sort((a, b) => b.upvotes - a.upvotes);  // descending order
		} else {
			// Sort by timestamp
			requests = requests.sort((a, b) => b.timestamp - a.timestamp);  // descending order
		}
	}

	async function handleSubmit() {
		if (!get(isLoggedIn)) {
			alert("You need to be logged in to submit a request.");
			return;
		}

		try {
			const response = await fetch(
				`${base_url}/submit_request`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						text: requestText,
						user_id: user.uid,
					}),
				}
			);

			const result = await response.json();
			if (response.status !== 200) {
				alert(result.error || "Failed to submit the request.");
			} else {
				fetchRequests();
				requestText = ""; // Clear the input field
			}
		} catch (error) {
			console.error("Error submitting request:", error);
			alert("Failed to submit the request. Can only submit one request per 15 minutes.");
		}
	}

	async function fetchRequests() {
		try {
			console.log("Starting fetch for requests...");
			const response = await fetch(
				`${base_url}/fetch_requests`
			);

			console.log("Received response:", response);

			// Check if the response is OK (status 200)
			if (!response.ok) {
				console.error(
					"Server responded with an error:",
					response.status,
					response.statusText
				);
				return;
			}

			console.log("Parsing JSON...");
			requests = await response.json();

			console.log("Requests received and parsed successfully:", requests);
		} catch (error) {
			console.error("Error fetching requests:", error);
		}
	}

	async function toggleUpvote(requestId) {
		try {
			await fetch(
				`${base_url}/toggle_upvote`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						request_id: requestId,
						user_id: user.uid,
					}),
				}
			);

			fetchRequests();
		} catch (error) {
			console.error("Error toggling upvote:", error);
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

	const dummyBounties = [
		{
			id: "1",
			solved: true,
			subscribers: [],
			text: "Test Bounty",
			timestamp: new Date(),
			upvotes: 0,
		},
		{
			id: "1",
			solved: true,
			subscribers: [],
			text: "Test Bounty 2",
			timestamp: new Date(),
			upvotes: 0,
			isUnderReview: true,
		},
	];
</script>

<main
	class="pt-[40px] pb-[108px] px-8 lg:px-[50px] xl:px-[348px] flex flex-col items-center justify-center"
>
	<div class="flex flex-col gap-[40px] justify-center items-center">
		<h1 class="font-bold text-4xl capitalize">Feedback</h1>

		<div
			class="p-6 rounded-[32px] bg-[rgba(59,130,246,0.1)] mb-[32px] w-[392px]"
		>
			<form on:submit|preventDefault={handleSubmit} class="flex flex-col gap-6">
				<input
					type="text"
					id="requestText"
					bind:value={requestText}
					placeholder="Enter request here"
					required
					class="px-[16px] py-[12px] bg-[rgba(86,192,240,0.25)] border-none rounded-xl text-xs leading-[20px] text-interface-50 placeholder-interface-50 placeholder:text-xs placeholder:leading-[20px]"
				/>
				<Button type="submit" variant="primary-blue" className="w-full"
					>Submit Request</Button
				>
			</form>
		</div>
	</div>

	<div class="flex flex-col gap-8 w-full">
		<div class="flex items-center justify-between gap-5">
			<h3 class="font-bold text-2xl capitalize">Requests</h3>
			<button
				class="flex items-center gap-2 text-[16px] font-bold text-primary-500 capitalize"
				on:click={handleToggleClick}
			>
				{#if toggleFilter}
					Upvotes
				{:else}
					Date
				{/if}
				<figure>
					<img src="{ArrowDown}" alt="arrow" class="w-2" width="8" height="8" />
				</figure>
			</button>
		</div>
		<ul class="grid gap-6 place-items-center lg:grid-cols-2 2.5xl:grid-cols-3">
			{#each [...dummyBounties, ...requests] as request}
				<RequestCard {request} {user} {toggleUpvote} />
			{/each}
		</ul>
	</div>
</main>
