<script>
	import { onMount } from "svelte";
	import Success from "../../assets/about/rounded-success.png";
	import SuccessLine from "../../assets/about/success-with-line.png";

	// References for "Learn," "Understand," "Apply"
	let learnText, understandText, applyText;

	// Visibility states
	let textVisible = [false, false, false];
	let fastMasteryVisible = false;

	// Function to start animations with a delay
	const startAnimations = () => {
		setTimeout(() => {
			textVisible[0] = true; // Learn
			setTimeout(() => (textVisible[1] = true), 500); // Understand
			setTimeout(() => (textVisible[2] = true), 1000); // Apply
		}, 1000); // 2-second delay before starting the bounce animations
	};

	// Observe visibility to trigger animation
	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				if (entries[0].isIntersecting) {
					startAnimations();
					fastMasteryVisible = true; // Slide in "Fast mastery"
				}
			},
			{ threshold: 0.2 } // Trigger animations earlier (20% visibility)
		);

		observer.observe(document.querySelector(".text-animation-container")); // Observe container
	});
</script>

<section
	class="relative max-lg:px-8 max-3xl:px-[300px] px-[526px] pt-16 2xl:pt-[148px] pb-16 2xl:pb-[266px] flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-[129px] bg-[#111827]"
>
	<div class="absolute inset-0 bg-[rgba(59,130,246,0.15)] w-full h-full"></div>

	<!-- Left Nodes and Lines -->
	<div class="flex flex-col text-animation-container">
		<div class="flex items-center gap-6 2xl:gap-[28px]">
			<figure class="shrink-0">
				<img src={Success} alt="success" />
			</figure>
			<p
				class="text-xl 2xl:text-2xl font-bold leading-6 2xl:leading-[20px] bounce-text"
				bind:this={learnText}
				class:visible={textVisible[0]}
			>
				Pinpoint Weaknesses
			</p>
		</div>
		<div class="flex items-center gap-6 2xl:gap-[28px]">
			<figure class="shrink-0">
				<img src={SuccessLine} alt="success" />
			</figure>
			<p
				class="text-xl 2xl:text-2xl font-bold leading-6 2xl:leading-[20px] bounce-text"
				bind:this={understandText}
				class:visible={textVisible[1]}
			>
				Custom Test Plan
			</p>
		</div>
		<div class="flex items-center gap-6 2xl:gap-[28px]">
			<figure class="shrink-0">
				<img src={Success} alt="success" />
			</figure>
			<p
				class="text-xl 2xl:text-2xl font-bold leading-6 2xl:leading-[20px] bounce-text"
				bind:this={applyText}
				class:visible={textVisible[2]}
			>
				Guided Practice
			</p>
		</div>
	</div>

	<!-- Right Text Section -->
	<div class="max-w-full 2xl:max-w-[505px]">
		<h3
			class="text-primary-500 font-roboto font-bold text-2xl 2xl:text-[32px] leading-tight 2xl:leading-[36px] mb-4 slide-text"
			class:visible={fastMasteryVisible}
		>
			Fast mastery.
		</h3>

		<p
			class="font-roboto text-lg 2xl:text-2xl leading-relaxed 2xl:leading-[28px] slide-text"
			class:visible={fastMasteryVisible}
		>
		With a diagnostic test that pinpoints your weaknesses, a custom study plan tailored to your needs, and guided practice that adapts as you learn, our platform enables you to master technical certification material in half the time of traditional study methods. 
			For the AWS SAA-C03 exam, our median user reported passing after just <strong>17 hours</strong>, compared to the median study time of <strong>30 hours</strong> as reported by Amazon.
		</p>
	</div>
</section>

<style>
	/* Base animation styles for bounce text */
	.bounce-text {
		opacity: 0;
		transform: scale(0.8); /* Shrink initially */
		transition: opacity 0.5s ease, transform 0.5s ease;
	}

	.bounce-text.visible {
		opacity: 1;
		transform: scale(1); /* Bounce into full size */
	}

	/* Base animation styles for sliding text */
	.slide-text {
		opacity: 0;
		transform: translateX(50px); /* Slide in from the right */
		transition: opacity 1s ease, transform 1s ease;
	}

	.slide-text.visible {
		opacity: 1;
		transform: translateX(0); /* End at center */
	}
</style>
