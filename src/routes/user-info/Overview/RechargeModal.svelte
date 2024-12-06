<script lang="js">
	import Modal from "../../../components/Modal.svelte";
	import CloseIcon from "../../../assets/icons/close_small.svg";
	import Button from "../../../components/Button.svelte";
	import CreditSelect from "./CreditSelect.svelte";
	import AmountBtns from "./AmountBtns.svelte";

	export let open = false;
	export let onClose = () => {
		open = false;
	};
	export let accountBalanceData;

	let isChangeCardOpen = false;
	let refillAmountInput;
	let refillThresholdInput;

	const handleClose = () => {
		refillAmountInput.value = 0;
		refillThresholdInput.value = 0;
		onClose();
	};

	const handleTurnOff = () => {
		accountBalanceData.update((data) => ({ ...data, isRechargeable: false }));
		handleClose();
	};

	const handleSave = () => {
		accountBalanceData.update((data) => ({
			...data,
			balance: Number(refillAmountInput.value) + data.balance,
			isRechargeable: true,
		}));
		handleClose();
	};
</script>

<Modal {open} onClose={handleClose}>
	<div
		class="p-6 w-[324px] min-h-[504px] bg-interface-700 rounded-3xl flex flex-col gap-8"
	>
		<div class="flex flex-col gap-6">
			<div class="flex justify-between items-center">
				<h2 class="text-base font-bold text-[#F9FAFB]">Auto Recharge</h2>

				<button type="button" on:click={onClose}>
					<img src={CloseIcon} alt="close" width="10" height="10" />
				</button>
			</div>

			<div class="flex flex-col gap-2">
				<div class="flex justify-between items-center">
					<label for="refill-amount" class="text-interface-50 font-bold text-xs"
						>Refill Amount:</label
					>
					<input
						type="number"
						id="refill-amount"
						name="refill-amount"
						class="w-[172px] h-[31px] py-2 px-4 bg-transparent rounded-xl text-interface-50 placeholder-interface-400 text-xs border border-interface-400"
						placeholder="$10.00"
						bind:this={refillAmountInput}
					/>
				</div>

				<AmountBtns inputRef={refillAmountInput} />
			</div>

			<div class="flex justify-between items-center">
				<label
					for="refill-threshold"
					class="text-interface-50 font-bold text-xs">Refill Threshold:</label
				>
				<input
					type="number"
					id="refill-threshold"
					name="refill-threshold"
					class="w-[172px] h-[31px] py-2 px-4 bg-transparent rounded-xl text-interface-50 placeholder-interface-400 text-xs border border-interface-400"
					placeholder="$0.00"
					bind:this={refillThresholdInput}
				/>
			</div>
		</div>

		<CreditSelect {isChangeCardOpen} />

		<div class="flex flex-col gap-4">
			<Button
				variant="primary-red"
				className="w-full"
				handleClick={handleTurnOff}>Turn Off</Button
			>
			<Button variant="primary-blue" className="w-full" handleClick={handleSave}
				>Save</Button
			>
		</div>
	</div></Modal
>
