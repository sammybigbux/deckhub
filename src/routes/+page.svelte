<script>
	// Import necessary functions from Firebase
	import { initializeApp } from "firebase/app";
	import { getAuth } from "firebase/auth";
	import { goto } from '$app/navigation';

	// Firebase configuration
	const firebaseConfig = {
		apiKey: "AIzaSyC-ZOP0oH3IISFl3Qwzc7rGnbEB5VwYOps",
		authDomain: "deckhubapp.firebaseapp.com",
		projectId: "deckhubapp",
		storageBucket: "deckhubapp.appspot.com",
		messagingSenderId: "1086653848406",
		appId: "1:1086653848406:web:ad7fa7ec34c3061cc694f7",
	};

	// Initialize Firebase and authentication
	const app = initializeApp(firebaseConfig);
	const auth = getAuth(app);

	function handleClick() {
      const slug = encodeURIComponent("AWS Certified Solutions Architect"); // Ensure the slug is URL-safe
      goto(`/new/learn/${slug}`); // Navigate to the dynamic route
    }

	import { loginWithGoogle, isLoggedIn } from '$lib/firebase';
</script>

<div class="page-content flex items-center justify-start relative">
	<div class="content-wrapper flex flex-col gap-6 items-start relative z-10 max-w-[768px]">
		<h1 class="font-bold text-5xl leading-[58px] tracking-[1.7px]">
			Pass your technical certification exam in <span class="text-primary-500">record time</span>
		</h1>
		<p class="font-medium text-2xl leading-[29px] tracking-wide">
			Accelerate your path to cloud certification with a study guide that adapts to you, helping you cover all exam material in half the time.
		</p>
		<div class="flex items-center gap-6">
			<a href="/about" class="button outline-blue w-[233px]">About</a>
			{#if $isLoggedIn}
				<a on:click={handleClick} href="/diagnostic-welcome" class="button primary-blue w-[233px]">AWS SAA03 Practice</a>
			{:else}
				<button on:click={loginWithGoogle} class="button primary-blue w-[233px]">Try it out</button>
			{/if}
		</div>
	</div>
</div>

<style>
	/* Set a global box-sizing to contain padding within elements */
	*,
	*::before,
	*::after {
		box-sizing: border-box;
	}

	html, body {
		height: 100%;
		margin: 0;
		overflow: hidden;
	}

	.page-content {
		width: 100%;
		height: 100%;
		padding-left: 192px; /* Keeps the text padding on the left */
		display: flex;
		align-items: center;
		overflow: hidden;
	}

	.page-content::after {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-image: url("/assets/frontPage.png");
		background-size: cover;
		background-position: center;
		opacity: 0.6;
		z-index: 1;
	}

	.content-wrapper {
		transform: translateY(-5%); /* Moves the content up slightly */
	}
</style>
