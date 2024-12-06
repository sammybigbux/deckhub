<script lang="js">
	import { onMount } from "svelte";
	import { writable } from "svelte/store";
	import AccountName from "./Overview/AccountName.svelte";
	import AccountBalance from "./Overview/AccountBalance.svelte";
	import PaymentMethods from "./Overview/PaymentMethods.svelte";
	import { fade } from "svelte/transition";
	import PastOrders from "./TransactionHistory/PastOrders.svelte";
	import PayAsYouGo from "./TransactionHistory/PayAsYouGo.svelte";

	// Create writable store to manage active tab state
	const tabSet = writable(0);
	// Function to update the moving border position
	function updateTab(index, event) {
		tabSet.set(index);

		const movingBorder = document.getElementById("moving-border");
		const tab = event.currentTarget;

		const { width, left } = tab.getBoundingClientRect();
		const containerLeft = tab.parentElement.getBoundingClientRect().left;

		// Update border width and position
		movingBorder.style.width = `${width}px`;
		movingBorder.style.left = `${left - containerLeft}px`;
	}

	// Initialize border to the first tab on mount
	onMount(() => {
		const firstTab = document.querySelector('[data-tab="0"]');
		if (firstTab) updateTab(0, { currentTarget: firstTab });
	});

	// Update tab based on the URL hash
	onMount(() => {
		const hash = window.location.hash;
		if (hash) {
			const tabIndex = parseInt(hash.replace("#tab", ""), 10);
			if (!isNaN(tabIndex)) {
				tabSet.set(tabIndex);
			}
		}
	});
</script>

<div class="pt-10 pb-[108px] flex flex-col items-center justify-center gap-10 max-2xl:gap-5 max-2xl:pt-2">
	<h1 class="font-bold text-4xl text-center text-interface-50">Account</h1>

	<div
		class="p-8 !pb-4 rounded-4xl w-full max-w-[1116px] min-h-[620px] max-2xl:min-h-[520px] bg-[rgba(59,130,246,0.1)]"
	>
		<!-- Tabs Header -->
		<div class="relative mb-8 max-2xl:mb-5">
			<div class="flex gap-10 pb-4 border-b border-[rgba(86,192,240,0.25)]">
				<button
					data-tab="0"
					class="text-interface-50 cursor-pointer w-[76px] transition-all duration-300 {$tabSet ===
					0
						? 'font-bold'
						: ''}"
					on:click={(e) => updateTab(0, e)}
				>
					Overview
				</button>
				<button
					data-tab="1"
					class="text-interface-50 cursor-pointer w-[153px] transition-all duration-300 {$tabSet ===
					1
						? 'font-bold'
						: ''}"
					on:click={(e) => updateTab(1, e)}
				>
					Transaction history
				</button>
				<button
					data-tab="2"
					class="text-interface-50 cursor-pointer w-[96px] transition-all duration-300 {$tabSet ===
					2
						? 'font-bold'
						: ''}"
					on:click={(e) => updateTab(2, e)}
				>
					Preferences
				</button>
			</div>

			<!-- Moving Border -->
			<div
				id="moving-border"
				class="absolute bottom-0 h-px bg-interface-50 transition-all duration-300"
				style="width: 0; left: 0;"
			></div>
		</div>

		<!-- Tab Content -->
		<div>
			{#if $tabSet === 0}
				<div class="flex gap-[69px] flex-wrap [&_>div]:flex-1" in:fade={{ duration: 700 }}>
					<AccountName />
					<AccountBalance />
					<PaymentMethods />
				</div>
			{/if}

			{#if $tabSet === 1}
				<div class="flex flex-col gap-8" in:fade={{ duration: 700 }}>
					<PastOrders />
					<PayAsYouGo />
				</div>
			{/if}

			{#if $tabSet === 2}
				<div class="" in:fade={{ duration: 700 }}>
					<h2>Funding</h2>
					<p>Here you will manage your funding options.</p>
				</div>
			{/if}
		</div>
	</div>
</div>
