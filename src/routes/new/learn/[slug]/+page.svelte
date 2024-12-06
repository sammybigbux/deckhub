<script>
  import { onMount } from "svelte";
  import { Avatar, ProgressBar } from "@skeletonlabs/skeleton";
  import { page } from "$app/stores";
  import ReturnIcon from "../../../../assets/icons/return-icon.svg";
  import SingleCard from "./SingleCard.svelte";
  import { userId } from '../../../../lib/firebase';
  import { get } from 'svelte/store';

  const base_url = import.meta.env.VITE_BASE_URL;

  let slug = $page.params.slug;
  $: slug = $page.params.slug;
  let isHovered = false;
  $: isHovered = false;

  // Define locked variables
  let understand_locked = true;
  let learn_locked = true;

  // Progress data for each section
  let learnProgress = { "sections_completed": 0, "sections_total": 1 };
  let understandProgress = { "sections_completed": 0, "sections_total": 1 };
  let applyProgress = { "sections_completed": 0, "sections_total": 1 };

  const handleGoBack = () => {
    window.location.href = `/new/my-cards`;
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

  // Function to retrieve terms data from different endpoints
  async function retrieveSectionData() {
      // Extract the exam name from the URL
      const userID = await getUserID();
      const url = window.location.href;
      const examName = decodeURIComponent(url.split("/").pop());

      // Prepare the request payload
      const payload = {
          user_id: userID,
          exam: examName
      };

      try {
          // Send POST request to /get_user_progress
          const response = await fetch(`${base_url}/get_user_progress`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
          });

          if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
          }

          // Parse the response JSON
          const data = await response.json();
          console.log("Data retrieved from get_user_progress:", data);

          // Set progress variables based on the returned dictionary
          const progress = data.progress || {}; // Default to empty object if no data is returned

          console.log("Progress variable is:", { progress });

          // Assign progress values to appropriate variables
          applyProgress = progress.apply
          understandProgress = progress.understand
          learnProgress = progress.learn

          console.log("Progress retrieved and variables set:", { applyProgress, understandProgress, learnProgress });

          // Check progress to unlock next section
          if (applyProgress.sections_completed === applyProgress.sections_total) {
              understand_locked = false; // Unlock the Concept Explorer section
          }
          if (understandProgress.sections_completed === understandProgress.sections_total) {
              learn_locked = false; // Unlock the Terms section
          }

          console.log("Progress retrieved and variables set:", { applyProgress, understandProgress, learnProgress });
      } catch (error) {
          console.error("Error retrieving user progress:", error);
      }
  }


  onMount(async () => {
    await retrieveSectionData(); // Initial fetch
    setTimeout(async () => {
      await retrieveSectionData(); // Fetch again after 500ms
    }, 500);
  });
</script>

<div class="text-interface-50 pt-[32px] pb-[270px] px-12">
  <button class="flex items-center gap-[7px] mb-16" on:click={handleGoBack}>
    <figure><img src={ReturnIcon} alt="back" /></figure>
    <span
      class="text-interface-50 text-xs leading-[20px] duration-300 hover:underline"
      >Back</span
    >
  </button>

  <div class="flex flex-col items-center justify-center">
    <h1 class="font-bold text-4xl mb-[116px]">{slug}</h1>

    <ul class="grid sm:grid-cols-2 lg:grid-cols-3 gap-[60px]">
      <!-- Apply Module Card -->
      <div
        class="duration-300 transition-transform cursor-default group {isHovered &&
        applyProgress.sections_completed === applyProgress.sections_total
          ? 'translate-y-[47px]'
          : 'translate-y-0'}"
        on:mouseenter={() =>
          !(
            applyProgress.sections_completed === applyProgress.sections_total
          )
            ? (isHovered = true)
            : null}
        on:mouseleave={() =>
          !(
            applyProgress.sections_completed === applyProgress.sections_total
          )
            ? (isHovered = false)
            : null}
        role="button"
        tabindex="0"
      >
        <SingleCard
          title="Diagnostic"
          description="Answer scenario-based practice questions designed to uncover your learning needs."
          progressValue={applyProgress.sections_completed}
          progressMax={applyProgress.sections_total}
          standardLink={`/new/learn/${slug}/overview?module=Diagnostic`}
          smartLink={`/new/learn/${slug}/overview?module=Diagnostic`}
          viewLink={`/new/learn/${slug}/overview?module=Diagnostic`}
        />
      </div>

      <!-- Understand Module Card -->
      <div
        class="duration-300 transition-transform cursor-default group {isHovered &&
        (understandProgress.sections_completed === understandProgress.sections_total ||
          understand_locked)
          ? 'translate-y-[47px]'
          : 'translate-y-0'}"
        on:mouseenter={() =>
          !(
            understandProgress.sections_completed ===
            understandProgress.sections_total
          ) && !understand_locked
            ? (isHovered = true)
            : null}
        on:mouseleave={() =>
          !(
            understandProgress.sections_completed ===
            understandProgress.sections_total
          ) && !understand_locked
            ? (isHovered = false)
            : null}
        role="button"
        tabindex="0"
      >
        <SingleCard
          title="Concept Explorer"
          description="Review a tailored list of concepts by answering questions paired with in-depth feedback."
          progressValue={understandProgress.sections_completed}
          progressMax={understandProgress.sections_total}
          standardLink={`/new/learn/${slug}/overview?module=Concept Explorer`}
          smartLink={`/new/learn/${slug}/overview?module=Concept Explorer`}
          isLocked={understand_locked}
          viewLink={`/new/learn/${slug}/overview?module=Concept Explorer`}
        />
      </div>

      <!-- Learn Module Card -->
      <div
        class="duration-300 transition-transform cursor-default group {isHovered &&
        (learnProgress.sections_completed === learnProgress.sections_total ||
          learn_locked)
          ? 'translate-y-[47px]'
          : 'translate-y-0'}"
        on:mouseenter={() =>
          !(
            learnProgress.sections_completed === learnProgress.sections_total
          ) && !learn_locked
            ? (isHovered = true)
            : null}
        on:mouseleave={() =>
          !(
            learnProgress.sections_completed === learnProgress.sections_total
          ) && !learn_locked
            ? (isHovered = false)
            : null}
        role="button"
        tabindex="0"
      >
        <SingleCard
          title="Term Mastery"
          description="Strengthen your understanding of key terms that are customized to your learning path."
          progressValue={learnProgress.sections_completed}
          progressMax={learnProgress.sections_total}
          standardLink="/new/learn/{slug}/open"
          smartLink="/new/learn/{slug}/open"
          isLocked={learn_locked}
          viewLink={`/new/learn/${slug}/overview?module=Term Mastery`}
        />
      </div>
    </ul>
  </div>
</div>
