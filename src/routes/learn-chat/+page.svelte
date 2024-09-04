<script lang="ts">
    import { onMount } from 'svelte';
    import { Avatar, ProgressBar } from '@skeletonlabs/skeleton';
    import { marked } from 'marked';

    marked.setOptions({ breaks: true });
    let currentTerm = '';
    let currentAnswerResponse = {}; // When the user answers a question, the in/correct answer explanation and elaboration are stored here
    let currentQuestionData = {
        section: '',
        term: '',
        question: '',
        options: [],
        answer: ''
    };
    let elemChat: HTMLElement;
    let related_terms: string[] = [];
    type MessageContent = string | {
        section: string;
        term: string;
        question: string;
        options: string[];
        answer: string;
    };

    interface Message {
        id: number;
        host: boolean;
        avatar: number;
        name: string;
        timestamp: string;
        message: MessageContent;
        color: string;
    }

    let messageFeed: Message[] = [
        {
            id: 0,
            host: false,
            avatar: 48,
            name: 'AI Coach',
            timestamp: `Today @ ${getCurrentTimestamp()}`,
            message: 'Hi! This is your **AI coach** for the AWS SAA-03 exam. The goal of this section is to help you recall terms and definitions related to the exam by answering and getting feedback on multiple choice questions. Are you ready to get started?',
            color: 'variant-soft-primary'
        }
    ];

    let currentMessage = '';
    let threadId = '';
    let totalTerms = 1;
    let solvedTerms = 0;

    async function startThread(): Promise<void> {
        const response = await fetch('http://localhost:5000/start_thread', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
        const data = await response.json();
        threadId = data.thread_id;
    }

    async function updateStatus() {
        const payload = {
            term: currentTerm,
        };

        try {
            const response = await fetch('http://localhost:5000/update_status', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                console.log(`${currentTerm} passed!`);
                retrieveTermsData();
            } else {
                console.error(`Failed to update status for ${currentTerm}. Status: ${response.status}`);
            }
        } catch (error) {
            console.error(`Error updating status for ${currentTerm}:`, error);
        }
    }


    async function sendMessage(query: string): Promise<{ response: any, updateStatusCalled: boolean }> {
        const response = await fetch('http://localhost:5000/send_message', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ thread_id: threadId, message: query }) });
        console.log("Waiting for message from GPT")
        const data = await response.json();
        console.log("Message from the GPT: {data}", data)
        return data;
    }

    async function retrieveTermsData(): Promise<void> {
        const response = await fetch('http://localhost:5000/get_terms_data', { method: 'GET', headers: { 'Content-Type': 'application/json' } });
        const data = await response.json();
        totalTerms = data.totalTerms;
        solvedTerms = data.solvedTerms;
    }

    async function retrieveRelatedTermResponse(relatedTerm) {
        console.log("Retrieving related term response for term: ", currentTerm, "and related term: ", relatedTerm);
        const payload = {
            term: currentTerm,
            related_term: relatedTerm
        };

        const response = await fetch('http://localhost:5000/retrieve_related_term_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Related term response data from the API: ", data);
            return {
                relatedTermDefinition: data.related_term_definition,
                relatedTermExplanation: data.related_term_explanation
            };
        } else {
            console.error('Failed to retrieve related term response:', response.statusText);
        }
    }

    async function displayRelatedTermResponse(term, relatedTerm) {
        const response_data = await retrieveRelatedTermResponse(relatedTerm);
        
        if (response_data) {
            const { relatedTermDefinition, relatedTermExplanation } = response_data;
            const message = `Related term: ${relatedTerm}\nSummary: ${relatedTermDefinition}\nConnection: ${relatedTermExplanation}`;
            console.log("Related term response message:", message);

            const rt_response_message = {
                id: messageFeed.length,
                host: false,
                avatar: 48,
                name: 'AI Coach',
                timestamp: `Today @ ${getCurrentTimestamp()}`,
                message: message,
                color: 'variant-soft-primary'
            };

            // Update messages with the related term response
            messageFeed = [...messageFeed, rt_response_message];
        }
        else {
            console.error('Failed to display related term response');
        }
    }

    async function getSections(): Promise<void> {
        try {
            const response = await fetch('http://localhost:5000/get_remaining_sections', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log("Getting back the section data from getSections() (frontend):", data);
            const sectionMessage: Message = {
                id: messageFeed.length,
                host: false,
                avatar: 48,
                name: 'AI Coach',
                timestamp: `Today @ ${getCurrentTimestamp()}`,
                message: data.message,
                color: 'variant-soft-primary'
            };
            messageFeed = [...messageFeed, sectionMessage];
        } catch (error) {
            console.error('Error updating section:', error);
        }
    }

    async function getTerms(): Promise<void> {
        try {
            const response = await fetch('http://localhost:5000/get_remaining_terms', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            console.log("Getting back the term data from getTerms() (frontend):", data);
            const sectionMessage: Message = {
                id: messageFeed.length,
                host: false,
                avatar: 48,
                name: 'AI Coach',
                timestamp: `Today @ ${getCurrentTimestamp()}`,
                message: data.message,
                color: 'variant-soft-primary'
            };
            messageFeed = [...messageFeed, sectionMessage];
        } catch (error) {
            console.error('Error updating section:', error);
        }
    }

    async function retrieveQuestion(term: string | null = null): Promise<void> {
        related_terms = [];
        try {
            const response = await fetch('http://localhost:5000/get_question', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ thread_id: threadId, term }) // Sending the term if provided
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Getting back the question data from retrieveQuestion():', data);
            related_terms = data.related_terms;

            const questionMessage: Message = {
                id: messageFeed.length,
                host: false,
                avatar: 48,
                name: 'AI Coach',
                timestamp: `Today @ ${getCurrentTimestamp()}`,
                message: {
                    section: data.section || '',
                    term: data.term || '',
                    question: data.question || '',
                    options: [data.option1, data.option2, data.option3, data.option4] || [],
                    answer: data.answer || ''
                },
                color: 'variant-soft-primary'
            };
            messageFeed = [...messageFeed, questionMessage];
            currentTerm = data.term;
            currentQuestionData = data
        } catch (error) {
            console.error('Error retrieving question:', error);
        }
    }

    async function retrieveCorrectResponse(term) {
    try {
        const response = await fetch('http://localhost:5000/get_correct_response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ term: term })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Getting back the answer response data from retrieveCorrectResponse():', data);
        currentAnswerResponse = data;
        return data;
    } catch (error) {
        console.error('Error retrieving answer response:', error);
        return null; // Return null in case of error
    }
}

    async function retrieveIncorrectResponse(term, userAnswer) {
        try {
            const response = await fetch('http://localhost:5000/get_incorrect_response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ term: term, userAnswer: userAnswer })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log('Getting back the answer response data from retrieveInorrectResponse():', data);
            currentAnswerResponse = data;
            return data;
        } catch (error) {
            console.error('Error retrieving answer response:', error);
            return null; // Return null in case of error
        }
    }

    async function displayAnswerResponse(userAnswer) {
        let response_message = null; // Declare the variable outside the if-else blocks
        console.log("Submitting answer", userAnswer, "for term", {currentTerm});
        console.log("Current question answer:", currentQuestionData.answer);

        if (userAnswer == currentQuestionData.answer) {
            const data = await retrieveCorrectResponse(currentTerm); // Await the async function
            if (data) { // Ensure data is not null
                response_message = {
                    id: messageFeed.length,
                    host: false,
                    avatar: 48,
                    name: 'AI Coach',
                    timestamp: `Today @ ${getCurrentTimestamp()}`,
                    message: `Correct! ${data['explanation']}`,
                    color: 'variant-soft-primary'
                };
            }
            updateStatus();
            retrieveTermsData();
        } else {
            const incorrect_answer = currentQuestionData[userAnswer];
            const data = await retrieveIncorrectResponse(currentTerm, incorrect_answer); // Await the async function
            if (data) { // Ensure data is not null
                response_message = {
                    id: messageFeed.length,
                    host: false,
                    avatar: 48,
                    name: 'AI Coach',
                    timestamp: `Today @ ${getCurrentTimestamp()}`,
                    message: `Not quite. ${data['explanation']}`,
                    color: 'variant-soft-primary'
                };
            }
        }

        if (response_message) {
            console.log("Response message being added to messages:", response_message);
            messageFeed = [...messageFeed, response_message];
        } else {
            console.error('Failed to create a response message');
        }
    }

    function displayAnswerElaborateResponse(correct) {
        const data = currentAnswerResponse;
        if (data) { // Ensure data is not null
            const response_message = {
                id: messageFeed.length,
                host: false,
                avatar: 48,
                name: 'AI Coach',
                timestamp: `Today @ ${getCurrentTimestamp()}`,
                message: `${correct ? 'Correct' : 'Incorrect'} Explanation: ${data['elaborate']}`,
                color: 'variant-soft-primary'
            };
            messageFeed = [...messageFeed, response_message];
        } else {
            console.error('No currentAnswerResponse data available');
        }
    }

    async function resetTerms(): Promise<void> {
        const response = await fetch('http://localhost:5000/reset_terms', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
        if (response.ok) {
            solvedTerms = 0; // Reset the solvedTerms when terms are reset
            const resetMessage: Message = {
                id: messageFeed.length,
                host: false,
                avatar: 48,
                name: 'AI Coach',
                timestamp: `Today @ ${getCurrentTimestamp()}`,
                message: "All terms have been reset.",
                color: 'variant-soft-primary'
            };
            messageFeed = [...messageFeed, resetMessage];
        }
    }

    async function passAllTerms(): Promise<void> {
        const response = await fetch('http://localhost:5000/pass_all_terms', { method: 'POST', headers: { 'Content-Type': 'application/json' } });
        if (response.ok) {
            solvedTerms = totalTerms; // Mark all terms as solved
            const passedMessage: Message = {
                id: messageFeed.length,
                host: false,
                avatar: 48,
                name: 'AI Coach',
                timestamp: `Today @ ${getCurrentTimestamp()}`,
                message: "All terms have been passed.",
                color: 'variant-soft-primary'
            };
            messageFeed = [...messageFeed, passedMessage];
        }
    }

    function scrollChatBottom(behavior?: ScrollBehavior): void {
        elemChat.scrollTo({ top: elemChat.scrollHeight, behavior });
    }

    function getCurrentTimestamp(): string {
        return new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });
    }

    async function addMessage(messageContent = ''): Promise<void> {
        if (messageContent.trim() === '' && currentMessage.trim() === '') return;
        const messageToSend = messageContent || currentMessage;

        const userMessage: Message = {
            id: messageFeed.length,
            host: true,
            avatar: 48,
            name: 'You',
            timestamp: `Today @ ${getCurrentTimestamp()}`,
            message: messageToSend,
            color: 'variant-soft-primary'
        };
        messageFeed = [...messageFeed, userMessage];

        const botMessage: Message = {
            id: messageFeed.length,
            host: false,
            avatar: 48,
            name: 'AI Coach',
            timestamp: `Today @ ${getCurrentTimestamp()}`,
            message: '🤖',
            color: 'variant-soft-primary'
        };
        messageFeed = [...messageFeed, botMessage];

        currentMessage = '';

        // Scroll to the bottom to show the new message
        setTimeout(() => {
            scrollChatBottom('smooth');
        }, 0);

        // Animate robot emojis while waiting for the response
        const interval = setInterval(() => {
            if (typeof botMessage.message === 'string') {
                botMessage.message += '🤖';
                messageFeed = [...messageFeed];
            }
        }, 1000);

        const { response, updateStatusCalled } = await sendMessage(messageToSend);

        clearInterval(interval);

        // Check if response is a JSON string
        console.log("Here the response from the GPT: {response}", response)
        console.log("response is of type: ", typeof response)
        let parsedResponse;
        if (response.startsWith('{')) {
            try {
                parsedResponse = JSON.parse(response);
                console.log('Parsed response:', parsedResponse);

                // Ensure all properties are correctly assigned
                botMessage.message = {
                    section: parsedResponse.section || '',
                    term: parsedResponse.term || '',
                    question: parsedResponse.question || '',
                    options: parsedResponse.options || [],
                    answer: parsedResponse.answer || ''
                };
                console.log('Bot message:', botMessage.message);

            } catch (e) {
                console.error('Failed to parse response as JSON:', e);
                botMessage.message = response;
            }
        } else {
            botMessage.message = response.replace(/^(\w+)\1/, '$1'); // Remove repeating words
        }
        messageFeed = [...messageFeed];

        setTimeout(() => {
            scrollChatBottom('smooth');
        }, 0);
    }

    function onPromptKeydown(event: KeyboardEvent): void {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Prevent the default behavior of adding a newline
            addMessage();
        }
    }

    function renderMarkdown(markdown: string): string {
        return marked(markdown);
    }

    function isString(message: MessageContent): message is string {
        return typeof message === 'string';
    }

    function isSectionList(message: string): boolean {
        return message.startsWith("Sure, here are the remaining sections");
    }

    function isTermsList(message: string): boolean {
        return message.startsWith("Sure, here are the remaining terms");
    }

    function isRelatedTerm(message: string): boolean {
        return message.startsWith("Related term:");
    }

    function formatMessage(message) {
        // Extract the parts of the message using regex
        const relatedTermMatch = message.match(/Related term:\s*(.*)/);
        const summaryMatch = message.match(/Summary:\s*(.*)/);
        const connectionMatch = message.match(/Connection:\s*(.*)/);

        if (!relatedTermMatch || !summaryMatch || !connectionMatch) {
            return message;
        }

        const relatedTerm = relatedTermMatch[1].trim();
        const summary = summaryMatch[1].trim();
        const connection = connectionMatch[1].trim();

        // Replace all instances of related term with underlined term
        const underlinedTerm = `<u>${relatedTerm}</u>`;
        const formattedSummary = summary.replace(new RegExp(relatedTerm, 'g'), underlinedTerm);
        const formattedConnection = connection.replace(new RegExp(relatedTerm, 'g'), underlinedTerm);

        // Create formatted HTML
        const formattedMessage = `
            <div>
            <div class="card-hover" style="background-color: navy; padding: 20px; border-radius: 5px; margin-top: 10px; max-width: 600px; word-wrap: break-word; overflow-wrap: break-word; white-space: normal; width: 100%; display: flex; flex-direction: column;">
                <div style="text-align: center; font-size: 1.5rem; font-weight: bold; margin-bottom: 10px;">Summary</div>
                <p style="text-align: left; font-size: 1rem;">${formattedSummary}</p>
            </div>
            <div class="card-hover" style="background-color: green; padding: 20px; border-radius: 5px; margin-top: 10px; max-width: 600px; word-wrap: break-word; overflow-wrap: break-word; white-space: normal; width: 100%; display: flex; flex-direction: column;">
                <div style="text-align: center; font-size: 1.5rem; font-weight: bold; margin-bottom: 10px;">Connection</div>
                <p style="text-align: left; font-size: 1rem;">${formattedConnection}</p>
            </div>
            </div>
        `;

        return formattedMessage;
    }

    function updateSection(section: string): void {
        // Define the endpoint and payload
        const endpoint = 'http://localhost:5000/update_section';
        const payload = { section: section };

        // Send a POST request to the /update_section endpoint with the section data
        fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        // Add a message to the thread without waiting for a response
        let message = {
                    section: section,
                    term: 'Select next question or choose a term',
                    question: "",
                    options: [],
                    answer: ''
                }
        console.log(`Section has been updated to ${section}`)

        // Add a message from the AI saying "Section has been updated to [section]"
        const botMessage: Message = {
            id: messageFeed.length,
            host: false,
            avatar: 48,
            name: 'AI Coach',
            timestamp: `Today @ ${getCurrentTimestamp()}`,
            message: message,
            color: 'variant-soft-primary'
        };
        messageFeed = [...messageFeed, botMessage];
    }

    onMount(async () => {
        await startThread();
        scrollChatBottom();
        retrieveTermsData();
    });
</script>

<div class="h-full grid grid-rows-[1fr_auto] gap-1">
    <section bind:this={elemChat} class="flex-1 p-4 overflow-y-auto space-y-4">
        {#each messageFeed as bubble}
            {#if bubble.host === false}
                <div class="grid grid-cols-[auto_1fr] gap-2">
                    <Avatar src={`https://i.pravatar.cc/?img=${bubble.avatar}`} width="w-12" />
                    <div class="card p-4 variant-soft rounded-tl-none space-y-2">
                        {#if typeof bubble.message === 'object'}
                            <header class="flex justify-between items-center card-header">
                                <p class="text-lg font-bold">{bubble.message.section} - {bubble.message.term}</p>
                                <small class="opacity-50">{bubble.timestamp}</small>
                            </header>
                            <section class="p-4">
                                <p class="text-lg font-bold"><strong>{@html renderMarkdown(bubble.message.question)}</strong></p>
                                {#each bubble.message.options as option, index}
                                    <p class="mb-4"><button class="option-btn card-hover btn bg-primary-500 card-hover rounded-container-token" on:click={() => displayAnswerResponse("option" + (index + 1))}>{option}</button></p>
                                {/each}
                            </section>
                        {:else if isSectionList(bubble.message)}
                            <div class="grid grid-cols-2 auto-rows-max gap-2">
                                {#each bubble.message.split('\n').slice(1).filter(item => item.trim() !== '').map(item => item.trim()) as item}
                                    <button class="btn bg-secondary-500 card-hover rounded-container-token" on:click={() => updateSection(item)}>{item}</button>
                                {/each}
                            </div>
                        {:else if isTermsList(bubble.message)}
                            <div class="grid grid-cols-2 auto-rows-max gap-2">
                                {#each bubble.message.split('\n').slice(1).filter(item => item.trim() !== '').map(item => item.trim()) as item}
                                    <button class="btn bg-secondary-500 card-hover rounded-container-token" on:click={() => retrieveQuestion(item)}>{item}</button>
                                {/each}
                            </div>
                        {:else if isRelatedTerm(bubble.message)}
                            {@html formatMessage(bubble.message)}
                        {:else}
                            {#if bubble.message.includes('Not quite')}
                                <!-- Custom rendering for "Not quite" messages -->
                                <div class="red-div btn card-hover" on:click={() => displayAnswerElaborateResponse(false)}>
                                    <div class="header">Incorrect</div>
                                    <p class="text-content">{@html renderMarkdown(bubble.message)}</p>
                                </div>
                                <div class="blue-div btn card-hover">
                                    <div class="header">If you want to learn more</div>
                                    <div class="flex justify-center flex-wrap gap-2 mt-4">
                                        {#each related_terms as relatedTerm}
                                            <button class="btn bg-secondary-500 card-hover rounded-container-token" on:click={() => displayRelatedTermResponse(currentTerm, relatedTerm)}>{relatedTerm}</button>
                                        {/each}
                                    </div>
                                </div>
                            {:else if bubble.message.includes('Correct!')}
                                <div class="green-div btn card-hover" on:click={() => displayAnswerElaborateResponse(true)}>
                                    <div class="header">Correct!</div>
                                    <p class="text-content">{@html renderMarkdown(bubble.message.split('Correct!')[1])}[1]}</p>
                                </div>
                                <div class="blue-div btn card-hover">
                                    <div class="header">If you want to learn more</div>
                                    <div class="flex justify-center flex-wrap gap-2 mt-4">
                                        {#each related_terms as relatedTerm}
                                            <button class="btn bg-secondary-500 card-hover rounded-container-token" on:click={() => displayRelatedTermResponse(currentTerm, relatedTerm)}>{relatedTerm}</button>
                                        {/each}
                                    </div>
                                </div>
                            {:else if bubble.message.includes('Correct Explanation')}
                                <div class="green-div btn card-hover">
                                    <div class="header">Correct Explanation</div>
                                    <p class="text-content">{@html bubble.message.split('Correct Explanation:')[1]}</p>
                                </div>
                                <div class="blue-div btn card-hover">
                                    <div class="header">If you want to learn more</div>
                                    <div class="flex justify-center flex-wrap gap-2 mt-4">
                                        {#each related_terms as relatedTerm}
                                            <button class="btn bg-secondary-500 card-hover rounded-container-token" on:click={() => displayRelatedTermResponse(currentTerm, relatedTerm)}>{relatedTerm}</button>
                                        {/each}
                                    </div>
                                </div>
                            {:else if bubble.message.includes('Incorrect Explanation')}
                                <div class="red-div btn card-hover">
                                    <div class="header">Inorrect Explanation</div>
                                    <p class="text-content">{@html bubble.message.split('Incorrect Explanation:')[1]}</p>
                                </div>
                                <div class="blue-div btn card-hover">
                                    <div class="header">If you want to learn more</div>
                                    <div class="flex justify-center flex-wrap gap-2 mt-4">
                                        {#each related_terms as relatedTerm}
                                            <button class="btn bg-secondary-500 card-hover rounded-container-token" on:click={() => displayRelatedTermResponse(currentTerm, relatedTerm)}>{relatedTerm}</button>
                                        {/each}
                                    </div>
                                </div>
                            {:else}
                                <p>{@html renderMarkdown(bubble.message)}</p>
                            {/if}
                        {/if}
                    </div>
                </div>
            {:else}
                <div class="grid grid-cols-[1fr_auto] gap-2">
                    <div class="card p-4 rounded-tr-none space-y-2 {bubble.color}">
                        <header class="flex justify-between items-center">
                            <p class="font-bold">{bubble.name}</p>
                            <small class="opacity-50">{bubble.timestamp}</small>
                        </header>
                        {#if isString(bubble.message)}
                            <p>{@html renderMarkdown(bubble.message)}</p>
                        {/if}
                    </div>
                    <Avatar src={`https://i.pravatar.cc/?img=${bubble.avatar}`} width="w-12" />
                </div>
            {/if}
        {/each}
    </section>
    <section class="border-t border-surface-500/30 p-4">
        <div class="flex items-center space-x-2">
            <button class="btn bg-warning-500 card-hover rounded-container-token" on:click={resetTerms}>Reset</button>
            <div class="relative w-full">
                <ProgressBar
                    value={solvedTerms}
                    max={totalTerms}
                    height="h-10"
                    rounded="rounded-md"
                    transition="transition-[width]"
                    meter="bg-primary-500"
                    track="bg-surface-200"
                    labelledby="progress-label"
                />
                <div id="progress-label" class="absolute inset-0 flex justify-center items-center text-white font-bold">
                    {solvedTerms} / {totalTerms}
                </div>
            </div>
            <button class="btn bg-success-500 card-hover rounded-container-token" on:click={passAllTerms}>Got it</button>
        </div>
        <div class="grid grid-cols-4 gap-2 mb-2 mt-2">
            <button class="btn bg-primary-500 card-hover rounded-container-token" on:click={() => retrieveQuestion()}>Retrieve question</button>
            <button class="btn bg-primary-500 card-hover rounded-container-token" on:click={() => getSections()}>Remaining Sections</button>
            <button class="btn bg-primary-500 card-hover rounded-container-token" on:click={() => getTerms()}>Remaining Terms</button>
            <button class="btn bg-primary-500 card-hover rounded-container-token" on:click={() => addMessage('This is the greatest piece of software ever thank you for making it')}>Thank the Dev</button>
        </div>
        <div class="input-group grid-cols-[1fr_auto] rounded-container-token">
            <textarea
                bind:value={currentMessage}
                class="bg-transparent border-0 ring-0"
                name="prompt"
                id="prompt"
                placeholder="Write a message..."
                rows="1"
                on:keydown={onPromptKeydown}
            ></textarea>
            <button class="btn bg-primary-500 card-hover rounded-r-container-token" on:click={() => addMessage(currentMessage)}>
                Send
            </button>
        </div>
    </section>
</div>

<style>
    .input-group > button {
        border-radius: 0 var(--rounded-container-token) var(--rounded-container-token) 0;
        padding-right: 1.5rem;
        padding-left: 1.5rem;
    }

    .relative {
        position: relative;
    }

    .absolute {
        position: absolute;
    }

    .red-div, .green-div, .blue-div {
        padding: 20px; /* More padding on all sides */
        border-radius: 5px;
        margin-top: 10px;
        max-width: 600px; /* Adjust the width as needed */
        word-wrap: break-word; /* Ensure text wraps within the div */
        overflow-wrap: break-word; /* Ensure text wraps within the div */
        white-space: normal; /* Ensure text wraps within the div */
        width: 100%; /* Ensure the divs are the same width */
        display: flex;
        flex-direction: column;
    }

    .red-div {
        background-color: red;
    }

    .green-div {
        background-color: green;
    }

    .blue-div {
        background-color: navy; /* Changed to navy blue */
    }

    .header {
        text-align: center;
        font-size: 1.5rem; /* Larger font size */
        font-weight: bold;
        margin-bottom: 10px; /* Space between header and text */
    }

    .text-content {
        text-align: left; /* Left align the text content */
        font-size: 1rem; /* Adjust the font size if needed */
    }

    .flex-wrap {
        justify-content: center; /* Center align the buttons within the div */
    }
</style>

