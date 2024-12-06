<script>
  import { Modal } from '@skeletonlabs/skeleton';
  import Button from "../../../../../components/Button.svelte"; // Your custom Button component

  let isModalOpen = true;

  function handleConfirm() {
    // Handle the confirm action here
    isModalOpen = false; // Close the modal after action
  }

  function handleCancel() {
    // Handle the cancel action here
    isModalOpen = false; // Close the modal after action
  }
</script>

<!-- Modal Component -->
<Modal bind:open={isModalOpen} closeOnEsc={false} closeOnOutsideClick={false}>
  <!-- Header Slot -->
  <h3 slot="header">Your Attention is Required</h3>

  <!-- Body Slot -->
  <div slot="body">
    <p>Please read the following information carefully before proceeding.</p>
  </div>

  <!-- Footer Slot -->
  <div slot="footer">
    <Button
      variant="primary-blue"
      on:click={handleConfirm}
    >
      Confirm
    </Button>
    <Button
      variant="secondary-blue"
      on:click={handleCancel}
    >
      Cancel
    </Button>
  </div>
</Modal>
