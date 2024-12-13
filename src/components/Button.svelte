<script>
  import { createEventDispatcher } from 'svelte';
  export let type = "button";
  export let variant = "primary-blue";
  export let className = "";
  export let disabled = false;

  const dispatch = createEventDispatcher();

  export let handleClick = function handleClick(event) {
    dispatch('click', event); // Dispatch the click event to the parent
  }

  const classes = {
    "primary-blue": "primary-blue",
    "outline-blue": "outline-blue",
    "secondary-blue": "secondary-blue",
    "primary-green": "primary-green",
    "outline-green": "outline-green",
    "secondary-green": "secondary-green",
    "primary-purple": "primary-purple",
    "outline-purple": "outline-purple",
    "secondary-purple": "secondary-purple",
    "primary-red": "primary-red",
    "outline-red": "outline-red",
  };
</script>

<button
  class={`button ${classes[variant]} ${className} disabled:opacity-60 disabled:cursor-not-allowed`}  
  on:click={handleClick}
  {type}
  {disabled}
>
  <slot></slot>
</button>
