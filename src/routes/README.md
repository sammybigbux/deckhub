## Overview
The frontend of the platform is built using **Svelte** with **TypeScript** and utilizes **Svelte stores** for state management, Firebase for authentication (`userId`, `isLoggedIn`), and **Skeleton UI** for components like **Avatars** and **ProgressBars**. It interacts with a backend hosted on either localhost or a cloud server (`base_url`).

## Key Pages and Functionality

### 1. My-Cards Page (`my-cards.svelte`)
- **Purpose**: Displays the user's purchased decks and allows them to search through their decks.
- **Stores**: 
  - `allDecks` and `userOwnedDeckNames` store the available decks and the decks owned by the user.
  - `searchQuery` stores the search input, and the **derived store** `filteredDecks` filters decks based on the search query and ownership.
- **Functions**:
  - `handleInput` updates the search input field.
  - On mount, the page fetches all decks using the `/get_decks` endpoint and then fetches the user-specific decks using the `/get_user_decks` endpoint, passing the **Firebase token** for authentication (`idToken`).
- **UI Elements**:
  - Decks are listed with an option to either **download** (for owned decks) or **purchase** (for decks not owned).

### 2. Search Page (`search.svelte`)
- **Purpose**: A place for users to search all products and decks.
- **Stores**:
  - `searchQuery` is used to store user input from the search bar.
  - `decks` holds all decks fetched from the backend.
  - `filteredDecks` is derived from `searchQuery` and `decks` to filter the decks based on the user’s input.
- **Functions**:
  - `handleInput` updates `searchQuery` as the user types.
  - On mount, the function makes a GET request to `/get_decks` to populate `decks`. Additionally, it fetches the user’s decks via `/get_user_decks` using the Firebase token (`idToken`).
- **UI Elements**:
  - A search bar filters available decks.
  - Each deck has buttons to either **purchase** or **open** based on user ownership status.

### 3. User-Info Page (`user-info.svelte`)
- **Purpose**: Displays user account information such as payment info, past orders, and allows log out.
- **Stores**:
  - `tabSet` tracks which tab (Payment Information, Past Orders, Funding, Log out) is currently active.
- **Functions**:
  - `onMount`: Checks the URL hash to set the active tab.
- **UI Elements**:
  - The page consists of tabbed content where each tab shows a specific section of the user's information.

### 4. Chat Pages (Learn, Understand, Apply)
The chat pages (e.g., `learn-multiple`, `learn-open`, `understand-multiple`, `apply-multiple`) are built on similar structures with differences based on the mode (multiple choice or open-ended).

#### Learn-Multiple Page (`learn-multiple.svelte`)
- **Purpose**: Delivers multiple-choice questions to the user based on terms relevant to their study.
- **Stores**:
  - `messageFeed` holds the conversation history.
  - `related_terms` holds terms related to the current question.
  - `currentTerm` and `currentQuestionData` store the current question’s data.
- **Functions**:
  - `retrieveTermsData`: Fetches the user's progress (total and solved terms).
  - `retrieveQuestion`: Fetches the next question from the backend and updates the chat.
  - `displayAnswerResponse`: Displays feedback (correct/incorrect) when the user answers a question.
  - `toggle_multi`: Switches between multiple-choice and open-ended modes.
  - `updateStatus`: Updates the user’s progress after answering correctly.
  - `sendMessage`: Sends a user query to the backend and streams back a response.
- **UI Elements**:
  - The page includes a chat interface where the **AI Coach** guides the user through questions.
  - Users answer multiple-choice questions by clicking on buttons representing the options.

#### Learn-Open Page (`learn-open.svelte`)
- **Purpose**: Similar to `learn-multiple` but for open-ended questions.
- **Key Differences**:
  - Instead of multiple-choice, users submit their own written responses.
  - The function `change_difficulty` adjusts the AI's response difficulty.

### General Components
Across all pages, common components include:
- **Avatar**: Displays the profile picture of the user or AI in the chat.
- **ProgressBar**: Shows the user's progress within the session (e.g., total terms completed out of total terms).
- **Textareas** for user input and **buttons** for interactions such as answering questions or navigating through sections.

### Firebase Integration
- The `userId` store from Firebase handles user authentication.
- Firebase authentication (`onAuthStateChanged`) is used to get the user’s token (`idToken`), which is required for accessing protected routes like `/get_user_decks` and `/get_terms_data`.

### Svelte Lifecycle Hooks
- **onMount**: Used on most pages to fetch initial data (e.g., decks, user info, or terms).
- **onDestroy**: Ensures that any environment setup (like threads or sessions) is cleaned up when the user navigates away.
  - For instance, `cleanupEnv` ensures the user’s environment is reset when they leave the chat pages.

## Conclusion
The frontend of the platform is a combination of Svelte’s reactivity, store management, Firebase authentication, and backend interactions. Each page is structured around a core set of stores (`decks`, `userDecks`, `messageFeed`) and functions (`retrieveQuestion`, `sendMessage`, `updateStatus`) that ensure a dynamic and interactive learning experience for users. The UI is cleanly structured with **Skeleton UI** components to enhance visual consistency across the platform.
