<script>
  import ProgressBar from "../../../../../components/ProgressBar.svelte";
  import Section from "./Section.svelte";
  import SectionsContainer from "./SectionsContainer.svelte";
  import LockProgressImage from "../../../../../assets/learn-overview/lock-progress.png";
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  export let isOpenSection = false;

  const handleOpenSection = (subSection) => {
    isOpenSection = !isOpenSection;
    dispatch('sectionClicked', { title: subSection.title });
  };


  export let SECTIONS_DATA = [
    {
      title: "Section",
      description: "Build your foundation on concepts essential to proceeding.",
      isLocked: false,
      progressValue: 2,
      progressMax: 8,
      sections: [
        { title: "Section", isCompleted: true },
        { title: "Section", isCompleted: true },
        { title: "Section", isActive: true },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section", isEndSection: true },
      ],
    },
    {
      title: "Section",
      description:
        "Take your knowledge of concepts to the next level, achieving a well-rounded understanding.",
      isLocked: true,
      progressValue: 0,
      progressMax: 8,
      sections: [
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section", isEndSection: true },
      ],
    },
    {
      title: "Section",
      description:
        "Master special topics by applying the knowledge gained from previous sections.",
      isLocked: true,
      sections: [
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section" },
        { title: "Section", isEndSection: true },
      ],
    },
  ];
</script>

<div
  class="absolute inset-0 left-1/2 grid grid-cols-5 gap-0 rounded-3xl bg-[#3B82F6]/10 p-8 w-full lg:w-[900px] xl:w-[1116px] h-full overflow-auto hide-scrollbar duration-700 transition-transform {!isOpenSection
    ? '-translate-x-1/2'
    : '-translate-x-[190%]'}"
>
  {#each SECTIONS_DATA as section, index}
    <div class="flex flex-col items-center gap-4">
      <div class="flex flex-col items-center gap-4 text-white min-h-[81px]">
        <h3 class="font-bold leading-[20px]">{section.title}</h3>
        <p class="text-xs leading-[15px]">{section.description}</p>
      </div>
      <SectionsContainer isLocked={section.isLocked}>
        {#each section.sections as subSection}
          <Section
            title={subSection.title}
            isCompleted={subSection?.isCompleted}
            isActive={subSection?.isActive}
            isEndSection={subSection.isEndSection}
            handleSectionClick={() => handleOpenSection(subSection)}
          />
        {/each}
      </SectionsContainer>
    </div>

    {#if index < SECTIONS_DATA.length - 1}
      <div class="flex flex-col items-center gap-4 mt-[17rem]">
        <figure class="w-full">
          <img src={LockProgressImage} alt="locked" class="w-full" />
        </figure>
        <div class="px-[19px] w-full">
          <ProgressBar
            value={section.progressValue}
            max={section.progressMax}
            borderRadius="8px"
            height="8px"
            labelSize="12px"
            isActiveLabel={true}
          />
        </div>
      </div>
    {/if}
  {/each}
</div>
