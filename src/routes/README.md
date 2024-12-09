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

### 4. Chat Pages (Apply, Understand, Learn, or Diagnostic, Concept Mastery, Term Mastery)
The chat pages (e.g., `/new/learn/open` and `/new/learn/overview`) utilize dynamic routing to produce different elements depending on the relevant exam (AWS Certified Solutions Architect).

(Currently a lot of churn in this area so waiting for that before solidifying documenation)

### Firebase Integration
- The `userId` store from Firebase handles user authentication.
- Firebase authentication (`onAuthStateChanged`) is used to get the user’s token (`idToken`), which is required for accessing protected routes like `/get_user_decks` and `/get_terms_data`.

### Svelte Lifecycle Hooks
- **onMount**: Used on most pages to fetch initial data (e.g., decks, user info, or terms).
- **onDestroy**: Ensures that any environment setup (like threads or sessions) is cleaned up when the user navigates away.
  - For instance, `cleanupEnv` ensures the user’s environment is reset when they leave the chat pages.

## Conclusion
The frontend of the platform is a combination of Svelte’s reactivity, store management, Firebase authentication, and backend interactions. Each page is structured around a core set of stores (`decks`, `userDecks`, `messageFeed`) and functions (`retrieveQuestion`, `sendMessage`, `updateStatus`) that ensure a dynamic and interactive learning experience for users. The UI is cleanly structured with **Skeleton UI** components to enhance visual consistency across the platform.
