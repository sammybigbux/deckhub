import openai
import time
import json
from tqdm import tqdm  # For the progress bar
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Set the assistant ID and API key
assistant_id = "asst_hzPGjoA3p9B6ftcnm2C6yV1A"

# Initialize the OpenAI API client
openai.api_key = api_key
client = openai.OpenAI(api_key=api_key)

def create_thread(client):
    thread = client.beta.threads.create()
    return thread

def add_message(client, thread_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    return message

def create_run(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    return run

def recursive_dict_merge(d1, d2):
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
            recursive_dict_merge(d1[k], v)
        else:
            d1[k] = v

# Validation function to ensure the response includes the required keys
def is_valid_response(response_dict):
    if not response_dict:
        return False

    if len(response_dict) != 1:  # Expecting only one top-level entry
        return False

    category = list(response_dict.keys())[0]
    scenario_content = response_dict[category]

    # Required keys: 'component_concepts', 'specificity', 'questions'
    expected_keys = {"component_concepts", "specificity", "questions"}

    if not set(scenario_content.keys()).issuperset(expected_keys):
        return False

    # Check that 'component_concepts' is a list
    if not isinstance(scenario_content["component_concepts"], list) or not scenario_content["component_concepts"]:
        return False

    # Check that 'specificity' is a string (should be either foundational, intermediate, or special topics)
    if not isinstance(scenario_content["specificity"], str):
        return False

    # Check that 'questions' contains valid question fields
    questions = scenario_content["questions"]
    expected_question_keys = {"question", "option1", "option2", "option3", "option4", "answer"}
    if not isinstance(questions, dict) or not set(questions.keys()).issuperset(expected_question_keys):
        return False

    return True

def send_concepts_to_ai(client, section_name, specificity, concepts, assistant_id):
    # Construct the input format for the assistant
    text_to_send = f"{section_name}\n{specificity}\n" + "\n".join(concepts)

    attempts = 0
    valid_response = False
    response_dict = None

    while attempts < 3 and not valid_response:
        attempts += 1

        # Create a thread
        thread = create_thread(client)

        # Add a message to the thread
        add_message(client, thread.id, text_to_send)

        # Create a run
        run = create_run(client, thread.id, assistant_id)

        # Process the response
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            response_message = [message for message in messages.data if message.role == "assistant"]
            if response_message:
                response = response_message[0].content[0].text.value
                try:
                    response_dict = json.loads(response)
                    if is_valid_response(response_dict):
                        valid_response = True
                    else:
                        print(f"Invalid response structure, retrying ({attempts}/3)...")
                except json.JSONDecodeError:
                    print(f"JSON decode error, retrying ({attempts}/3)...")
            else:
                print("No response from the assistant.")
        else:
            print(f"Run status: {run.status}")

        if not valid_response and attempts == 3:
            print("Failed 3 times, logging to error file.")
            with open('error_log.json', 'a') as error_file:
                error_data = {
                    "section": section_name,
                    "specificity": specificity,
                    "concepts": concepts,
                    "error": f"Failed after 3 attempts"
                }
                json.dump(error_data, error_file, indent=2)
                error_file.write("\n")

        # Sleep for a bit before retrying
        if not valid_response:
            time.sleep(2)

    return response_dict

def process_section(section_name, section_data, merged_data):
    # Iterate through specificity levels (foundational, intermediate, special topics)
    for specificity, concepts in section_data.items():
        print(f"Processing section '{section_name}' with specificity '{specificity}'...")

        # Continue generating questions until all concepts are used
        while concepts:
            response_dict = send_concepts_to_ai(client, section_name, specificity, concepts, assistant_id)
            if response_dict:
                # Extract component_concepts and remove them from the list
                component_concepts = response_dict[list(response_dict.keys())[0]]["component_concepts"]
                concepts = [c for c in concepts if c not in component_concepts]

                # Merge response into the final JSON
                if section_name not in merged_data:
                    merged_data[section_name] = {}
                recursive_dict_merge(merged_data[section_name], response_dict)

def main(file_path, section_name):
    # Load concept_lists.json
    with open(file_path, 'r') as file:
        concept_lists = json.load(file)

    merged_data = {}

    # Check if the section exists in the file
    if section_name not in concept_lists:
        print(f"Section '{section_name}' not found in the concept lists.")
        return

    # Process only the specified section
    process_section(section_name, concept_lists[section_name], merged_data)

    # Write merged data to the output file
    with open(f'questions_{section_name}.json', 'w') as outfile:
        json.dump(merged_data, outfile, indent=2)

    print(f"Processing complete for section '{section_name}'. Merged JSON data has been written to 'questions_{section_name}.json'.")

if __name__ == "__main__":
    file_path = 'concept_lists.json'  # Path to your concept_lists.json file
    section_name = input("Enter the section you want to process (e.g., 'Networking'): ")
    main(file_path, section_name)
