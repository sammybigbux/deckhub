<script lang="ts">
  import { page } from "$app/stores";
  import ChatHeader from "../../../../../components/Chat/ChatHeader.svelte";
  import ChooseDifficulty from "../../../../../components/Chat/ChooseDifficulty.svelte";
  import SendButtonIcon from "../../../../../assets/icons/send-button.svg";
  import Button from "../../../../../components/Button.svelte";
  import Terms from "../../../../../components/Terms.svelte";
  import type { SvelteComponent } from "svelte";
  import Question from "../../../../../components/Chat/Question.svelte";
  import Correct from "../../../../../components/Chat/Correct.svelte";
  import CorrectExplanation from "../../../../../components/Chat/CorrectExplanation.svelte";
  import SingleTerm from "../../../../../components/Chat/SingleTerm.svelte";
  import FreeQuestion from "../../../../../components/Chat/FreeQuestion.svelte";
  import OutOfFundModal from "../../../../../components/Chat/OutOfFundModal.svelte";
  import AvatarBotImg from "../../../../../assets/icons/avatar-bot.svg";
  import AvatarPersonImg from "../../../../../assets/icons/avatar-person.svg";
  import AvatarBotFreeImg from "../../../../../assets/icons/avatar-bot-free.svg";
  import { Avatar } from "@skeletonlabs/skeleton";
  import { slide } from "svelte/transition";
  import { get } from 'svelte/store';
  import { userId } from '../../../../../lib/firebase';
  import { solvedTerms, totalTerms, totalCompleted, totalIncorrect, total_questions, sectionName } from "../../../../../stores/random_store";
  import { onMount, onDestroy } from 'svelte';
  import { getModalStore } from '@skeletonlabs/skeleton';
  import type { ModalSettings } from '@skeletonlabs/skeleton';
  import ReportModal from '../../../../../components/Chat/ReportModal.svelte';


  const base_url = import.meta.env.VITE_BASE_URL;
  let time_left_estimated = false;

  let chatEle: HTMLDivElement;
  let moduleName: string | null = "";
  let activePlan: "CHOICE" | "FREE" = "CHOICE";
  let activeDifficulty: "EASY" | "NORMAL" | "HARD" = "EASY";
  let remainingFreeQuestions = 2;
  let newMessage = "";
  let cleanupEnvTriggered = false; // ensure that cleanup is only called once
  let beforeUnloadTriggered = false;
  let specificity = "Foundational";
  let userOwnership = false; // whether or not the user owns this module
  const moduleLevels = {
    "Diagnostic": "apply",
    "Concept Explorer": "understand",
    "Term Mastery": "learn"
  };

  let firstQuestion = true;
  let currentTerm = "";
  let current_related_terms = {"term1": {"definition": "", "connection": ""}, "term2": {"definition": "", "connection": ""}, "term3": {"definition": "", "connection": ""}}; // attributes are "explanation" and "elaborate"
  let correct_response_data = {"explanation": "", "elaborate": ""}; // attributes are "explanation" and "elaborate"
  let incorrect_response_data = {"1": {"explanation": "", "elaborate": ""}, "2": {"explanation": "", "elaborate": ""}, "3": {"explanation": "", "elaborate": ""}}; //attributes are "text of incorrect answer": {"explanation", "elaborate"}

  type ConversationItem = {
    id: number;
    sender: "bot" | "person";
    message?: string;
    type: "text" | "component";
    component?: typeof SvelteComponent;
    props?: Record<string, any>;
  };

  let conversation: ConversationItem[] = [
    {
      id: 0,
      sender: "bot",
      message: `Hi! This is your <strong>AI Coach</strong> for the <strong>AWS SAA-03 Exam</strong>! The goal of this section is to help you recall terms and definitions for the exam through multiple choice. Let's start with a question.`,
      type: "text",
    },
  ];

  let certification;
  const modalStore = getModalStore();

  $: {
    const searchParams = new URLSearchParams($page.url.search);
    moduleName = searchParams.get("module");
    const parts = $page.url.pathname.split('/');
    certification = decodeURIComponent(parts[3]);
    if ($solvedTerms >= 20) {
      triggerReportModal(modalStore);
    }
  }

  const searchParams = new URLSearchParams($page.url.search);
  sectionName.set(searchParams.get("section"));
  console.log('sectionName set to this in the beginning: ', $sectionName);

  console.log("Section name",$sectionName)
  console.log("Module name",moduleName)

  async function updateIncorrect() {
        totalIncorrect.update((n) => n + 1);
        const userID = await getUserID();  // Wait for userID to be populated
        const payload = {
            term: currentTerm,
            userID: userID  // Add userID to the payload
        };

        try {
            const response = await fetch(`${base_url}/update_incorrect`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                console.log(`${currentTerm} marked as incorrect!`);
                await retrieveTermsData();  // Ensure the data is refreshed after the update
            } else {
                console.error(`Failed to update status for ${currentTerm}. Status: ${response.status}`);
            }
        } catch (error) {
            console.error(`Error updating inccorrect for ${currentTerm}:`, error);
        }
    }

    async function updateProgress() {
        totalCompleted.update((n) => n + 1);
        const userID = await getUserID();  // Wait for userID to be populated
        const payload = {
            term: currentTerm,
            userID: userID  // Add userID to the payload
        };

        try {
            const response = await fetch(`${base_url}/update_progress`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                console.log(`${currentTerm} passed!`);
                await retrieveTermsData();  // Ensure the data is refreshed after the update
            } else {
                console.error(`Failed to update status for ${currentTerm}. Status: ${response.status}`);
            }
        } catch (error) {
            console.error(`Error updating status for ${currentTerm}:`, error);
        }
    }

  function handleOptionClick(
    chosenIndex: number,
    correctIndex: number,
    answer: string,
    relatedTerms: string[]
  ) {
      newMessage = answer;

      if (chosenIndex !== correctIndex) {
        console.log("User answer is incorrect")
        updateIncorrect();
      }
      if (moduleName === "Diagnostic") {
        updateProgress();
        generateNextQuestion();
      }
      else {
        if (chosenIndex === correctIndex) {
          updateProgress();
        }
        sendMessage({
        id: generateId(),
        sender: "bot",
        type: "component",
        component: Correct,
        props: {
          isCorrect: chosenIndex === correctIndex,
          handleExplainClick: () =>
            handleExplainClick(chosenIndex === correctIndex, chosenIndex, Object.keys(current_related_terms)),
          correct_response_explanation: correct_response_data.explanation,
          incorrect_response_explanation: incorrect_response_data[Object.keys(incorrect_response_data)[chosenIndex]].explanation
        },
      });
    }
  }

  function handleExplainClick(isCorrect, chosenIndex, relatedTerms) {
    sendMessage({
      id: generateId(),
      sender: "bot",
      type: "component",
      component: CorrectExplanation,
      props: {
        isCorrect,
        relatedTerms: Object.keys(current_related_terms),
        handleTermClick: (term) =>
          handleTermClick(
            term,
            relatedTerms.filter((ele) => ele !== term)
          ),
        correct_response_elaboration: correct_response_data.elaborate,
        incorrect_response_elaboration: incorrect_response_data[Object.keys(incorrect_response_data)[chosenIndex]].elaborate
      },
    });
  }

  async function getRTFromLookup(section, term, related_term) {
      const userID = await getUserID();
      try {
          const response = await fetch(`${base_url}//get_rt_from_lookup`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
                  // Include any authentication headers if required
              },
              body: JSON.stringify({
                  section: section,
                  term: term,
                  related_term: related_term,
                  userID: userID
              })
          });

          if (!response.ok) {
              throw new Error(`Server error: ${response.statusText} (status ${response.status})`);
          }

          const data = await response.json();
          return data;
      } catch (error) {
          console.error('Error in getRTFromLookup:', error);
          throw error;
      }
  }

  function handleTermClick(term: string) {
    console.log("Related terms message is ", current_related_terms[term]['definition']);
    const related_term_dict = current_related_terms[term];
    const restTerms = Object.keys(current_related_terms).slice(0,3).filter(ele => ele !== term);

    const related_related_terms = related_term_dict['lookups']
      .map(lookup => lookup.related_term)
      .filter(relatedTerm => !restTerms.includes(relatedTerm));

      sendMessage({
        id: generateId(),
        sender: "bot",
        type: "component",
        component: SingleTerm,
        props: {
          title: term,
          restTerms,
          concepts: related_related_terms,
          handleTermClick: (term) =>
            handleTermClick(
              term,
              restTerms.filter(ele => ele !== term),
            ),
          handleRTClick: (related_term) =>
            handleRelatedTermClick(related_term),
          message: related_term_dict['definition'] + " " + related_term_dict['connection'],
        },
      });
    }

    async function handleRelatedTermClick(related_term: string) {
      // Step 1: Find the lookup_dict for the related_term
      let lookup_dict = null;

      // Iterate through current_related_terms to find the lookup_dict
      for (const key in current_related_terms) {
        if (current_related_terms.hasOwnProperty(key)) {
          const lookups = current_related_terms[key]['lookups'];
          if (lookups) {
            const found_lookup = lookups.find(lookup => lookup['related_term'] === related_term);
            if (found_lookup) {
              lookup_dict = found_lookup;
              break; // Exit the loop once we've found the lookup_dict
            }
          }
        }
      }

      if (!lookup_dict) {
        console.error("Lookup dict not found for related term: ", related_term);
        return;
      }

      // Step 2: Fetch the data for the related_term
      try {
        const related_term_data = await getRTFromLookup(
          lookup_dict['section'],
          lookup_dict['term'],
          lookup_dict['related_term']
        );

        if (related_term_data && related_term_data[related_term]) {
          const related_term_dict = related_term_data[related_term];

          // Step 3: Add the fetched term to current_related_terms
          current_related_terms[related_term] = related_term_dict;

          // Step 4: Prepare variables for sendMessage
          const title = related_term;
          const restTerms = Object.keys(current_related_terms); // Keep restTerms the same
          const concepts = related_term_dict['lookups'].map(lookup => lookup['related_term']);

          const message = related_term_dict['definition'] + " " + related_term_dict['connection'];

          // Step 5: Render the component using sendMessage
          sendMessage({
            id: generateId(),
            sender: "bot",
            type: "component",
            component: SingleTerm,
            props: {
              title: title,
              restTerms: restTerms,
              concepts: concepts,
              handleTermClick: (term) =>
                handleTermClick(
                  term,
                  restTerms.filter(ele => ele !== term),
                ),
              handleRTClick: (related_term) =>
                handleRelatedTermClick(related_term),
              message: message,
            },
          });
        } else {
          console.error("Data for related term not found: ", related_term);
        }
      } catch (error) {
        console.error("Error fetching data for related term: ", related_term, error);
      }
    }



  function handleDifficultyChange(event: CustomEvent) {
    activeDifficulty = event.detail.difficulty;
  }

  function handleActivePlanChange(event: CustomEvent) {
    activePlan = event.detail.plan;
    resetConversation();
  }

  async function handleViewTerms() {
    const userIdValue = get(userId);
    if (!$sectionName) {
        console.error('No active section found');
        return;
    }

    try {
        const response = await fetch(`${base_url}/get_term_list?section=${$sectionName}&userId=${userIdValue}`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error('Failed to fetch term data');
        }

        // Set TERMS_LIST with the JSON response
        let TERMS_LIST = await response.json();
        console.log('Terms list:', TERMS_LIST);
        newMessage = "Show me the terms"
        sendMessage({
          id: generateId(),
          sender: "bot",
          type: "component",
          component: Terms,
          props: { TERMS_LIST, isChat: true, onStudyClick: (title) => generateNextQuestion(title) }
        });

    } catch (error) {
        console.error('Error fetching term data:', error);
    }
  }

  async function getUserID() {
        return new Promise((resolve, reject) => {
            const uid = get(userId);  // Get current value of userId
            if (uid) {
                resolve(uid);  // If userID is already set, return it
            } else {
                // Wait for userID to be populated
                const unsubscribe = userId.subscribe(value => {
                    if (value) {
                        resolve(value);
                        unsubscribe();  // Unsubscribe once the userID is populated
                    }
                });
            }
        });
    }

  async function generateNextQuestion(term) {
    firstQuestion = false;
    newMessage = "Give me a question";
    if (term) {
      console.log("Term: ", term);
      newMessage = "Give me the " + term.replace(/_/g, ' ');
    }
    const userID = await getUserID();  // Wait for userID to be populated
    const payload = {
            term: term, // in case we want the user to set the term
            userID: userID,  // Add userID to the payload
            section: $sectionName
        };
    try {
        const response = await fetch(`${base_url}/get_question`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)  // Send userID in the body
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (!data.related_terms) {
            data.related_terms = [];
        }
        console.log("You are trying to send this option in with the generate question payload:", data.option1);
        sendMessage({
          id: generateId(),
          sender: "bot",
          type: "component",
          component: Question,
          props: {
            options: [data.option1, data.option2, data.option3, data.option4],
            question: data.question,
            correctOption: parseInt(data.answer.slice(-1), 10) - 1,
            relatedTerms: Object.keys(data.related_terms),
            handleOptionClick,
            sectionName: data.section
          },
        });
        currentTerm = data.term;
        const url = new URL(window.location.href);

        // If the section changes with the new question
        if ($sectionName !== data.section) {
            // Update the 'section' parameter in the URL
            url.searchParams.set('section', data.section);

            // Assign the updated URL back to the browser
            window.history.pushState({}, '', url);
            sectionName.set(data.section);
            console.log('sectionName set from question data: ', $sectionName);
        }
        console.log("The url after setting the section:", url);
        current_related_terms = data.related_terms;

        // update params in url if necessary
        console.log("Upon generating the question, the correct_response_data is:", correct_response_data);
        correct_response_data = data.correct_response;
        incorrect_response_data = data.incorrect_response;
        console.log('Getting back the question data from retrieveQuestion():', data);
        console.log("Upon generating the question, the correct_response_data is:", correct_response_data);
      }
      catch (error) {
          console.error('Error updating section:', error);
      }
  }


  function handleSubmit() {
    if (newMessage.trim()) {
      sendMessage({
        id: generateId(),
        sender: "bot",
        message: "I don't understand your message.",
        type: "text",
      });
    }
  }

  function sendMessage(botResponse: ConversationItem) {
    if (newMessage.trim()) {
      conversation = [
        ...conversation,
        {
          id: generateId(),
          sender: "person",
          message: newMessage,
          type: "text",
        },
      ];
    }

    setTimeout(() => {
      conversation = [...conversation, botResponse];
      newMessage = "";
      scrollToBottom();
    }, 300);
  }

  function resetConversation() {
    conversation = [
      {
        id: 0,
        sender: "bot",
        message: `Hi! This is your <strong>AI Coach</strong> for the <strong>AWS SAA-03 Exam</strong>! The goal of this section is to help you recall terms and definitions for the exam through multiple choice. Are you ready to get started?`,
        type: "text",
      },
    ];
  }

  function scrollToBottom() {
    setTimeout(() => {
      chatEle?.scrollTo({ top: chatEle.scrollHeight, behavior: "smooth" });
    }, 300); // as the new message is added after 300ms
  }
  function generateId() {
    return Math.round(Math.random() * 1000);
  }

  async function triggerReportModal(modalStore) {
      try {
          const userID = await getUserID(); // Wait for userID to be populated
          const payload = { userID };

          // Make the API call to fetch report data
          const response = await fetch(`${base_url}/get_report_data`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(payload)
          });

          // Parse the response JSON
          if (!response.ok) {
              const error = await response.json();
              console.error('Error fetching report data:', error);
              return;
          }

          const { report_data: report_info } = await response.json();
          console.log('Report data:', report_info);

          // Configure and trigger the modal
          const modal = {
              type: 'component',
              component: {
                  ref: ReportModal,
                  props: {
                      weakHierarchy: report_info.weak,
                      strongHierarchy: report_info.strong,
                      correct_of_twenty: report_info.number_correct,
                      incorrect_of_twenty: report_info.number_incorrect,
                      timeSaved: "12 hours", // Example time saved, adjust if dynamic
                      onClose: () => modalStore.close(),
                  },
              },
              modalClasses: '!w-screen !h-screen !flex !items-center !justify-center !p-0', // Full height and centered content
              backdropClasses: '!w-screen !h-screen !p-0 !m-0 fixed top-0 left-0 flex items-center justify-center', // Fullscreen fixed container
          };

          modalStore.trigger(modal);
      } catch (error) {
          console.error('Error triggering report modal:', error);
      }
  }

  async function retrieveTermsData(): Promise<void> {
      try {
          const userID = await getUserID();  // Wait for userID to be populated
          const payload = { userID };

          const response = await fetch(`${base_url}/get_terms_data`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(payload)
          });
          
          const data = await response.json();
          if (data.solvedTerms >= 10) {
            await triggerReportModal(modalStore);
          }
          totalTerms.set(data.totalSpecificityTerms)  // Reactive updates
          solvedTerms.set(data.solvedTerms);  // Reactive updates
          // add condition to trigger ReportModal when 
          specificity = data.specificity;
          if (!time_left_estimated) { // setting baseline to estimate time left
            // console.log("data.totalSpecificityTerms:", data.totalSpecificityTerms);
            // console.log("data.totalQuestions:", data.total_terms);
            // console.log("data.termsCompleted:", data.termsCompleted);
            // console.log("data.termsIncorrect:", data.termsIncorrect);
            time_left_estimated = true;
            total_questions.set(data.total_terms);
            totalCompleted.set(data.termsCompleted); // total completed in the module
            totalIncorrect.set(data.termsIncorrect);
          }
      } catch (error) {
          console.error('Error retrieving terms data:', error);
      }
  }

  async function checkUserOwnership(): Promise<void> {
      try {
          const userID = await getUserID();  // Wait for userID to be populated
          const payload = { "userID": userID, "certification": certification };

          const response = await fetch(`${base_url}/get_user_ownership`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(payload)
          });
          
          const data = await response.json();
          
          userOwnership = data.ownsModule;
      } catch (error) {
          console.error('Error retrieving terms data:', error);
      }
  }  

    async function initializeEnv() {
        const userID = await getUserID();  // Wait for userID to be populated
        const payload = { userID: userID, module: moduleLevels[moduleName] };  // Add userID to the payload

        try {
            const response = await fetch(`${base_url}/initialize_env`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`Failed to initialize environment: ${response.statusText}`);
            }
            console.log('Environment initialized successfully.');
        } catch (error) {
            console.error('Error initializing environment:', error);
        }
    }

    // Function to clean up the environment on destroy
    async function cleanupEnv() {
    try {
        const userID = await getUserID(); // Wait for userID to be populated

        // Extract exam from the URL
        const url = new URL(window.location.href);
        const pathParts = url.pathname.split('/');
        const exam = decodeURIComponent(pathParts[pathParts.length - 1]); // Second-to-last part of the URL path

        // Validate required data
        if (!userID || !exam) {
            console.error("Missing required data for cleanup.");
            return;
        }

        // Construct the payload
        const payload = {
            userID: userID,
            exam: exam
        };

        console.log("Sending this to the /cleanup_env endpoint:", payload);

        const response = await fetch(`${base_url}/cleanup_env`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include', // Ensure credentials (cookies) are included
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Failed to clean up environment: ${response.statusText}`);
        }

        console.log('Environment cleaned up successfully.');
    } catch (error) {
        console.error('Error cleaning up environment:', error);
    }
}

    // Function to send a cleanup request before the page unloads
  async function sendCleanupEnv() {
      try {
          const userID = await getUserID();  // Replace with actual userID logic
          const url = new URL(window.location.href);
          const pathParts = url.pathname.split('/');
          console.log("pathPArts: ", pathParts);
          const examName = decodeURIComponent(pathParts[3]);
          console.log("examName: ", examName);
          const payload = JSON.stringify({ userID: userID, exam: examName });

          // Use Blob to send JSON data via sendBeacon
          const blob = new Blob([payload], { type: 'application/json' });
          navigator.sendBeacon(`${base_url}/cleanup_env`, blob);
      } catch (error) {
          console.error('Error sending cleanup request with sendBeacon:', error);
      }
  }

  function handleBeforeUnload() {
      if (!beforeUnloadTriggered) {
          beforeUnloadTriggered = true;
          sendCleanupEnv(); // Ensure cleanup runs before page unloads
      }
  }

  onMount(async () => {
    try {
        await initializeEnv();  // Ensure initializeEnv completes first
        scrollToBottom();  // Scroll the chat window
        await retrieveTermsData();  // Initial data load
        await checkUserOwnership();  // Check if the user owns the module

        console.log("Initial Module Name:", moduleName);
        console.log("Initial Section Name:", $sectionName);

        if (typeof window !== 'undefined') {
            window.addEventListener('beforeunload', handleBeforeUnload);
        }
    } catch (error) {
        console.error('Error during onMount:', error);
    }
});

onDestroy(async () => {
    try {
        if (!cleanupEnvTriggered) {
            cleanupEnvTriggered = true;
            await cleanupEnv(); // Await the cleanup to ensure it completes
        }

        if (typeof window !== 'undefined') {
            window.removeEventListener('beforeunload', handleBeforeUnload);
        }
    } catch (error) {
        console.error('Error during onDestroy:', error);
    }
});
</script>

<OutOfFundModal {remainingFreeQuestions} />

<div class="pt-8 px-5 xl:px-12 min-h-full flex flex-col">
  <ChatHeader {moduleName} {handleActivePlanChange} solvedTerms={$solvedTerms} totalTerms={$totalTerms} specificity={specificity}/>

  <ChooseDifficulty
    {activeDifficulty}
    {remainingFreeQuestions}
    isFreePlan={activePlan === "FREE"}
    on:difficultyChange={handleDifficultyChange}
    module={moduleName}
    specificity={specificity}
  />

  <div
    class="flex flex-col items-center justify-center gap-4 mt-4 pb-[26px] h-full flex-1"
  >
    <!-- Conversation -->
    <div
      class="max-w-[1116px] xl:w-[1116px] overflow-y-auto flex flex-col gap-4 hide-scrollbar pt-10 max-h-[calc(100vh-352px)] xl:max-h-[calc(100vh-230px)] custom-padding custom-padding-2"
      bind:this={chatEle}
    >
      {#each conversation as chatItem (chatItem.id)}
        <div
          class="flex items-start gap-6 {chatItem.sender === 'person'
            ? 'self-end message-person'
            : 'self-start message-bot custom-padding-botmessage'}"
          in:slide={{ duration: 200 }}
        >
          <div class={chatItem.sender === "person" ? "order-2" : "order-1"}>
            <Avatar
              src={chatItem.sender === "person"
                ? AvatarPersonImg
                : activePlan === "FREE"
                  ? AvatarBotFreeImg
                  : AvatarBotImg}
              width="w-9"
            />
          </div>
          <div
            class="{activePlan === 'FREE'
              ? 'bg-[#5E3EB7]/10'
              : 'bg-[#3B82F6]/10'} px-6 py-4 {chatItem.type === 'component'
              ? 'w-full max-w-[804px]'
              : 'max-w-[804px]'} min-w-[118px] text-xs text-white leading-[20px] {chatItem.sender ===
            'person'
              ? 'rounded-l-[40px] rounded-br-[55px] order-1 !bg-[#93C5FD]/25'
              : 'rounded-r-[40px] rounded-bl-[40px] order-2 custom-padding-botmessage'}"
          >
            {#if chatItem.type === "text"}
              <p >{@html chatItem.message}</p>
            {/if}

            {#if chatItem.type === "component"}
              <svelte:component this={chatItem.component} {...chatItem.props} />
            {/if}
          </div>
        </div>
      {/each}
    </div>
    <form
      class="w-full flex items-center justify-center mt-auto gap-6 !bg-transparent !border-none"
      on:submit|preventDefault={handleSubmit}
    >
    {#if moduleName == 'Diagnostic'}
      <Button
        variant="primary-blue"
        className="!min-w-0 !w-[750px] !h-[44px] lg:text-nowrap"
        on:click={(event) => firstQuestion ? generateNextQuestion() : handleViewTerms(event)}
        disabled={activePlan === "FREE" && remainingFreeQuestions <= 0}
      >
        {firstQuestion ? "Give me a question" : "View Terms"}
      </Button>
    {:else}
      <Button
        variant="secondary-blue"
        className="!min-w-0 !w-[350px] !h-[44px] lg:text-nowrap"
        on:click={handleViewTerms}
        disabled={activePlan === "FREE" && remainingFreeQuestions <= 0}
      >
        View Terms
      </Button>
    
      <Button
        variant="primary-blue"
        className="!min-w-0 !w-[350px] !h-[44px] lg:text-nowrap"
        on:click={generateNextQuestion}
        disabled={activePlan === "FREE" && remainingFreeQuestions <= 0}
      >
        Next Question
      </Button>
    {/if}
    </form>
  </div>
</div>

<style>
  @media (max-width: 1550px) {
    .custom-padding {
      padding-right: 6rem; /* Adjust as needed, 5rem = 80px */
    }
  }
  @media (max-width: 1375px) {
    .custom-padding-2 {
      padding-right: 10rem; /* Adjust as needed, 5rem = 80px */
    }
  }
  @media (max-width: 1250px) {
    .custom-padding-2 {
      padding-right: 13rem; /* Adjust as needed, 5rem = 80px */
    }
  }
  @media (max-width: 1250px) {
    .custom-padding-botmessage {
      padding-right: 6rem; /* Adjust as needed, 5rem = 80px */
    }
  }
</style>
