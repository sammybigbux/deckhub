<script lang="ts">
  import ProgressBar from "../../../../components/ProgressBar.svelte";
  import Button from "../../../../components/Button.svelte";
  import CompletedIcon from "../../../../assets/icons/check-circle.svg";
  import LockIcon from "../../../../assets/icons/Lock-Icon.svg";
  import Star from "../../../../assets/icons/star.svg";
  import { goto } from '$app/navigation';  // Import goto for navigation
  import { already_initialized, active_section_title, moduleName } from '../../../../stores/random_store';
  import { userId } from '../../../../lib/firebase';
  import { get } from 'svelte/store';
  

  export let title: string = "Learn";
  export let description: string =
    "Gain new knowledge and familiarity with key terms.";
  export let progressValue: number = 0;
  export let progressMax: number = 0;
  export let isLocked: boolean = (progressValue === 0 && progressMax === 0);
  export let standardLink: string = "/learn-multiple";
  export let smartLink: string = "/learn-open";
  export let viewLink: string = "";

  const moduleLevels = {
    "Diagnostic": "apply",
    "Concept Explorer": "understand",
    "Term Mastery": "learn"
  };

  async function getUserID() {
    return new Promise((resolve, reject) => {
      const uid = get(userId);  // Get current value of userId
      if (uid) {
        resolve(uid);  // If userID is already set, return it
      } else {
        // Wait for userID to be populated
        const unsubscribe = userId.subscribe(value => {
          if (value) {
            resolve(value);
            unsubscribe();  // Unsubscribe once the userID is populated
          }
        });
      }
    });
  }

  let isCompleted = progressValue === progressMax;
  let activeSection = "";
  const base_url = import.meta.env.VITE_BASE_URL;

  const handleView = () => {
    // Use SvelteKit's goto function for navigation

    goto(viewLink);
  };

  async function initializeEnv() {
    const userID = await getUserID();  // Wait for userID to be populated
    const payload = { userID: userID, module: moduleLevels[title] };  // Add userID to the payload

    try {
      const response = await fetch(`${base_url}/initialize_env`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Failed to initialize environment: ${response.statusText}`);
      }
      console.log('Environment initialized successfully.');
    } catch (error) {
      console.error('Error initializing environment:', error);
    }
  }

  async function fetchSectionsData() {
    let activeSection = null;
    try {
      const userIdValue = get(userId);
      console.log("User id is: ", userIdValue);
      const response = await fetch(`${base_url}/get_section_data?userID=${userIdValue}`, {
        method: 'GET'
      });

      if (!response.ok) {
        throw new Error('Failed to fetch sections data');
      }

      // Parse the JSON response and assign it to SECTIONS_DATA
      let SECTIONS_DATA = await response.json();

      // Update values for progress bar
      SECTIONS_DATA.forEach(section => {
          section.sections.forEach(subSection => {
            if (subSection.isActive) {
              activeSection = subSection;
              active_section_title.set(activeSection.title);
            }
          });
        });

      } catch (error) {
        console.error('Error fetching sections data:', error);
      }
      return activeSection;
    }

    // Function to handle the button click
    async function navigate_to_chat() {
      const slug = "AWS Certified Solutions Architect";
      try {
        await initializeEnv();
        const fetchedSection = await fetchSectionsData(); // Fetch the section data
        already_initialized.set(true); // Reset already_initialized
        goto(`/new/learn/${slug}/open/?module=${$moduleName}&section=${fetchedSection.title}`); // Navigate to the overview page
      } catch (error) {
        console.error('Error handling continue click:', error);
      }
    }

</script>

<li>
  <div
    class="relative rounded-3xl px-4 py-6 w-[300px] h-[280px] min-h-[280px] flex flex-col items-center gap-6 text-center mb-6 {isLocked
      ? 'bg-[#1E40AF]/10 text-interface-400'
      : isCompleted
        ? 'bg-[#075B3F]/10 text-interface-50'
        : 'bg-[#3B82F6]/10 duration-300 group-hover:h-[355px] text-interface-50'}"
  >
    <h1 class="title {isLocked ? '!text-interface-400' : ''}">{title}</h1>
    <p class="text-xs leading-[20px]">{description}</p>

    {#if isCompleted}
      <div
        class="flex flex-col gap-6 items-center justify-center w-full mt-auto"
      >
        <figure><img src={CompletedIcon} alt="completed" /></figure>
        <Button
          variant="primary-green"
          on:click={handleView}
          className="w-full"
        >
          View
        </Button>
      </div>
    {:else if isLocked}
      <figure class="opacity-85"><img src={LockIcon} alt="Locked" /></figure>
    {:else}
      <div
        class="flex flex-col gap-6 items-center w-full text-interface-50 mt-[80px] duration-300 group-hover:mt-0"
      >
        <Button
          variant="primary-green"
          on:click={handleView}
          className="w-full"
        >
          Overview
        </Button>
        <div
          class="absolute bottom-6 inset-x-0 flex flex-col gap-6 items-center duration-300 transition-opacity opacity-0 group-hover:opacity-100"
        >
          <div class="h-[1px] w-full bg-[#56C0F0]/25" />
          <p class="title">Study</p>
          <Button
            variant="primary-blue"
            on:click={navigate_to_chat}
            className="w-full"
          >
            Continue
          </Button>
        </div>
      </div>
    {/if}
  </div>
  {#if !(progressValue === 0 && progressMax === 1)}
    <ProgressBar
      max={progressMax}
      value={progressValue}
      {isLocked}
      containerBg="rgba(30,64,175,0.1)"
    />
  {/if}
</li>
