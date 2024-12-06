<script lang="js">
	import Button from "../../../components/Button.svelte";
	import MastercardIcon from "../../../assets/icons/mastercard.svg";
	import VisaIcon from "../../../assets/icons/visa.svg";
	import { fade, slide } from "svelte/transition";

	// Array to hold the payment methods
	let paymentMethods = [
		{
			id: 1,
			cardType: "mastercard",
			icon: MastercardIcon,
			last4Digits: "1234",
			expiry: "12/2026",
			isDefault: true,
		},
		{
			id: 2,
			cardType: "visa",
			icon: VisaIcon,
			last4Digits: "9876",
			expiry: "12/2026",
			isDefault: false,
		},
	];

	// Function to set a card as default and sort the list
	function setDefault(id) {
		// Update the default status
		paymentMethods = paymentMethods.map((card) => ({
			...card,
			isDefault: card.id === id,
		}));

		// Sort so that the default card is first
		paymentMethods = paymentMethods.sort((a, b) => b.isDefault - a.isDefault);
	}

	function deletePaymentMethod(id) {
		// Delete the card
		paymentMethods = paymentMethods.filter((card) => card.id !== id);

		// If the default card was deleted, make the first card the default
		if (
			!paymentMethods.some((card) => card.isDefault) &&
			paymentMethods.length > 0
		) {
			paymentMethods[0].isDefault = true;
		}

		// Sort so that the default card is first
		paymentMethods = paymentMethods.sort((a, b) => b.isDefault - a.isDefault);

		// TODO: Create delete payment method request logic
	}

	function AddPaymentMethod() {
		// TODO: Create add payment method logic
		// TODO: Create add payment method request logic
	}
</script>

<div class="flex flex-col gap-6 w-[276px] max-2xl:gap-4">
	<h3 class="text-2xl font-bold text-interface-50">Payment Methods</h3>

	<div class="flex flex-col gap-4">
		{#each paymentMethods as payment}
			<div
				class="p-4 rounded-2xl border border-[rgba(86,192,240,0.25)] flex flex-col gap-4"
				out:slide={{ duration: 300 }}
			>
				<div class="flex gap-6 flex-wrap">
					<figure class="shrink-0">
						<img
							src={payment.icon}
							alt={payment.cardType}
							width="48"
							height="32"
							class="w-12 h-8"
						/>
					</figure>

					<div class="flex flex-col">
						<p class="text-xs font-bold">••••{payment.last4Digits}</p>
						<p class="text-xs">expires {payment.expiry}</p>
					</div>
				</div>
				<div class="flex justify-between">
					{#if payment.isDefault}
						<p class="text-xs font-bold text-secondary-500">Default</p>
					{:else}
						<button
							type="button"
							class="text-xs font-bold text-interface-400"
							on:click={() => setDefault(payment.id)}
						>
							Set as default
						</button>
					{/if}

					<button
						type="button"
						class="text-xs font-bold text-error-500"
						on:click={() => deletePaymentMethod(payment.id)}
					>
						Delete
					</button>
				</div>
			</div>
		{/each}
	</div>

	<Button
		variant="outline-blue"
		handleClick={AddPaymentMethod}
		className="w-fit h-9"
	>
		Add payment method
	</Button>
</div>
