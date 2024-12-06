<script lang="js">
	import Button from "../../../components/Button.svelte";

	const data = [
		{
			id: 1,
			product: "AWS SAA-C03 Exam",
			amount: 29.99,
			date: "Oct 1, 2024, 3:02 PM",
			isFunded: false,
		},
		{
			id: 2,
			product: "Exam name",
			amount: 29.99,
			date: "Oct 1, 2024, 3:02 PM",
			isFunded: false,
		},
		{
			id: 3,
			product: "Exam name",
			amount: 29.99,
			date: "Oct 1, 2024, 3:02 PM",
			isFunded: true,
		},
	];

	const handleReportIssue = (productId) => () => {
		console.log(productId);
	};

	const handleRefund = (productId) => () => {
		data[productId - 1].isFunded = true;
	};
</script>

<section class="flex flex-col gap-8 [&_*]:leading-none">
	<div class="flex flex-col gap-2">
		<h3 class="font-bold text-base text-interface-50">Past Orders</h3>
		<p class="text-xs text-interface-50">
			Showing orders from the past 12 months
		</p>
	</div>

	<div class="text-interface-50 text-xs">
		<!-- Table Header -->
		<div
			class="flex items-center pb-2 border-b border-[rgba(86,192,240,0.25)] font-bold"
		>
			<div class="w-full max-w-[267px]">Product</div>
			<div class="w-full max-w-[71px]">Amount</div>
			<div class="w-full max-w-[533px]">Transaction Date</div>
		</div>

		<!-- Table Body -->
		<div class="max-h-[195px] overflow-y-auto">
			{#each data as item}
				<div
					class="flex items-center py-4 border-b border-[rgba(86,192,240,0.25)]"
				>
					<div class="w-full max-w-[267px]">{item.product}</div>
					<div class="w-full max-w-[71px]">${item.amount.toFixed(2)}</div>
					<div class="w-full max-w-[533px]">{item.date}</div>
					<div class="w-full max-w-[204px] flex justify-between items-center">
						<button
							type="button"
							class="py-1 px-2 text-xs font-semibold text-interface-300"
							on:click={handleReportIssue(item.id)}
						>
							Report and issue
						</button>

						{#if item.isFunded}
							<div
								class="rounded-lg py-1 px-2 font-semibold text-xs text-interface-50 bg-secondary-800"
							>
								Refunded
							</div>
						{:else}
							<Button
								variant="primary-blue"
								type="button"
								className="!rounded-lg !py-1 !px-2 !font-semibold !text-xs !text-interface-50 !min-w-fit"
								handleClick={handleRefund(item.id)}>Refund</Button
							>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	</div>
</section>
