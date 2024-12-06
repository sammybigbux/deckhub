<script lang="ts">
  import { getModalStore } from '@skeletonlabs/skeleton';
  import type { ModalSettings } from '@skeletonlabs/skeleton';
  import ReportModal from './ReportModal.svelte';

  // Sample report data
  let report_info = {
    strong_areas: ['Area 1', 'Area 2'],
    weak_areas: ['Area 3', 'Area 4'],
    'time saved': '2 hours',
  };

  const modalStore = getModalStore();

  const modal: ModalSettings = {
    type: 'component',
    component: {
      ref: ReportModal,
      props: {
        strongAreas: report_info.strong_areas,
        weakAreas: report_info.weak_areas,
        timeSaved: report_info['time saved'],
        onClose: () => modalStore.close(),
      },
    },
    modalClasses: '!w-screen !h-screen !flex !items-center !justify-center !p-0', // Full height and centered content
    backdropClasses: '!w-screen !h-screen !p-0 !m-0 fixed top-0 left-0 flex items-center justify-center', // Fullscreen fixed container
  };



  modalStore.trigger(modal);
</script>

<main>
  <h1>Report Modal Test</h1>
  <p>The modal will appear immediately upon loading this page.</p>
</main>
