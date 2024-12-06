import openai
import time
import json
from tqdm import tqdm  # For progress bar
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = 'asst_DAZQyawIvUMCFxSjCy3XA4p5'

# Initialize OpenAI API client
openai.api_key = api_key
client = openai.OpenAI(api_key=api_key)

def create_thread(client):
    """Create a new thread."""
    return client.beta.threads.create()

def add_message(client, thread_id, content):
    """Add a message to the thread."""
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def create_run(client, thread_id, assistant_id):
    """Create and poll a run."""
    return client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

def recursive_dict_merge(d1, d2):
    """Merge two dictionaries recursively."""
    for key, value in d2.items():
        if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
            recursive_dict_merge(d1[key], value)
        else:
            d1[key] = value

def send_concepts_to_ai(client, section_name, batch, all_terms, assistant_id):
    """Send a batch of concepts and all section terms to ChatGPT."""
    # Construct the input message
    text_to_send = (
        f"Section: {section_name}\n\n"
        f"Concepts to analyze:\n" + "\n".join(batch) + "\n\n"
        f"Relevant terms from the section:\n" + "\n".join(all_terms)
    )

    attempts = 0
    valid_response = False
    response_dict = None

    while attempts < 3 and not valid_response:
        attempts += 1

        thread = create_thread(client)
        add_message(client, thread.id, text_to_send)
        run = create_run(client, thread.id, assistant_id)

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            response_message = [msg for msg in messages.data if msg.role == "assistant"]
            if response_message:
                response = response_message[0].content[0].text.value
                try:
                    response_dict = json.loads(response)
                    valid_response = True
                except json.JSONDecodeError:
                    print(f"JSON decode error, retrying ({attempts}/3)...")
            else:
                print("No response from the assistant.")
        else:
            print(f"Run status: {run.status}")

        if not valid_response:
            time.sleep(2)

    return response_dict

def process_section(section_name, concepts, all_terms, merged_data):
    """Process a section by sending batches of concepts and relevant terms."""
    print(f"Processing section '{section_name}'...")

    while concepts:
        batch = concepts[:5]  # Take up to 5 concepts
        concepts = concepts[5:]  # Remove processed concepts

        response_dict = send_concepts_to_ai(client, section_name, batch, all_terms, assistant_id)
        if response_dict:
            if section_name not in merged_data:
                merged_data[section_name] = {}
            recursive_dict_merge(merged_data[section_name], response_dict)

def main(concepts_file, terms_file):
    """Main function to process sections and save the results."""
    with open(concepts_file, 'r') as f:
        concepts_data = json.load(f)

    with open(terms_file, 'r') as f:
        terms_data = json.load(f)

    merged_data = {}

    for section_name, section_concepts in concepts_data.items():
        if section_name in terms_data:
            all_terms = list(terms_data[section_name].keys())
            concept_list = list(section_concepts.keys())
            process_section(section_name, concept_list, all_terms, merged_data)
        else:
            print(f"Warning: No terms found for section '{section_name}'.")

    with open('concept_terms_mapping.json', 'w') as outfile:
        json.dump(merged_data, outfile, indent=2)

    print("Processing complete. Results saved to 'concept_terms_mapping.json'.")

if __name__ == "__main__":
    concepts_file = 'terms_concepts.json'
    terms_file = 'terms.json'
    main(concepts_file, terms_file)
