<script lang="ts">
  import ArrowRight from "../assets/icons/route-arrow.svg";
  import ReturnIcon from "../assets/icons/return-icon.svg";

  export let route = "";
  export let text: string | null = "";
  export let isFirstRoute = false;
</script>

<figure class="shrink-0">
  <img src={isFirstRoute ? ReturnIcon : ArrowRight} alt="arrow" class = "pt-4"/>
</figure>
<a
  href={route}
  class="text-interface-50 font-medium text-xs leading-[20px] duration-300 hover:underline text-nowrap pt-4"
>
  {text}
</a>
