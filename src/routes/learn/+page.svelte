<script>
    import { onMount } from "svelte";
    import { Avatar, ProgressBar } from "@skeletonlabs/skeleton";
    import ReturnIcon from "../../assets/icons/return-icon.svg";
    import SingleCard from "./SingleCard.svelte";
  
    let isHovered = false;
    $: isHovered = false;
  
    // Define locked variables
    let understand_locked = true;
    let apply_locked = true;
  
    // Progress data for each section
    let learnProgress = { solvedTerms: 0, totalTerms: 0 };
    let understandProgress = { solvedTerms: 0, totalTerms: 0 };
    let applyProgress = { solvedTerms: 0, totalTerms: 0 };
  
    const handleGoBack = () => {
      window.location.href = `/new/my-cards`;
    };
  
    const DUMMY_PROGRESS = {
      learn: {
        solvedTerms: 0,
        totalTerms: 40,
      },
      understand: {
        solvedTerms: 0,
        totalTerms: 44,
      },
      apply: {
        solvedTerms: 0,
        totalTerms: 44,
      },
    };
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
      <!-- Static title for the page -->
      <h1 class="font-bold text-4xl mb-[116px]">AWS Solutions Architect Associate</h1>
  
      <ul class="grid sm:grid-cols-2 lg:grid-cols-3 gap-[60px]">
        <!-- Learn Module Card -->
        <div
          class="duration-300 transition-transform cursor-default group {isHovered &&
          DUMMY_PROGRESS.learn.solvedTerms === DUMMY_PROGRESS.learn.totalTerms
            ? 'translate-y-[47px]'
            : 'translate-y-0'}"
          on:mouseenter={() =>
            !(
              DUMMY_PROGRESS.learn.solvedTerms === DUMMY_PROGRESS.learn.totalTerms
            )
              ? (isHovered = true)
              : null}
          on:mouseleave={() =>
            !(
              DUMMY_PROGRESS.learn.solvedTerms === DUMMY_PROGRESS.learn.totalTerms
            )
              ? (isHovered = false)
              : null}
          role="button"
          tabindex="0"
        >
          <SingleCard
            title="Diagnostic"
            description="Answer scenario-based practice questions designed to uncover your learning needs."
            progressValue={DUMMY_PROGRESS.learn.solvedTerms}
            progressMax={DUMMY_PROGRESS.learn.totalTerms}
            standardLink="/apply-multiple"
            smartLink="/learn-open"
            viewLink="/apply-multiple" 
          />
        </div>
  
        <!-- Understand Module Card -->
        <div
          class="duration-300 transition-transform cursor-default group {isHovered &&
          (DUMMY_PROGRESS.understand.solvedTerms ===
            DUMMY_PROGRESS.understand.totalTerms ||
            understand_locked)
            ? 'translate-y-[47px]'
            : 'translate-y-0'}"
          on:mouseenter={() =>
            !(
              DUMMY_PROGRESS.understand.solvedTerms ===
              DUMMY_PROGRESS.understand.totalTerms
            ) && !understand_locked
              ? (isHovered = true)
              : null}
          on:mouseleave={() =>
            !(
              DUMMY_PROGRESS.understand.solvedTerms ===
              DUMMY_PROGRESS.understand.totalTerms
            ) && !understand_locked
              ? (isHovered = false)
              : null}
          role="button"
          tabindex="0"
        >
          <SingleCard
            title="Concept Explorer"
            description="Review a tailored list of concepts by answering questions paired with in-depth feedback."
            progressValue={DUMMY_PROGRESS.understand.solvedTerms}
            progressMax={DUMMY_PROGRESS.understand.totalTerms}
            standardLink="/understand-multiple"
            smartLink="/learn-open"
            isLocked={understand_locked}
            viewLink="/understand-multiple" 
          />
        </div>
  
        <div
          class="duration-300 transition-transform cursor-default group {isHovered &&
          (DUMMY_PROGRESS.apply.solvedTerms === DUMMY_PROGRESS.apply.totalTerms ||
            apply_locked)
            ? 'translate-y-[47px]'
            : 'translate-y-0'}"
          on:mouseenter={() =>
            !(
              DUMMY_PROGRESS.apply.solvedTerms === DUMMY_PROGRESS.apply.totalTerms
            ) && !apply_locked
              ? (isHovered = true)
              : null}
          on:mouseleave={() =>
            !(
              DUMMY_PROGRESS.apply.solvedTerms === DUMMY_PROGRESS.apply.totalTerms
            ) && !apply_locked
              ? (isHovered = false)
              : null}
          role="button"
          tabindex="0"
        >
          <SingleCard
            title="Term Mastery"
            description="Strengthen your understanding of key terms that are customized to your learning path."
            progressValue={DUMMY_PROGRESS.apply.solvedTerms}
            progressMax={DUMMY_PROGRESS.apply.totalTerms}
            standardLink="/learn-multiple"
            smartLink="/apply-open"
            isLocked={apply_locked}
            viewLink="/learn-multiple" 
          />
        </div>
      </ul>
    </div>
  </div>
  