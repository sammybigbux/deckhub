import os
import json
import time
import threading
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
from term_manager import TermManager  # Assuming the TermManager is in term_manager.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import re
from dotenv import load_dotenv
import os
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# Define the assistant ID from an environment variable
assistant_id = "asst_dlHW5pVVkce0IWgKZzz77tTm"

term_manager = TermManager('terms.json')

def create_thread():
    start_time = time.time()
    thread = client.beta.threads.create()
    print(f"create_thread took {time.time() - start_time} seconds")
    return thread.id

class ResponseEventHandler(AssistantEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_text = []

    def _get_related_Terms(self):
        return 

    @override
    def on_text_created(self, text) -> None:
        self.response_text.append(text.value)

    @override
    def on_text_delta(self, delta, snapshot):
        self.response_text.append(delta.value)

    def get_response(self):
        full_response = ''.join(self.response_text)
        return full_response


def run_assistant_query(thread_id, query):
    start_time = time.time()
    runs = client.beta.threads.runs.list(thread_id=thread_id)
    active_runs = [run for run in runs if run.status in ['in_progress', 'requires_action']]
    if active_runs:
        terminate_start_time = time.time()
        for active_run in active_runs:
            client.beta.threads.runs.terminate(
                thread_id=thread_id,
                run_id=active_run.id
            )
        print(f"Terminate active runs took {time.time() - terminate_start_time} seconds")

    create_message_start_time = time.time()
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query,
    )
    print(f"Create message took {time.time() - create_message_start_time} seconds")

    event_handler = ResponseEventHandler()

    stream_run_start_time = time.time()
    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=event_handler
    ) as stream:
        stream.until_done()
    print(f"Stream run took {time.time() - stream_run_start_time} seconds")

    return event_handler.get_response()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/start_thread', methods=['POST'])
def start_thread_endpoint():
    start_time = time.time()
    thread_id = create_thread()
    print(f"start_thread_endpoint took {time.time() - start_time} seconds")
    return jsonify({'thread_id': thread_id})

@app.route('/send_message', methods=['POST'])
def send_message_endpoint():
    start_time = time.time()
    data = request.json
    thread_id = data['thread_id']
    message = data['message']
    response = run_assistant_query(thread_id, message)

    response_data = {'response': response}

    return jsonify(response_data)

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    if not data or 'term' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    term = data.get('term')
    # Assuming term_manager.update_status(term) is a function that updates the status
    term_manager.update_status(term)
    
    return jsonify({'message': f'Status for {term} updated successfully'}), 200

@app.route('/get_terms_data', methods=['GET'])
def get_terms_data():
    start_time = time.time()
    total_terms = term_manager.get_total_terms()
    solved_terms = term_manager.get_solved_terms()
    print(f"get_terms_data took {time.time() - start_time} seconds")
    return jsonify({'totalTerms': total_terms, 'solvedTerms': solved_terms})

@app.route('/reset_terms', methods=['POST'])
def reset_terms():
    start_time = time.time()
    term_manager.reset_all_terms()
    print(f"reset_terms took {time.time() - start_time} seconds")
    return jsonify({'message': 'All terms reset successfully'})

@app.route('/pass_all_terms', methods=['POST'])
def pass_all_terms():
    start_time = time.time()
    term_manager.pass_all_terms()
    print(f"pass_all_terms took {time.time() - start_time} seconds")
    return jsonify({'message': 'All terms passed successfully'})

@app.route('/get_question', methods=['POST'])
def get_question():
    data = request.json
    section = term_manager.section
    term = data.get('term')
    print("Now in get_question() with section: ", section, " and term: ", term)
    # Retrieve the question data from the term manager
    question_dict = term_manager.retrieve_question(section, term)

    # Add a message to the thread without waiting for a response
    thread_id = data['thread_id']
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"Question data: {question_dict}"
    )
    print("Returned question data from API is ", question_dict)
    # Convert the dictionary to a string form and return it
    return jsonify(question_dict)

@app.route('/get_correct_response', methods=['POST'])
def get_correct_response():
    data = request.json
    term = data.get('term')
    response = term_manager.get_correct_response(term)
    print(f"Response from get_correct_response: {response}")
    return jsonify({'explanation': response.get('explanation'), 'elaborate': response.get('elaborate')}), 200

@app.route('/get_incorrect_response', methods=['POST'])
def get_incorrect_response():
    data = request.json
    term = data.get('term')
    userAnswer = data.get('userAnswer')
    response = term_manager.get_incorrect_response(term, userAnswer)
    print(f"Response from get_incorrect_response: {response}")
    return jsonify({'explanation': response.get('explanation'), 'elaborate': response.get('elaborate')}), 200

@app.route('/update_section', methods=['POST'])
def update_section_endpoint():
    data = request.json
    term_manager.section = data['section'].capitalize()
    print("Changed section to ", term_manager.section)
    return jsonify({'message': f"Sure, here are the remaining sections {term_manager.section}"}), 200

@app.route('/get_remaining_sections', methods=['POST'])
def get_remaining_sections():
    return jsonify({'message': f"Sure, here are the remaining sections:\n{term_manager.get_remaining_sections()}"}), 200

@app.route('/retrieve_related_term_response', methods=['POST'])
def get_related_term_response():
    # Extract the request body
    data = request.get_json()
    term = data.get('term')
    related_term = data.get('related_term')

    if term and related_term:
        try:
            # Get the related term response from term_manager
            response = term_manager.get_rt_response(term, related_term)
            
            # Check if the response is valid
            if response:
                return jsonify({
                    'related_term_definition': response.get('definition'),
                    'related_term_explanation': response.get('connection')
                }), 200
            else:
                return jsonify({'error': 'No related term response found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid request. Both term and related_term are required.'}), 400

@app.route('/get_remaining_terms', methods=['POST'])
def get_remaining_terms():
    print(f"Remaining terms returned by /get_remaining_terms: {term_manager.get_remaining_terms()}")
    return jsonify({'message': f"Sure, here are the remaining terms:\n{term_manager.get_remaining_terms()}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)