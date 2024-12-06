<script>
  import ArrowLeft from "../../../../../assets/icons/arrow-left.svg";
  import Terms from "../../../../../components/Terms.svelte";

  export let isOpenSection = false;
  export let handleCloseSection = () => {
    isOpenSection = false;
  };
  export let TERMS_LIST = [
    { id: 1, isCompleted: true, title:"concept" },
    { id: 2, isCompleted: true, title:"concept" },
    { id: 3, isCompleted: true, title:"concept" },
    { id: 4, isCompleted: true, title:"concept" },
    { id: 5, isCompleted: true, title:"concept" },
    { id: 6, isCompleted: true, title:"concept" },
    { id: 7, isCompleted: true, title:"concept" },
    { id: 8, isCompleted: false, title:"concept" },
    { id: 9, isCompleted: false, title:"concept" },
    { id: 10, isCompleted: false, title:"concept" },
    { id: 11, isCompleted: false, title:"concept" },
    { id: 12, isCompleted: false, title:"concept" },
    { id: 13, isCompleted: false, title:"concept" },
    { id: 14, isCompleted: false, title:"concept" },
  ];
</script>

<div
  class="absolute inset-0 left-1/2 rounded-3xl bg-[#3B82F6]/10 p-8 w-full lg:w-[900px] xl:w-[1116px] max-h-[696px] overflow-y-scroll hide-scrollbar duration-700 transition-transform {isOpenSection
    ? '-translate-x-1/2'
    : 'translate-x-[190%]'}"
>
  <button
    class="flex items-center gap-[19px] text-interface-50 mb-[42px]"
    on:click={handleCloseSection}
  >
    <figure><img src={ArrowLeft} alt="back" /></figure>
    <span class="font-bold text-base">Section</span>
  </button>

  <Terms {TERMS_LIST} />
</div>
