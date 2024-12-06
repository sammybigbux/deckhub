<script lang="ts">
  import { page } from "$app/stores";
  import BreadcrumbRoute from "../BreadcrumbRoute.svelte";
  import ProgressBar from "../ProgressBar.svelte";
  import PlanTabs from "./PlanTabs.svelte";

  export let sectionName: string | null = "";
  export let moduleName: string | null = "";
  export let activePlan: "CHOICE" | "FREE" = "CHOICE";
  export let handleActivePlanChange = (event: CustomEvent) => {};
  export let solvedTerms = 0;
  export let totalTerms = 0;
  export let specificity = "";

  $: slug = $page.params.slug;
</script>

<div class="flex items-start justify-between gap-5 flex-col">
  <div class="flex items-center gap-2 text-interface-50">
    <BreadcrumbRoute
      isFirstRoute={true}
      route="/new/learn/{slug}"
      text={slug}
    />
    <BreadcrumbRoute
      route="/new/learn/{slug}/overview?module={moduleName}"
      text={moduleName}
    />
    <BreadcrumbRoute
      route="/new/learn/{slug}/open?module={moduleName}&section={sectionName}"
      text={sectionName}
    />
  </div>

  <div
    class="xl:absolute xl:top-[26px] 2xl:left-[calc(50%-26px)] xl:left-1/2 xl:-translate-x-1/2 flex lg:items-center max-xl:gap-7 gap-2 flex-col 2xl:gap-7 lg:mx-auto"
  >
    <div class="flex items-center gap-6">
      <p class="font-bold">{specificity ? specificity.charAt(0).toUpperCase() + specificity.slice(1).toLowerCase() : moduleName}</p>
      <ProgressBar
        isVertical={false}
        width="336px"
        height="16px"
        borderRadius="24px"
        containerBg="#111827"
        value={solvedTerms}
        max={totalTerms}
        labelSize="12px"
        labelWeight="500"
        labelName="questions"
        containerClass="max-xl:!gap-7 2xl:!gap-7 !gap-2"
        progressClass="max-lg:!w-[150px] xl:!w-[150px] max-lg:!h-[10px] xl:!h-[10px] 2xl:!h-[16px] 2xl:!w-[336px]"
      />
    </div>

  </div>
</div>
