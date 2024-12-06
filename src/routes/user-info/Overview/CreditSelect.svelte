<script lang="js">
	import MastercardIcon from "../../../assets/icons/mastercard.svg";
	import VisaIcon from "../../../assets/icons/visa.svg";
	import ArrowDownIcon from "../../../assets/icons/arrow-down-white.svg";
	import { slide } from "svelte/transition";

	export let isChangeCardOpen = false;

	let cards = [
		{ id: 1, lastFour: "1234", expiry: "12/2026", icon: MastercardIcon },
		{ id: 2, lastFour: "9876", expiry: "12/2026", icon: VisaIcon },
	];

	let selectedCard = cards[0]; // Set the default selected card

	const toggleChangeCard = () => (isChangeCardOpen = !isChangeCardOpen);

	const selectCard = (card) => {
		selectedCard = card;
		isChangeCardOpen = false; // Close the change card dropdown after selection
	};
</script>

<div class="flex flex-col gap-2">
	<div
		class="p-4 flex flex-col gap-4 bg-secondary-500/10 border border-secondary-500/25 rounded-2xl"
	>
		<div class="flex gap-6">
			<figure>
				<img src={selectedCard.icon} alt="mastercard" />
			</figure>

			<div class="flex flex-col">
				<p class="text-xs font-bold">••••{selectedCard.lastFour}</p>
				<p class="text-xs">expires {selectedCard.expiry}</p>
			</div>
		</div>
		<p class="text-xs font-bold text-secondary-500">Selected</p>
	</div>

	<div class="flex flex-col gap-4">
		<button
			type="button"
			class="text-interface-50 font-bold text-xs flex items-center gap-1 w-fit"
			on:click={toggleChangeCard}
		>
			Change Card
			<img src={ArrowDownIcon} alt="close" width="7" height="7" />
		</button>

		{#if isChangeCardOpen}
			<div
				class="flex flex-col gap-4 origin-top"
				transition:slide={{ duration: 300 }}
			>
				{#each cards as card (card.id)}
					{#if selectedCard.id !== card.id}
						<div
							class="p-4 flex flex-col gap-4 border border-[rgba(86,192,240,0.25)] rounded-2xl"
						>
							<div class="flex gap-6">
								<figure>
									<img src={card.icon} alt="mastercard" />
								</figure>

								<div class="flex flex-col">
									<p class="text-xs font-bold">••••{card.lastFour}</p>
									<p class="text-xs">expires {card.expiry}</p>
								</div>
							</div>
							<button
								class="text-interface-400 font-bold text-xs w-fit"
								type="button"
								on:click={() => selectCard(card)}
							>
								Select
							</button>
						</div>
					{/if}
				{/each}
			</div>
		{/if}
	</div>
</div>
