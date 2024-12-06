<script>
    import { onMount, tick } from 'svelte';
  
    let sections = [
      { title: "Edge Functions", status: "completed" },
      { title: "Databse Replication", status: "completed" },
      { title: "Machine Learning", status: "completed"},
      { title: "S3 Basics", status: "locked"}    ];
  
    let renderSections = Array(sections.length).fill(false);
    let fadeClass = Array(sections.length).fill(''); // Track fade-in class for each section
    let renderConnectors = Array(sections.length - 1).fill(false); // Track visibility of connectors
  
    onMount(async () => {
      // Start rendering the first section with a 3-second delay
      setTimeout(async () => {
        for (let index = 0; index < sections.length; index++) {
          // Render the current section
          renderSections[index] = true;
          await tick(); // Ensure DOM update before applying animation
          fadeClass[index] = 'fade-in';
  
          // Wait for section fade-in to complete
          await new Promise(resolve => setTimeout(resolve, 500));
  
          // Render the connector to the right of the current section (if it exists)
          if (index < sections.length - 1) {
            renderConnectors[index] = true;
            await new Promise(resolve => setTimeout(resolve, 500)); // Adding delay between each connector's rendering
          }
        }
      }, 3000); // 3-second delay before rendering the first section
    });
  
    function buttonClass(status) {
      if (status === "completed") return "button secondary-green w-full !opacity-100 h-[44px] disabled:opacity-60 disabled:cursor-not-allowed";
      if (status === "active") return "button secondary-blue w-full !opacity-100 h-[44px] disabled:opacity-60 disabled:cursor-not-allowed";
      if (status === "locked") return "button secondary-purple w-full !opacity-100 h-[44px] disabled:opacity-60 disabled:cursor-not-allowed locked";
    }
  
    function isDisabled(status) {
      return status !== "active"; // Completed and locked sections are disabled
    }
  </script>
  
  <div class="horizontal-container">
        {#each sections as section, index}
            <div
            class="section-wrapper"
            style="padding-left: {index === 0 ? '15px' : '0'}; padding-right: {index === sections.length - 1 ? '15px' : '0'};"
            >
            {#if renderSections[index]}
                <button
                class={`${buttonClass(section.status)} ${fadeClass[index]}`}
                type="button"
                disabled={isDisabled(section.status)}
                >
                {section.title}
                </button>
            {/if}
        
            {#if index < sections.length - 1 && renderConnectors[index]}
                <div class="connector connector-grow"></div>
            {/if}
            </div>
    {/each}
  </div>
  
  <style>
    /* Horizontal container for sections */
    .horizontal-container {
      display: flex;
      align-items: center;
      overflow-x: auto; /* Allow horizontal scrolling if needed */
      white-space: nowrap;
      position: relative;
    }
  
    /* Section wrapper for buttons and connectors */
    .section-wrapper {
        display: flex;
        align-items: center; /* Keeps elements vertically centered */
        justify-content: flex-start; /* Ensure elements render left-to-right */
        position: relative; /* Maintains its relative position */
        min-height: 60px; /* Adjust based on the maximum height of the animated elements */
        overflow: visible; /* Allows the bounce effect to expand beyond the element bounds */
        }
  
    /* Connector styles (horizontal thin blue line between sections) */
    .connector {
      width: 0; /* Initial width of 0 to grow */
      height: 2px; /* Thin blue line */
      background-color: #3b82f6; /* Blue color */
    }
  
    /* Connector grow animation */
    .connector-grow {
      animation: growConnector 1s ease-out forwards; /* Animation for the connector to grow */
    }
  
    /* Enhanced Fade-in animation for buttons */
    .fade-in {
      animation: fadeInEffect 2.5s ease-out forwards !important;
    }
  
    @keyframes fadeInEffect {
      0% {
        opacity: 0;
        transform: scale(0.9); /* Slightly smaller for a pop effect */
      }
      50% {
        opacity: 0.5;
        transform: scale(1.05); /* A slight enlargement for dynamic appearance */
      }
      100% {
        opacity: 1;
        transform: scale(1); /* Return to normal scale */
      }
    }
  
    @keyframes growConnector {
      0% {
        width: 0;
      }
      100% {
        width: 40px; /* Full length of the connector */
      }
    }
    .locked {
    position: relative; /* Enable positioning for the lock overlay */
    opacity: 0.5; /* Reduce opacity to indicate the element is inactive */
    pointer-events: none; /* Prevent interaction with the element */
    }

    /* Lock icon overlay */
    .locked::after {
    content: "\1F512"; /* Unicode for a lock symbol */
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); /* Center the lock icon */
    font-size: 24px; /* Adjust size as needed */
    color: #333; /* Lock icon color */
    z-index: 1; /* Ensure it appears above the element */
    }
  </style>
  