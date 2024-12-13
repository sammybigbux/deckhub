<script>
  import { page } from "$app/stores";
  import Button from "../../../../../components/Button.svelte";
  import ArrowRight from "../../../../../assets/icons/route-arrow.svg";
  import ReturnIcon from "../../../../../assets/icons/return-icon.svg";
  import ExamModule from "./ExamModule.svelte";
  import SectionDetails from "./SectionDetails.svelte";
  import ProgressBar from "../../../../../components/ProgressBar.svelte";
  import BreadcrumbRoute from "../../../../../components/BreadcrumbRoute.svelte";
  import { userId } from '../../../../../lib/firebase';
  import { onMount, onDestroy } from 'svelte';
  import { get } from 'svelte/store';
  import { Avatar } from "@skeletonlabs/skeleton";
  import { goto } from '$app/navigation'; // Added for navigatio
  import {active_section_title, moduleName} from "../../../../../stores/random_store";

  const isLocalhost = true;
  const base_url = import.meta.env.VITE_BASE_URL;

  let selectedSectionTitle = '';
  let activeSection = null;
  let isDataFetched = false;

  $: slug = $page.params.slug;
  $: {
    const searchParams = new URLSearchParams($page.url.search);
    moduleName.set(searchParams.get("module"));
  }

  const moduleLevels = {
    "Diagnostic": "apply",
    "Concept Explorer": "understand",
    "Term Mastery": "learn"
  };

  $: isOpenSection = false;
  let completed = 0;
  let total = 0;
  let SECTIONS_DATA = [];
  let TERMS_LIST = [];
  let cleanupEnvTriggered = false; // Ensure that cleanup is only called once

  // Fetch sections data
  async function fetchSectionsData() {
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
      SECTIONS_DATA = await response.json();
      
      // Update values for progress bar
      SECTIONS_DATA.forEach(section => {
        section.sections.forEach(subSection => {
          total += 1;
          if (subSection.isCompleted) {
            completed += 1;
          }
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

  async function fetchTermData(active_section) {
    const userIdValue = get(userId);
    if (!active_section) {
      console.error('No active section found');
      return;
    }

    try {
      const response = await fetch(`${base_url}/get_term_list?section=${active_section}&userId=${userIdValue}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch term data');
      }

      // Set TERMS_LIST with the JSON response
      TERMS_LIST = await response.json();
      console.log('Terms list:', TERMS_LIST);

    } catch (error) {
      console.error('Error fetching term data:', error);
    }
    isDataFetched = true;
  }

  const handleResume = () => {
    cleanupEnvTriggered = true;
    // Use SvelteKit's goto function for navigation
    goto(`/new/learn/${slug}/open?module=${$moduleName}&section=${activeSection.title}`);
  };

  const handleOpenSection = () => {
    isOpenSection = true;
  };

  function handleSectionClick(event) {
    selectedSectionTitle = event.detail.title;
    isOpenSection = true;
  }

  const handleCloseSection = () => {
    isOpenSection = false;
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

  async function initializeEnv() {
    const userID = await getUserID();  // Wait for userID to be populated
    const payload = { userID: userID, module: moduleLevels[$moduleName]};  // Add userID to the payload

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

  async function sendCleanupEnv() {
    const userID = await getUserID();
    const payload = JSON.stringify({ userID: userID });

    // Use Blob to send JSON data via sendBeacon
    const blob = new Blob([payload], { type: 'application/json' });
    navigator.sendBeacon(`${base_url}/cleanup_env`, blob);
  }

  async function cleanupEnv() {
    const userID = await getUserID();
    const payload = { userID: userID };

    try {
      const response = await fetch(`${base_url}/cleanup_env`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Failed to clean up environment: ${response.statusText}`);
      }
      console.log('Environment cleaned up successfully.');
    } catch (error) {
      console.error('Error cleaning up environment:', error);
    }
  }

  onMount(async () => {
    // Wait for `userId` to be defined before calling fetch
    await initializeEnv();

    if (typeof window !== 'undefined') {
      window.addEventListener('beforeunload', (event) => {
        if (!cleanupEnvTriggered) {
          cleanupEnvTriggered = true;
          // Use navigator.sendBeacon for cleanup before the page unloads
          sendCleanupEnv();
        }
      });
    }

    // Once `userId` is available, fetch the sections data
    let active_section = await fetchSectionsData();
    if (active_section) {
      await fetchTermData(active_section.title);
    } else {
      isDataFetched = true;
      active_section = "Completed";
    }
  });

  onDestroy(async () => {
    // Cleanup logic when navigating away within the app
    // if (!cleanupEnvTriggered) {
    //   await cleanupEnv();  // Await the cleanup to ensure it completes
    //   cleanupEnvTriggered = true;
    // }

    // Ensure window object exists before using it (for SSR compatibility)
    if (typeof window !== 'undefined') {
      window.removeEventListener('beforeunload', sendCleanupEnv);
    }
  });
</script>

<div class="pt-8 pb-[108px] px-12">
  <div class="flex lg:items-center justify-between gap-5 flex-col lg:flex-row">
    <div class="flex items-center gap-2 text-interface-50">
      <BreadcrumbRoute
        isFirstRoute={true}
        route="/new/learn/{slug}"
        text={slug}
      />

      <BreadcrumbRoute
        route="/new/learn/{slug}/overview?module={$moduleName}"
        text={$moduleName}
      />
    </div>

    <div
    class="
      hidden xl:flex
      lg:absolute lg:top-[26px] lg:left-1/2 lg:-translate-x-1/2
      2xl:left-[calc(50%-26px)]
      items-center gap-2 2xl:gap-6 max-lg:mx-auto
    "
  >
    <p class="font-bold xl:text-sm 2xl:text-base">{$moduleName}</p>
    <ProgressBar
      isVertical={false}
      width="336px"
      height="16px"
      borderRadius="24px"
      containerBg="#111827"
      value={completed}
      max={total}
      labelSize="12px"
      containerClass="max-xl:!gap-6 2xl:!gap-6 !gap-2"
      progressClass="xl:!w-[150px] xl:!h-[10px] 2xl:!h-[16px] 2xl:!w-[336px]"
    />
  </div>
  </div>

  <div
    class="flex flex-col items-center justify-center gap-10 mx-auto max-2xl:mt-5"
  >
    <h1 class="font-bold text-4xl capitalize">{$moduleName}</h1>

    {#if isDataFetched}
      <div class="relative w-full h-[696px]">
        <ExamModule {isOpenSection} on:sectionClicked={handleSectionClick} {SECTIONS_DATA} />
        <SectionDetails {isOpenSection} {handleCloseSection} {TERMS_LIST} />
      </div>
    {:else}
      <div class="relative w-full h-[696px]">
        <section class="absolute inset-0 left-1/2 grid grid-cols-1 gap-0 rounded-3xl bg-[#3B82F6]/10 p-8 w-full lg:w-[800px] xl:w-[1000px] h-full overflow-auto hide-scrollbar duration-700 transition-transform -translate-x-1/2">
          <div class="grid grid-cols-3 gap-8 h-full">
            <!-- Empty first row -->
            <div class="col-span-3 h-12"></div>

            {#each Array(24) as _, index}
              <div
                class="placeholder animate-pulse h-12 w-3/4 bg-gray-300 rounded-xl mx-auto"
                style="grid-column: span 1;"
              ></div>
            {/each}
          </div>
        </section>
      </div>
    {/if}

    <Button
      variant="primary-blue"
      className="w-[538px] h-[44px]"
      on:click={handleResume}
    >
      Resume
    </Button>
  </div>
</div>
