# Project Name

This backend is to serve all the data needed for the chat functionality. It uses Flask to serve different modules (Learn, Understand, Apply) on different ports. Each module is managed by its own instance of `TermManager`, which loads and processes data from specific directories.

## Directory Structure

The root directory contains the following important files and directories:

### 1. **`openai_integration.py`**
   - This file integrates with the OpenAI API to handle queries and responses using an assistant model. It handles creating threads, sending messages, and processing responses.

### 2. **`term_manager.py`**
   - This is the core script for managing term data. It reads from and writes to JSON files, calculates completion statuses, and manages interactions related to learning terms.

### 3. **`apply_data/`, `learn_data/`, `understand_data/`**
   - These three directories correspond to the different modules (Apply, Learn, Understand). Each directory contains:
     - **`input/`**: Contains raw data files used to generate the output data. This data is processed by scripts in the `data_scripts/` folder.
     - **`output/`**: Contains the processed data files that are served by the Flask server.

### 4. **`data_scripts/`**
   - Contains scripts used to generate the output data. These scripts process the raw data from the `input/` directories and produce the JSON files that are served by the Flask server from the `output/` directories.

### 5. **`data/`**
   - This directory contains the primary data for the application, organized into the aforementioned input and output subdirectories within the `apply_data`, `learn_data`, and `understand_data` directories. The data in these folders is used by the corresponding `TermManager` instances for each module.


## Running the backend server

### Prerequisites
- Python 3.x
- Pip (Python package installer)
- OpenAI API Key (set in the `.env` file)

### Setting Up

**Running the Flask Servers:**

   You will need to run the Flask servers for each module on different ports:

   - **Learn Module:**
     ```bash
     export PORT=5000
     python openai_integration.py
     ```
   - **Understand Module:**
     ```bash
     export PORT=5001
     python openai_integration.py
     ```
   - **Apply Module:**
     ```bash
     export PORT=5002
     python openai_integration.py
     ```

   Each server will serve its respective data from the `output/` directory of the corresponding data directory (`apply_data`, `learn_data`, `understand_data`).

## Usage

- Access the Learn module at `http://localhost:5000`
- Access the Understand module at `http://localhost:5001`
- Access the Apply module at `http://localhost:5002`

Use these endpoints to interact with the modules:
- `/start_thread` - Start a new thread with the assistant.
- `/send_message` - Send a message to the assistant.
- `/update_status` - Update the learning status of a term.
- `/get_terms_data` - Retrieve data on total and solved terms.
- `/reset_terms` - Reset all terms to unsolved.
- `/pass_all_terms` - Mark all terms as solved.
- `/get_question` - Retrieve a question for a specific section and term.
- `/get_correct_response` - Get the correct response explanation.
- `/get_incorrect_response` - Get the incorrect response explanation.
- `/update_section` - Update the current section being worked on.
- `/get_remaining_sections` - Get the remaining sections that have not been completed.
- `/retrieve_related_term_response` - Get the response related to a specific term.
- `/get_remaining_terms` - Get the remaining terms in the current section.