<script>
	import { onMount } from "svelte";
	import Handshake from "../../assets/about/handshake.png";
	import ProcessVideo from "../../assets/about/process-video.png";

	// References for elements
	let adaptivityHeader, adaptivityText;
	let handshakeImage;
	let feedbackHeader, feedbackText;
	let processVideo;

	// Visibility states
	let adaptivityVisible = [false, false];
	let handshakeVisible = false;
	let feedbackVisible = [false, false];
	let processVideoVisible = false;

	// Function to observe visibility
	const observeVisibility = (el, index, type) => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						// Element is entering view
						if (type === "adaptivity") adaptivityVisible[index] = true;
						if (type === "handshake") handshakeVisible = true;
						if (type === "feedback") feedbackVisible[index] = true;
						if (type === "processVideo") processVideoVisible = true;
					} else {
						// Element is leaving view
						if (type === "adaptivity") adaptivityVisible[index] = false;
						if (type === "handshake") handshakeVisible = false;
						if (type === "feedback") feedbackVisible[index] = false;
						if (type === "processVideo") processVideoVisible = false;
					}
				});
			},
			{ threshold: 0.2 } // Trigger animations earlier (20% visibility)
		);
		observer.observe(el);
	};

	// Observe elements on mount
	onMount(() => {
		if (adaptivityHeader) observeVisibility(adaptivityHeader, 0, "adaptivity");
		if (adaptivityText) observeVisibility(adaptivityText, 1, "adaptivity");
		if (handshakeImage) observeVisibility(handshakeImage, null, "handshake");
		if (feedbackHeader) observeVisibility(feedbackHeader, 0, "feedback");
		if (feedbackText) observeVisibility(feedbackText, 1, "feedback");
		if (processVideo) observeVisibility(processVideo, null, "processVideo");
	});
</script>

<section
  class="px-8 lg:px-16 xl:px-24 2xl:px-[313px] pt-16 lg:pt-24 xl:pt-[162PX] pb-16 lg:pb-24 xl:pb-[116px] flex flex-col justify-center items-center gap-16 lg:gap-20 xl:gap-[111px] bg-[#111827]"
>
	<div class="flex flex-col xl:flex-row items-start gap-6 xl:gap-8">
		<div class="max-w-full xl:max-w-[504px] flex flex-col gap-4">
			<h3
				class="text-primary-500 font-roboto font-bold text-2xl lg:text-3xl xl:text-[32px] leading-tight"
				bind:this={adaptivityHeader}
				class:visible={adaptivityVisible[0]}
			>
				Adaptivity
			</h3>

			<p
				class="font-roboto text-lg lg:text-xl xl:text-2xl leading-relaxed xl:leading-[28px] max-xl:mb-5"
				bind:this={adaptivityText}
				class:visible={adaptivityVisible[1]}
			>
				Our platform leverages machine learning to create a personalized study experience tailored to your progress. 
				By analyzing your responses, it continuously tunes the material in real-time, ensuring each question focuses precisely on the areas you need to improve. 
				This adaptive model makes every minute count.
			</p>
		</div>

		<figure
			class="self-center shrink-0 w-full max-w-[300px] lg:max-w-[400px] xl:max-w-none xl:w-auto"
			bind:this={handshakeImage}
			class:visible={handshakeVisible}
		>
			<img src={Handshake} alt="handshake" class="w-full h-auto" />
		</figure>

		<div class="max-w-full xl:max-w-[504px] flex flex-col gap-4">
			<h3
				class="text-primary-500 font-roboto font-bold text-2xl lg:text-3xl xl:text-[32px] leading-tight feedback"
				bind:this={feedbackHeader}
				class:visible={feedbackVisible[0]}
			>
				Instant feedback
			</h3>

			<p
				class="font-roboto text-lg lg:text-xl xl:text-2xl leading-relaxed xl:leading-[28px] max-xl:mb-5 self-start xl:self-end feedback"
				bind:this={feedbackText}
				class:visible={feedbackVisible[1]}
			>
				With instant feedback on every question, you’re always aware of where you stand. 
				Our context-driven approach provides detailed explanations of each possible answer and links to related terms, reinforcing your understanding as you go. 
				This interactive feedback loop makes concepts stick in a way that's proven to last.
			</p>
		</div>
	</div>

	<figure
		class="w-full max-w-[600px] max-h-[757px] lg:max-w-[700px] xl:max-w-none flex justify-center"
		bind:this={processVideo}
		class:visible={processVideoVisible}
	>
		<img src={ProcessVideo} alt="process video" class="" />
	</figure>
</section>

<style>
	p, h3 {
		opacity: 0;
		transform: translateX(-50px); /* Default slide-in from left */
		transition: opacity 1s ease, transform 1s ease;
	}

	/* Feedback section slides in from the right */
	p.feedback, h3.feedback {
		transform: translateX(50px); /* Slide in from right */
	}

	/* Visible state */
	p.feedback.visible, h3.feedback.visible,
	p.visible, h3.visible {
		opacity: 1 !important; /* Force visibility */
		transform: translateX(0) !important; /* Force to default position */
	}

	/* Slide in from bottom for handshake image */
	figure {
		opacity: 0;
		transform: translateY(50px);
		transition: opacity 1s ease, transform 1s ease;
	}

	figure.visible {
		opacity: 1 !important; /* Force visibility */
		transform: translateY(0) !important; /* Force to default position */
	}
</style>
