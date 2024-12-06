<script>
	import { onMount } from "svelte";
	import NoSubscription from "../../assets/about/sub.png";
	import ArrowUp from "../../assets/icons/arrow_upward_alt.svg";

	// Visibility state for the text block
	let textVisible = false;

	// Function to observe visibility
	const observeVisibility = (el) => {
		const observer = new IntersectionObserver(
			(entries) => {
				if (entries[0].isIntersecting) {
					textVisible = true; // Slide in text when it becomes visible
				}
			},
			{ threshold: 0.2 } // Trigger animation earlier (20% visibility)
		);

		observer.observe(el);
	};

	// Observe text block on mount
	onMount(() => {
		observeVisibility(document.querySelector(".text-slide-container"));
	});
</script>

<section
	class="relative max-lg:px-8 max-3xl:px-[300px] px-[526px] pt-16 2xl:pt-[116px] pb-16 2xl:pb-[264px] bg-[#111827] flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-[116px]"
>
	<div
		class="max-w-full 2xl:max-w-[504px] flex flex-col gap-4 text-slide-container"
		class:visible={textVisible}
	>
		<h3
			class="text-primary-500 font-roboto font-bold text-2xl lg:text-3xl 2xl:text-[32px] leading-tight 2xl:leading-[38px] slide-text"
		>
			No Subscription
		</h3>

		<p
			class="font-roboto text-lg lg:text-xl 2xl:text-2xl leading-relaxed 2xl:leading-[28px] mb-5 slide-text"
		>
			We despise subscriptions as much as a cat despises water—passionately and without compromise. 
			That’s why we’ll never ask you to sign up for one. 
			Instead, you get all our regularly updated study materials for a single price, with customized practice exams available through additional one-time purchases.
		</p>
	</div>

	<figure
		class="w-[248px] aspect-square flex justify-center items-center shrink-0"
	>
		<img src={NoSubscription} alt="success" width="248" height="248" />
	</figure>

	<a
		class="button primary-blue absolute right-[40px] bottom-[40px] flex items-center gap-1.5 !font-semibold !text-[16px] !leading-[20px]"
		href="#top"
		>Back to Top
		<img
			src={ArrowUp}
			alt="arrow up"
			class="w-[13px] aspect-square"
			width="13"
			height="13"
		/>
	</a>
</section>

<style>
	/* Base animation styles for sliding text */
	.slide-text {
		opacity: 0;
		transform: translateX(-50px); /* Slide in from the left */
		transition: opacity 1s ease, transform 1s ease;
	}

	/* Visible state for text block */
	.text-slide-container.visible .slide-text {
		opacity: 1;
		transform: translateX(0); /* End at center */
	}
</style>
