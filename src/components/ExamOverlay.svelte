<script lang="ts">
  import InfoIcon from "../assets/icons/info-icon.svg";
  import CloseIcon from "../assets/icons/close.svg";
  import Button from "./Button.svelte";
  import Modal from "./Modal.svelte";

  interface Exam {
    id?: string;
    icon: string;
    name: string;
    length: number;
    lastUpdated: Date;
    description: string;
    modules: {
      id: string;
      name: string;
      description: string;
      sections: number;
      questions: number;
      completeWeeksTime: number;
    }[];
  }

  export let exam: Exam;
  export let open: boolean = false;
  export let close: () => void = () => (open = false);
  export let purchase: () => void;
  export let isOwned: boolean = false;
</script>

<Modal {open} onClose={close}>
  <div
    class="relative rounded-[32px] bg-[#1A2841] flex flex-col max-w-[1116px] max-h-[780px] p-6 overflow-y-scroll hide-scrollbar"
  >
    <button class="absolute top-[31px] right-[31px]" on:click={close}
      ><img src={CloseIcon} alt="close" /></button
    >

    <figure
      class="w-full min-h-[320px] flex items-center justify-center text-9xl"
    >
      {exam.icon}
    </figure>

    <div class="flex items-start justify-between gap-5 mb-6">
      <div class="flex flex-col gap-2 leading-[20px]">
        <h2 class="font-semibold text-2xl">{exam.name}</h2>
        <p class="text-xs italic font-light">
          Last updated {new Date(exam.lastUpdated).toLocaleDateString()}
        </p>
      </div>
      <p class="font-semibold text-[16px] shrink-0">
        {exam.length} Sections
      </p>
    </div>

    <p class="mb-[40px]">{exam.description}</p>

    <div class="flex flex-col gap-[40px] items-center">
      <h3 class="font-bold text-2xl leading-[20px] text-interface-50">
        Modules
      </h3>

      <ul class="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-3">
        {#each exam.modules as module}
          <li
            class="w-[340px] rounded-3xl bg-[rgba(59,130,246,0.1)] px-4 py-6 flex flex-col items-center gap-6 text-center"
          >
            <h4 class="font-semibold text-2xl">{module.name}</h4>

            <p class="text-xs">{module.description}</p>

            <div class="w-full h-[1px] bg-[rgba(86,192,240,0.25)] shrink-0" />

            <div class="flex flex-col gap-2 justify-center items-center">
              <p class="text-white">
                Sections: <span class="text-secondary-500"
                  >{module.sections}</span
                >
              </p>
              <p class="text-white">
                Questions: <span class="text-secondary-500"
                  >{module.questions}</span
                >
              </p>
              <p class="text-white flex items-center gap-1">
                Time To Complete: <span
                  class="text-secondary-500 flex items-center gap-1"
                >
                  {module.completeWeeksTime} weeks
                  <img src={InfoIcon} alt="info" />
                </span>
              </p>
            </div>
          </li>
        {/each}
      </ul>
    </div>
  </div>

  <div class="flex items-center justify-center gap-10 flex-wrap">
    <Button
      variant="secondary-blue"
      className="w-[538px] !bg-[#111827] hover:!bg-primary-500"
      handleClick={close}>Back</Button
    >
    <Button
      variant={isOwned ? "primary-blue" : "primary-green"}
      className="w-[538px] "
      handleClick={purchase}
    >
      {isOwned ? "View" : "Purchase"}
    </Button>
  </div>
</Modal>
