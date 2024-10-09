### Overview of the Backend

The backend of the application is a Flask-based API designed to manage user sessions, interact with OpenAI for chat functionality, and handle user progress data through Firebase. It processes user requests such as retrieving or submitting questions and responses, manages term data for multiple modules (learn, understand, apply), and uses Firebase for storage and retrieval of terms data. The backend can be run locally or in the cloud, with `firebase_admin_init_cloud.py` and `firebase_admin_init_local.py` handling the connection to Firebase based on the environment.

### Key Files

#### `app.py`

This file contains the main logic for the API, including all the routes for interacting with the front end, managing user sessions, and handling question/answer logic for the platform.

- **Firebase and Cloud Storage**: Depending on whether the app is running locally or in the cloud, the backend uses either `firebase_admin_init_cloud.py` or `firebase_admin_init_local.py` for Firebase database (`db`) and cloud storage (`bucket`) operations.
- **Global Variables**: The OpenAI client is initialized with an API key for generating responses, and the assistant ID is set for answering questions.
- **Session Management**: The `UserManager` class is used to handle user sessions and term data for the modules.

**Main Routes and Functions**:
- `/start_thread`: Starts a new thread in OpenAI for the chat session.
- `/set_assistant_id`: Sets the OpenAI assistant ID used for querying questions.
- `/send_message`: Handles sending messages to OpenAI and streaming responses back to the front end.
- `/initialize_env`: Initializes the user environment by loading terms for a specific module (learn, understand, or apply) and storing the term manager for each user.
- `/cleanup_env`: Cleans up the user session by saving the terms data back to Firebase and deleting local files.
- `/get_terms_data`: Retrieves the total and solved terms for a user.
- `/update_status`: Updates the status of a specific term as "solved" for a user.
- `/get_question`: Retrieves a new question for the user based on their progress.
- `/get_correct_response` and `/get_incorrect_response`: Fetches the correct or incorrect response explanations for a specific term.
- `/reset_terms` and `/pass_all_terms`: Resets or marks all terms as passed for a user.
  
#### `user_manager.py`

The `UserManager` class is responsible for managing the user's term data and handling interactions with Firebase storage.

- **Term Managers**: It maintains a dictionary (`self.term_managers`) that stores a `TermManager` instance and the associated module (learn, understand, apply) for each user.
- **Session Initialization**: The `initialize_user_session` method initializes a session for a user, downloading their `terms.json` from Firebase Cloud Storage or using a default file if no data is available.
- **Session Cleanup**: The `cleanup_user_session` method uploads the user's `terms.json` back to Firebase Cloud Storage when their session ends, and removes the local file afterward.

**Key Functions**:
- `manage_user_json`: Handles downloading or creating the user's `terms.json` file.
- `initialize_user_session`: Initializes a session for the user by creating the necessary term manager and loading their terms data.
- `cleanup_user_session`: Saves the user’s progress by uploading their terms data back to Firebase Cloud Storage and cleaning up local files.

#### `term_manager.py`

The `TermManager` class handles reading and writing the user's `terms.json` file and managing the progress of terms within each module.

- **Loading and Saving Terms**: The `terms.json` file is loaded when the `TermManager` is initialized and is written to when the session is finished or terms are updated.
- **Sections and Terms**: Each user’s data is divided into sections (like Networking), and each section contains multiple terms.
  
**Key Functions**:
- `_read_json` and `write_terms_to_file`: Load the user's `terms.json` file from local storage and save it back.
- `get_correct_response` and `get_incorrect_response`: Retrieve the correct or incorrect answer explanations for a specific term.
- `update_status`: Marks a term as passed by setting its value to `True` in the `terms.json` file.
- `get_not_passed_terms`: Retrieves terms that have not yet been passed for a specific section.
- `get_remaining_sections`: Lists sections that still have terms remaining to be solved.

### Data Flow

1. **Session Initialization**: When a user starts a session, `app.py` calls the `/initialize_env` endpoint, which triggers `UserManager` to create a `TermManager` for the user, downloading their `terms.json` file or using a default.
   
2. **Question Retrieval**: When a user requests a new question, the `/get_question` endpoint is called, which uses `TermManager` to find an unsolved term and return a corresponding question.

3. **Answer Submission**: When a user answers a question, `/update_status` updates their progress in `terms.json`. If the answer is incorrect, the term manager fetches the incorrect response explanation.

4. **Session Cleanup**: When the user finishes their session, `/cleanup_env` is called, which uses `UserManager` to upload the updated `terms.json` back to Firebase and clean up the local files.

This backend structure allows the platform to manage multiple users, each with their own progress tracking, and handle data consistently across sessions using Firebase Cloud Storage. The logic in `app.py` ties everything together, providing an API that manages session state, retrieves questions and responses, and tracks user progress.
