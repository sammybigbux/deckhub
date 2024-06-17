<script>
    import { writable, derived } from 'svelte/store';
    import { goto } from '$app/navigation';
    import { isLoggedIn } from '../../stores/auth'; // Adjust the import path as needed

    let searchQuery = writable('');

    const exams = writable([
        {
            name: 'AWS Certified Solutions Architect',
            icon: '🖥️',
            title: 'aws-certified-solutions-architect',
            length: 200,
            lastUpdated: '2024-06-01'
        },
        {
            name: 'Google Cloud Professional Data Engineer',
            icon: '☁️',
            title: 'google-cloud-professional-data-engineer',
            length: 180,
            lastUpdated: '2024-05-15'
        },
        {
            name: 'Microsoft Certified: Azure Fundamentals',
            icon: '🔧',
            title: 'microsoft-certified-azure-fundamentals',
            length: 220,
            lastUpdated: '2024-04-20'
        }
    ]);

    const filteredExams = derived([searchQuery, exams], ([$searchQuery, $exams]) => {
        return $exams.filter(exam =>
            exam.name.toLowerCase().includes($searchQuery.toLowerCase())
        );
    });

    function handleInput(event) {
        searchQuery.set(event.target.value);
    }

    function navigateToExam(exam) {
        goto(`/${exam.title}`);
    }
</script>

<style>
    .search-container {
        padding: 16px;
    }
    .search-bar {
        width: 100%;
        padding: 8px;
        margin-bottom: 16px;
        font-size: 1em;
        border: 1px solid #ccc;
        border-radius: 4px;
        color: black; /* Ensure the search bar text is black */
    }
    .exam-list {
        list-style-type: none;
        padding: 0;
    }
    .exam-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px;
        border-bottom: 1px solid #eee;
        background-color: #333; /* Darker Skeleton UI color */
        border-radius: 8px;
        margin-bottom: 8px;
        transition: background 0.3s;
        color: #fff; /* White text for contrast */
    }
    .exam-item:hover {
        background: #444; /* Slightly lighter Skeleton UI color */
    }
    .exam-content {
        display: flex;
        align-items: center;
        flex: 1;
    }
    .exam-icon {
        font-size: 1.5em;
        margin-right: 12px;
    }
    .exam-info {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }
    .exam-title {
        font-size: 1em;
        color: #fff; /* Ensure title text is white */
        flex: 1;
    }
    .exam-details {
        display: flex;
        flex-direction: column;
        font-size: 0.9em;
        color: #ddd; /* Slightly lighter text for details */
        margin-left: auto; /* Push details to the right */
    }
    .btn {
        margin-left: 12px; /* Add some space between details and button */
    }
    @media (max-width: 600px) {
        .exam-title {
            font-size: 0.9em;
        }
        .exam-details {
            font-size: 0.8em;
        }
    }
</style>

<div class="search-container">
    <input
        type="text"
        class="search-bar"
        placeholder="Search exams..."
        on:input={handleInput}
    />
    <ul class="exam-list">
        {#each $filteredExams as exam}
            <li class="exam-item bg-gradient-to-br variant-gradient-tertiary-secondary" on:click={() => navigateToExam(exam)}>
                <div class="exam-content">
                    <div class="exam-icon">{exam.icon}</div>
                    <div class="exam-info">
                        <div class="exam-title">{exam.name}</div>
                        <div class="exam-details">
                            <span>{exam.length} cards</span>
                            <span>{exam.lastUpdated}</span>
                        </div>
                    </div>
                </div>
                {#if $isLoggedIn}
                    <button class="btn bg-primary-500 card-hover">Buy</button>
                {:else}
                    <button class="btn bg-primary-500 card-hover">Login to download</button>
                {/if}
            </li>
        {/each}
    </ul>
</div>
