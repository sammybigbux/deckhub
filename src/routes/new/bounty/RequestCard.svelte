<script lang="ts">
  export let request;
  export let user;
  export let toggleUpvote: (requestId: string) => void;
  import { goto } from '$app/navigation';

  // const isUpvoted = request.subscribers.includes(user?.uid);

  import Upvote from "../../../assets/icons/upvote.svg";
  import Button from "../../../components/Button.svelte";

  function handleClick() { // update input later to make the navigation variable
    goto('/new/learn/AWS Solutions Architect');
  }
</script>

<li class="w-full">
  <div
    class={`rounded-[32px] p-6 flex flex-col gap-8 w-full 3xl:max-w-[392px] max-h-[160px] ${
      request.isUnderReview
        ? "bg-[#EAB308]/10"
        : request.solved
          ? "bg-[rgba(15,186,129,0.1)] group"
          : "bg-[rgba(59,130,246,0.1)]"
    }`}
  >
    <div
      class="flex flex-col gap-4 text-interface-50 font-semibold text-base max-h-[56px]"
    >
      <span>{request.text}</span>
      <span class="font-normal"
        >{new Date(request.timestamp).toLocaleDateString()}</span
      >
    </div>

    <div class="flex items-center justify-between gap-5 relative">
      <button
        class="flex items-center gap-4"
        on:click={() => toggleUpvote(request.id)}
      >
        <figure class="w-[24px] aspect-square">
          <img src={Upvote} alt="arrow" />
        </figure>
        <span class="text-primary-600 font-semibold text-base leading-[20px]"
          >{request.upvotes}</span
        >
      </button>

      {#if request.isUnderReview}
        <div class="font-semibold text-base text-[#EAB308] leading-[20px]">
          Under Review
        </div>
      {:else if request.solved}
        <div class="font-semibold text-base text-secondary-700 leading-[20px]">
          Fulfilled
        </div>
        <Button
          variant="primary-green"
          className="absolute -bottom-1 -right-1 w-[200px] duration-300 opacity-0 group-hover:opacity-100"
          handleClick={handleClick}
          >View Fix</Button
        >
      {:else}
        <div class="font-semibold text-base text-interface-50 leading-[20px]">
          Unfulfilled
        </div>
      {/if}
    </div>
  </div>
</li>
