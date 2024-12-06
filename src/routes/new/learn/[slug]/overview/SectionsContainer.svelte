<script>
  export let isLocked = false;
</script>

<div
  class="rounded-3xl w-full border p-6 flex flex-col items-center"
  style="border-color: {!isLocked ? '#2563EB' : 'rgba(86, 192, 240, 0.25)'};"
>
  <slot></slot>
</div>
