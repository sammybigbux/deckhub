# Backend Structure Overview

The backend primarily consists of:
- **Main Application (`app.py`)**: This contains the core logic for handling requests from the frontend, interacting with Firebase Firestore and Cloud Storage, and managing users and terms through helper classes.
- **Helper Classes**:
  - `UserManager`: Manages users, their sessions, and their data files.
  - `TermManager`: Manages the terms and their statuses for each user.
- **Firebase Initialization Files**:
  - `firebase_admin_init_cloud.py`: Initializes Firebase Admin SDK for cloud deployments using credentials stored in Secret Manager.
  - `firebase_admin_init_local.py`: Initializes Firebase Admin SDK for local deployments using a service account file stored locally. 

## Application Workflow

### `app.py`

The `app.py` file defines the main Flask application that handles various endpoints. It handles:
- **Initializing and cleaning user environments** (`/initialize_env`, `/cleanup_env`)
- **Starting and managing user sessions** (`/start_thread`, `/send_message`)
- **Handling term-based functionality** (`/get_terms_data`, `/get_question`, `/update_status`, etc.)
- **Interacting with Firestore and Stripe for user data and payment processing** (`/create_user_if_not_exists`, `/api/create-checkout-session`, `/webhook`)

Key components include:

1. **Firebase Setup**:
   - Firebase Admin SDK is initialized with either local or cloud credentials (depending on environment).
   - Firestore is used for storing user data, while Cloud Storage is used to store and retrieve the `terms.json` files for each user.

2. **Data Loading**:
   - The backend loads static data from `learn_data.json`, `understand_data.json`, and `apply_data.json` from the `static_data` directory. These are used in various term-based operations.

3. **User and Term Management**:
   - The backend relies heavily on `UserManager` and `TermManager` for managing user sessions and interacting with `terms.json`.
   - `UserManager` handles downloading/uploading the user’s `terms.json` from/to Cloud Storage and initializing sessions.
   - `TermManager` handles loading the user's terms data, providing questions, and updating the status of terms.

### Helper Classes

#### `UserManager`
- **Manages User Sessions**: 
  - For each user, a new `TermManager` instance is created to handle the user's interaction with the current module (learn, understand, apply).
  - The user's `terms.json` file is downloaded from Cloud Storage (or initialized with default terms) when a session is started and uploaded when the session ends.
- **Functions**:
  - `initialize_user_session`: Initializes a user’s session, creates a `TermManager` for them, and retrieves their `terms.json` file.
  - `manage_user_json`: Downloads the user's `terms.json` from Cloud Storage if it exists, or creates one from a default template if it doesn't.
  - `cleanup_user_session`: Uploads the `terms.json` file back to Cloud Storage and deletes the local file when the session is cleaned up.

#### `TermManager`
- **Manages User's Terms**: 
  - Loads, updates, and provides terms-related data for a user.
  - Each user's progress (solved terms) is tracked in their `terms.json`.
- **Functions**:
  - `_read_json`: Reads the user's `terms.json`.
  - `write_terms_to_file`: Writes the updated terms to `terms.json` at the end of the session.
  - `retrieve_question`: Retrieves a question for the user based on their unsolved terms.
  - `update_status`: Updates the status of a term to mark it as solved.
  - `get_correct_response` and `get_incorrect_response`: Fetch correct or incorrect responses for terms.

### Firebase Initialization Files

#### `firebase_admin_init_cloud.py`
- Fetches Firebase credentials from Google Secret Manager.
- Initializes the Firebase Admin SDK with those credentials for Cloud deployments.
- Initializes Firestore and Cloud Storage connections.

#### `firebase_admin_init_local.py`
- Loads Firebase credentials from a local `firebase_key.json` file for local development.
- Initializes the Firebase Admin SDK for local use.
- Initializes Firestore and Cloud Storage connections.

enjoy :)



