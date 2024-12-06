<script lang="js">
	import { writable } from "svelte/store";
	import InfoIcon from "../../../assets/icons/info-icon.svg";
	import CheckCircleIcon from "../../../assets/icons/check-circle.svg";
	import Button from "../../../components/Button.svelte";
	import AddCreditModal from "./AddCreditModal.svelte";
	import RechargeModal from "./RechargeModal.svelte";
	import { fade } from "svelte/transition";

	const accountBalanceData = writable({
		balance: 5,
		isRechargeable: true,
	});

	let addCreditModalOpen = false;
	let rechargeModalOpen = false;

	const handleModifyRechargeOpen = () => (rechargeModalOpen = true);

	const handleModifyRechargeClose = () => (rechargeModalOpen = false);

	const handleAddToCreditBalanceOpen = () => (addCreditModalOpen = true);

	const handleAddToCreditBalanceModalClose = () => (addCreditModalOpen = false);

	const handleCancelPlan = () => {
		accountBalanceData.update((data) => ({
			...data,
			isRechargeable: false,
		}));
	};
</script>

<div class="flex flex-col gap-6 w-[338px] max-2xl:gap-4">
	<h3 class="text-2xl font-bold text-interface-50">Account Balance</h3>

	<div class="flex flex-col gap-1">
		<p class="text-2xl text-secondary-500 font-bold">
			${$accountBalanceData.balance.toFixed(2)}
		</p>
		<p class="flex gap-2 text-xs">
			16 questions remaining <img src={InfoIcon} alt="info" />
		</p>
	</div>

	<div class="flex flex-col gap-4">
		<div
			class="p-4 rounded-2xl border border-[rgba(86,192,240,0.25)] flex flex-col gap-4"
		>
			<div class="flex flex-col gap-2">
				<p class="flex gap-1 text-xs font-bold items-center">
					{#if $accountBalanceData.isRechargeable}
						<img
							src={CheckCircleIcon}
							alt="check"
							width="12"
							height="12"
							class="w-3 h-3 mb-1"
						/>
						<span>Auto recharge is on.</span>
					{:else}
						<span in:fade={{ duration: 400 }}>
							Auto recharge is turned off.</span
						>
					{/if}
				</p>
				{#if $accountBalanceData.isRechargeable}
					<p class="text-xs">
						When your balance reaches $0.00, your payment method will
						automatically be charged to bring your balance up to $10.00.
					</p>
				{/if}
			</div>
			<button
				class="text-secondary-500 font-bold text-xs w-fit"
				type="button"
				on:click={() => handleModifyRechargeOpen()}
			>
				{#if $accountBalanceData.isRechargeable}
					Modify
				{:else}
					Turn on
				{/if}
			</button>
		</div>

		<div class="flex gap-4">
			<Button
				variant="outline-blue" 
				className="h-9"
				handleClick={() => handleAddToCreditBalanceOpen()}
			>
				Add to credit balance
			</Button>
			<Button 
				variant="outline-blue" 
				className="h-9" 
				handleClick={() => handleCancelPlan()}
			>
				Cancel plan
			</Button>
		</div>
	</div>

	<div class="flex flex-col gap-4 max-2xl:gap-2">
		<p class="text-base font-bold text-interface-50">Pricing</p>
		<a
			href="/pricing-faq"
			class="text-xs leading-5 font-bold text-secondary-500"
		>
			View pricing guide and FAQ
		</a>
	</div>

	<RechargeModal
		open={rechargeModalOpen}
		onClose={handleModifyRechargeClose}
		{accountBalanceData}
	/>
	<AddCreditModal
		open={addCreditModalOpen}
		onClose={handleAddToCreditBalanceModalClose}
		{accountBalanceData}
	/>
</div>
