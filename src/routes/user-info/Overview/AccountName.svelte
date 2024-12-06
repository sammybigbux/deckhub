<script lang="ts">
	import { logout, userEmail, userName } from "$lib/firebase";
	import EditIcon from "../../../assets/icons/edit-pen-rounded.svg";
	import { derived, writable } from "svelte/store";
	import Button from "../../../components/Button.svelte";

	type InputStates = {
		[key: string]: boolean;
	};

	const inputStates = writable<InputStates>({
		emailDisabled: true,
		firstNameDisabled: true,
		lastNameDisabled: true,
	});

	let emailInput: HTMLInputElement;
	let firstNameInput: HTMLInputElement;
	let lastNameInput: HTMLInputElement;

	function toggleInputState(
		key: keyof InputStates,
		inputRef: HTMLInputElement
	) {
		inputStates.update((state) => {
			const newState = { ...state, [key]: !state[key] };
			if (!newState[key]) {
				// If input is enabled, focus on it
				setTimeout(() => inputRef.focus(), 0);
			} else {
				// TODO: add save changes logic and the input validations
			}
			return newState;
		});
	}

	function deleteAccount() {
		// TODO: Add Delete Account logic

		logout();
	}

	const displayFirstName = derived(
		userName,
		($userName) => $userName.split(" ")[0]
	);
	const displayLastName = derived(
		userName,
		($userName) => $userName.split(" ")[1]
	);
</script>

<div class="flex flex-col gap-8 w-[300px] max-2xl:gap-5">
	<h3 class="text-2xl font-bold text-interface-50">Account Name</h3>

	<form class="flex flex-col gap-8 max-2xl:gap-4">
		<div class="flex flex-col gap-2">
			<label for="email" class="text-interface-50 font-bold">Email:</label>
			<div class="flex gap-3">
				<input
					type="text"
					id="email"
					name="email"
					class="px-4 py-2 w-[268px] bg-interface-600 border-none rounded-xl text-interface-50 placeholder-interface-50 text-xs disabled:bg-interface-700 placeholder:text-xs disabled:placeholder:text-interface-400"
					placeholder={$userEmail || "Enter Your Email"}
					disabled={$inputStates.emailDisabled}
					bind:this={emailInput}
				/>

				<button
					on:click={() => toggleInputState("emailDisabled", emailInput)}
					type="button"
				>
					<figure><img src={EditIcon} alt="edit" /></figure>
				</button>
			</div>
		</div>

		<div class="flex flex-col gap-2">
			<label for="name" class="text-interface-50 font-bold">First name:</label>
			<div class="flex gap-3">
				<input
					type="text"
					id="name"
					name="name"
					class="px-4 py-2 w-[268px] bg-interface-600 border-none rounded-xl text-interface-50 placeholder-interface-50 text-xs disabled:bg-interface-700 placeholder:text-xs disabled:placeholder:text-interface-400"
					placeholder={$displayFirstName || "Enter Your First Name"}
					disabled={$inputStates.firstNameDisabled}
					bind:this={firstNameInput}
				/>

				<button
					on:click={() => toggleInputState("firstNameDisabled", firstNameInput)}
					type="button"
				>
					<figure><img src={EditIcon} alt="edit" /></figure>
				</button>
			</div>
		</div>

		<div class="flex flex-col gap-2">
			<label for="name" class="text-interface-50 font-bold">Last name:</label>
			<div class="flex gap-3">
				<input
					type="text"
					id="name"
					name="name"
					class="px-4 py-2 w-[268px] bg-interface-600 border-none rounded-xl text-interface-50 placeholder-interface-50 text-xs disabled:bg-interface-700 placeholder:text-xs disabled:placeholder:text-interface-400"
					placeholder={$displayLastName || "Enter Your First Name"}
					disabled={$inputStates.lastNameDisabled}
					bind:this={lastNameInput}
				/>

				<button
					on:click={() => toggleInputState("lastNameDisabled", lastNameInput)}
					type="button"
				>
					<figure><img src={EditIcon} alt="edit" /></figure>
				</button>
			</div>
		</div>
	</form>

	<Button
		variant="primary-blue"
		className="w-fit text-xs font-semibold leading-5 !px-[40px]"
		handleClick={() => logout()}
	>
		Logout
	</Button>

	<div class="flex flex-col gap-2 max-2xl:gap-1">
		<p class="text-base font-bold text-interface-50">Acount</p>
		<button
			class="text-error-400 font-bold text-xs w-fit"
			type="button"
			on:click={deleteAccount}
		>
			Delete Account
		</button>
	</div>
</div>
