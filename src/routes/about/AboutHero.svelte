<script>
	import homePreview from "../../assets/about/home-preview.svg";
	import DiagnosticMini from "../../assets/about/DiagnosticMini.mp4";
</script>

<section
	class="flex flex-col items-center justify-center max-2xl:gap-8 gap-[108px] pt-8 2xl:pt-[40px] px-8 lg:px-[50px] xl:px-[200px] 2xl:px-[402px] pb-10 lg:pb-[160px]"
>
	<h1 class="font-bold text-2xl lg:text-4xl">About</h1>

	<div class="flex flex-col gap-8 lg:gap-[40px] justify-center items-center">
		<figure class="w-full max-w-[90%] lg:max-w-[818px]">
			<img src={homePreview} alt="home laptop preview" class="w-full h-auto" />
		</figure>
		<!-- <video 
			src={DiagnosticMini} 
			autoplay 
			muted 
			loop 
			class="absolute top-[15%] left-[10%] w-[80%] h-[70%]" 
		/> -->

		<p
			class="text-lg lg:text-[28px] 2xl:text-[32px] font-roboto leading-7 xl:leading-9 2xl:leading-[46px] text-center max-w-full lg:max-w-[1110px] font-medium"
		>
			Our platform makes cloud certification prep 
			<span class="emphasize emphasize-1">faster</span> and 
			<span class="emphasize emphasize-2">more impactful</span>. 
			<br /><br />
			By tailoring content to your responses, our predictive model 
			<span class="emphasize emphasize-3">cuts study time</span>, while our tools for instant feedback and context ensure 
			<span class="emphasize emphasize-4">lasting retention</span>.
		</p>
	</div>
</section>

<style>
	/* Base style for emphasized text */
	.emphasize {
		color: #007BFF; /* Adjust primary color */
		font-weight: bold;
		position: relative;
	}

	.emphasize::after {
		content: '';
		position: absolute;
		left: 0;
		bottom: -2px;
		width: 0;
		height: 2px;
		background-color: #007BFF;
		animation: underline 0.4s ease-in-out forwards;
	}

	/* Specific animations for each span */
	.emphasize-1::after {
		animation-delay: 1s;
	}

	.emphasize-2::after {
		animation-delay: 1.5s;
	}

	.emphasize-3::after {
		animation-delay: 2.5s; /* Pause after the first two animations */
	}

	.emphasize-4::after {
		animation-delay: 3s;
	}

	/* Keyframes for underline animation */
	@keyframes underline {
		from {
			width: 0;
		}
		to {
			width: 100%;
		}
	}

		figure {
		position: relative; /* Ensures video is positioned relative to the image */
	}

	video {
		object-fit: cover; /* Ensures the video fills the space proportionally */
		pointer-events: none; /* Prevents interaction with the video */
		border-radius: 4px; /* Optional: adds slight rounding to match screen corners */
	}
</style>
