import openai
import time
import json
import re
from tqdm import tqdm  # For the progress bar
from dotenv import load_dotenv
import os

# Set the assistant ID and API key
assistant_id = "asst_mFgFyf3ty1axBzVWDnSL5N0p"
api_key = os.getenv("API_KEY")

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

def read_lines(file_path, test_mode=False):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines[:10] if test_mode else lines

def is_valid_response(response_dict):
    if not response_dict:
        print("Validation failed: Response is empty.")
        return False
    if len(response_dict) != 1:
        print(f"Validation failed: Expected 1 top-level key, found {len(response_dict)}.")
        return False
    section = list(response_dict.keys())[0]
    if len(response_dict[section]) != 1:
        print(f"Validation failed: Expected 1 key in section '{section}', found {len(response_dict[section])}.")
        return False
    question = list(response_dict[section].keys())[0]
    if not question.endswith('?'):
        print(f"Validation failed: Question '{question}' does not end with a question mark.")
        return False
    explanation_details = response_dict[section][question]
    if set(explanation_details.keys()) != {"explanation", "elaborate"}:
        print(f"Validation failed: Expected keys 'explanation' and 'elaborate' in question details, found {set(explanation_details.keys())}.")
        return False
    return True

def recursive_dict_merge(d1, d2):
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
            recursive_dict_merge(d1[k], v)
        else:
            d1[k] = v

def main(file_path, test_mode=False):
    lines = read_lines(file_path, test_mode)
    total_lines = len(lines)
    merged_data = {}

    print("Starting loop to process lines...")
    with tqdm(total=total_lines, desc="Processing lines") as pbar:
        for i in range(0, total_lines, 1):
            batch_lines = lines[i:i + 1]
            text_to_send = "\n".join(batch_lines).strip()

            # Create a thread
            print("Creating thread...")
            thread = create_thread(client)

            # Add a message to the thread
            print("Adding message to thread...")
            add_message(client, thread.id, text_to_send)

            # Create a run
            print("Creating run...")
            run = create_run(client, thread.id, assistant_id)

            # Process the response
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                response_message = [message for message in messages.data if message.role == "assistant"]
                if response_message:
                    response = response_message[0].content[0].text.value
                    response_dict = json.loads(response)
                    recursive_dict_merge(merged_data, response_dict)
                else:
                    print("No response from the assistant.")
            else:
                print(f"Run status: {run.status}")

            # Update the progress bar
            pbar.update(len(batch_lines))

    # Write merged data to the output file
    with open('correct_response_api.json', 'w') as outfile:
        json.dump(merged_data, outfile, indent=2)

    print("Processing complete. Merged JSON data has been written to 'correct_response_api.json'.")

if __name__ == "__main__":
    file_path = 'correct_response_lists.txt'
    test_mode = False  # Change to False to process the whole file
    main(file_path, test_mode)
