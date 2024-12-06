<script lang="js">
	import Button from "../../../components/Button.svelte";

	export let inputRef;
</script>

<div class="flex justify-between">
	<Button
		variant="primary-green"
		className="!py-1 !px-2 !rounded-lg !text-xs !w-auto !min-w-fit !font-semibold"
		handleClick={() => (inputRef.value = 5)}>$5.00</Button
	>
	<Button
		variant="primary-green"
		className="!py-1 !px-2 !rounded-lg !text-xs !w-auto !min-w-fit !font-semibold"
		handleClick={() => (inputRef.value = 10)}>$10.00</Button
	>
	<Button
		variant="primary-green"
		className="!py-1 !px-2 !rounded-lg !text-xs !w-auto !min-w-fit !font-semibold"
		handleClick={() => (inputRef.value = 15)}>$15.00</Button
	>
	<Button
		variant="primary-green"
		className="!py-1 !px-2 !rounded-lg !text-xs !w-auto !min-w-fit !font-semibold"
		handleClick={() => (inputRef.value = 20)}>$20.00</Button
	>
</div>
