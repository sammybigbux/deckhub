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
	let amountInput;

	const handleClose = () => {
		amountInput.value = 0;
		onClose();
	};

	const handleSave = () => {
		accountBalanceData.update((data) => ({
			...data,
			balance: Number(amountInput.value) + data.balance,
		}));
		handleClose();
	};
</script>

<Modal {open} onClose={handleClose}>
	<div class="p-6 w-[324px] bg-interface-700 rounded-3xl flex flex-col gap-8">
		<div class="flex flex-col gap-6">
			<div class="flex justify-between items-center">
				<h2 class="text-base font-bold text-[#F9FAFB]">Auto Recharge</h2>

				<button type="button" on:click={onClose}>
					<img src={CloseIcon} alt="close" width="10" height="10" />
				</button>
			</div>

			<div class="flex flex-col gap-2">
				<div class="flex justify-between items-center">
					<label for="amount" class="text-interface-50 font-bold text-xs"
						>Amount:</label
					>
					<input
						type="number"
						id="amount"
						name="amount"
						class="w-[217px] h-[31px] py-2 px-4 bg-transparent rounded-xl text-interface-50 placeholder-interface-400 text-xs border border-interface-400"
						placeholder="$0.00"
						bind:this={amountInput}
					/>
				</div>

				<AmountBtns inputRef={amountInput} />
			</div>
		</div>

		<CreditSelect {isChangeCardOpen} />

		<Button variant="primary-blue" className="w-full" handleClick={handleSave}
			>Add funds</Button
		>
	</div>
</Modal>
