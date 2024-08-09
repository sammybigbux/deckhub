import openai
import time
import json
import re
from tqdm import tqdm  # For the progress bar
from dotenv import load_dotenv
import os
api_key = os.getenv("API_KEY")

# Set the assistant ID and API key
assistant_id = "asst_ZNmKYn4FTAk61RNfFOfPKJ1v"

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
    return lines[:15] if test_mode else lines

def recursive_dict_merge(d1, d2):
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
            recursive_dict_merge(d1[k], v)
        else:
            d1[k] = v

def is_valid_response(response_dict):
    if not response_dict:
        return False
    if len(response_dict) != 1:
        return False
    category = list(response_dict.keys())[0]
    if len(response_dict[category]) != 1:
        return False
    scenario = list(response_dict[category].keys())[0]
    expected_keys = {"question", "option1", "option2", "option3", "option4", "answer"}
    scenario_content = response_dict[category][scenario]
    if set(scenario_content.keys()) != expected_keys:
        return False
    if scenario_content["question"] != scenario:
        return False
    return True

def main(file_path, test_mode=False):
    lines = read_lines(file_path, test_mode)
    total_lines = len(lines)
    merged_data = {}

    print("Starting loop to process lines...")
    with tqdm(total=total_lines, desc="Processing lines") as pbar:
        for i in range(total_lines):
            batch_lines = lines[i:i + 1]
            text_to_send = "\n".join(batch_lines).strip()

            attempts = 0
            valid_response = False
            while attempts < 3 and not valid_response:
                attempts += 1

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
                        try:
                            response_dict = json.loads(response)
                            if is_valid_response(response_dict):
                                recursive_dict_merge(merged_data, response_dict)
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
                    print("Failed 3 times, moving to the next batch.")

                # Sleep for a bit before retrying
                if not valid_response:
                    time.sleep(2)

            # Update the progress bar
            pbar.update(len(batch_lines))

    # Write merged data to the output file
    with open('questions.json', 'w') as outfile:
        json.dump(merged_data, outfile, indent=2)

    print("Processing complete. Merged JSON data has been written to 'questions.json'.")

if __name__ == "__main__":
    file_path = 'corpus_lists.txt'
    test_mode = False  # Change to False to process the whole file
    main(file_path, test_mode)
