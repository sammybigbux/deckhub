<script lang="ts">
  export let placeholder: string = 'Search';
  export let value: string = '';
  export let onInput: (e: Event) => void = () => {};

  import SearchIcon from '../assets/icons/search.svg';
</script>

<div class="relative w-full">
  <input
    type="text"
    class="rounded-[30px] bg-[rgba(86,192,240,0.25)] border-none w-full h-12 pl-[68px] pr-6 py-3 text-base leading-[20px] text-interface-50 placeholder-interface-50"
    bind:value
    placeholder={placeholder}
    on:input={onInput}
  />
  <figure class="absolute top-1/2 left-6 transform -translate-y-1/2">
    <img src={SearchIcon} alt="search" />
  </figure>
</div>
