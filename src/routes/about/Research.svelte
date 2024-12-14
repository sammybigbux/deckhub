<script>
	import { onMount } from "svelte";
	import networkDemo from "../../assets/about/network-demo.png";

	// Individual references for elements
	let h3Element;
	let p1Element;
	let p2Element;
	let videoElement;

	// Visibility states
	let textVisible = [false, false, false]; // For h3, p1, and p2
	let videoVisible = false; // Visibility state for the video

	// Function to observe element visibility
	const observeVisibility = (el, index) => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						// Element is entering view
						if (index !== null) {
							textVisible[index] = true;
						} else {
							videoVisible = true;
						}
					} else {
						// Element is leaving view
						if (index !== null) {
							textVisible[index] = false;
						} else {
							videoVisible = false;
						}
					}
				});
			},
			{ threshold: 0.4 } // Trigger animations at 40% visibility
		);
		observer.observe(el);
	};

	// Observe elements on mount
	onMount(() => {
		if (h3Element) observeVisibility(h3Element, 0);
		if (p1Element) observeVisibility(p1Element, 1);
		if (p2Element) observeVisibility(p2Element, 2);
		if (videoElement) observeVisibility(videoElement, null);
	});
</script>

<section 
  class="relative px-8 xl:px-24 2xl:px-[224px] py-16 xl:py-24 bg-[#111827]"
>
  <div class="absolute inset-0 bg-[rgba(59,130,246,0.15)] w-full h-full"></div>
  
  <h3
    class="text-primary-500 font-roboto font-bold text-2xl xl:text-[32px] leading-[37.5px] mb-4 max-w-full xl:max-w-[260px]"
    bind:this={h3Element}
    class:visible={textVisible[0]}
  >
    Why is it faster?
  </h3>

  <div
    class="flex flex-col xl:flex-row items-center gap-8 xl:gap-16 2xl:gap-[214px]"
  >
    <div class="flex flex-col gap-7 max-w-full xl:max-w-[480px]">
      <p
        class="font-roboto text-lg xl:text-2xl leading-relaxed xl:leading-[28px]"
        bind:this={p1Element}
        class:visible={textVisible[1]}
      >
        Instead of spending hours on video courses and endless notes, imagine a guided learning path that adapts with each answer you give, targeting only the concepts you need to master. That’s exactly what our platform provides. 
      </p>

      <p
        class="font-roboto text-lg xl:text-2xl leading-relaxed xl:leading-[28px]"
        bind:this={p2Element}
        class:visible={textVisible[2]}
      >
        Using a <strong>hierarchy-based model</strong>, we organize study material into three sections—Diagnostic, Concept Explorer, and Term Mastery—becoming more specific as you progress as our model continuously learns from your answers. Our real-time 'time saved' counter lets you see the efficiency in action, with the average user saving <strong>13 hours</strong> overall.
      </p>
    </div>

    <figure
      class="max-w-full xl:max-w-[850px] min-w-[300px] h-auto mt-[-20px]"
      bind:this={videoElement}
      class:visible={videoVisible}
    >
      <img
        src={networkDemo}
        alt="research video"
        class="w-full h-auto xl:max-w-[850px] xl:max-h-[600px]"
      />
    </figure>
  </div>
</section>

<style>
	/* Animation for sliding text */
	h3, p {
		opacity: 0;
		transform: translateX(-50px);
		transition: opacity 1s ease, transform 1s ease; /* Slower transition */
	}
	
	/* Slide in from left */
	.visible {
		opacity: 1;
		transform: translateX(0);
	}

	/* Animation for sliding video */
	figure {
		opacity: 0;
		transform: translateX(50px);
		transition: opacity 1s ease, transform 1s ease; /* Slower transition */
	}

	figure.visible {
		opacity: 1;
		transform: translateX(0);
	}
</style>
