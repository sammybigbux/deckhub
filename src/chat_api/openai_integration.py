import os
import json
import time
from functools import lru_cache
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
from term_manager import TermManager  # Assuming the TermManager is in term_manager.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# Define the assistant ID from an environment variable
assistant_id = "asst_dlHW5pVVkce0IWgKZzz77tTm"

def create_term_manager(port):
    if port == 5000:
        data_dir = "learn_data"
    elif port == 5001:
        data_dir = "understand_data"
    elif port == 5002:
        data_dir = "apply_data"
    else:
        raise ValueError("Port number not recognized for any module.")
    return TermManager('terms_fixed.json', data_dir)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.before_first_request
def setup_term_manager():
    global term_manager
    port = request.environ['SERVER_PORT']
    term_manager = create_term_manager(int(port))

def create_thread():
    start_time = time.time()
    thread = client.beta.threads.create()
    print(f"create_thread took {time.time() - start_time} seconds")
    return thread.id

class ResponseEventHandler(AssistantEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_text = []

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

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query,
    )

    event_handler = ResponseEventHandler()

    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        event_handler=event_handler
    ) as stream:
        stream.until_done()

    return event_handler.get_response()

@app.route('/start_thread', methods=['POST'])
def start_thread_endpoint():
    thread_id = create_thread()
    return jsonify({'thread_id': thread_id})

@app.route('/send_message', methods=['POST'])
def send_message_endpoint():
    data = request.json
    thread_id = data['thread_id']
    message = data['message']
    response = run_assistant_query(thread_id, message)
    return jsonify({'response': response})

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    if not data or 'term' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    term = data.get('term')
    term_manager.update_status(term)
    return jsonify({'message': f'Status for {term} updated successfully'}), 200

@app.route('/get_terms_data', methods=['GET'])
def get_terms_data():
    total_terms = term_manager.get_total_terms()
    solved_terms = term_manager.get_solved_terms()
    return jsonify({'totalTerms': total_terms, 'solvedTerms': solved_terms})

@app.route('/reset_terms', methods=['POST'])
def reset_terms():
    term_manager.reset_all_terms()
    return jsonify({'message': 'All terms reset successfully'})

@app.route('/pass_all_terms', methods=['POST'])
def pass_all_terms():
    term_manager.pass_all_terms()
    return jsonify({'message': 'All terms passed successfully'})

@app.route('/get_question', methods=['POST'])
def get_question():
    data = request.json
    section = term_manager.section
    term = data.get('term')
    question_dict = term_manager.retrieve_question(section, term)
    return jsonify(question_dict)

@app.route('/get_correct_response', methods=['POST'])
def get_correct_response():
    data = request.json
    term = data.get('term')
    response = term_manager.get_correct_response(term)
    return jsonify({'explanation': response.get('explanation'), 'elaborate': response.get('elaborate')}), 200

@app.route('/get_incorrect_response', methods=['POST'])
def get_incorrect_response():
    data = request.json
    term = data.get('term')
    userAnswer = data.get('userAnswer')
    response = term_manager.get_incorrect_response(term, userAnswer)
    return jsonify({'explanation': response.get('explanation'), 'elaborate': response.get('elaborate')}), 200

@app.route('/update_section', methods=['POST'])
def update_section_endpoint():
    data = request.json
    term_manager.section = data['section'].capitalize()
    return jsonify({'message': f"Sure, here are the remaining sections {term_manager.section}"}), 200

@app.route('/get_remaining_sections', methods=['POST'])
def get_remaining_sections():
    return jsonify({'message': f"Sure, here are the remaining sections:\n{term_manager.get_remaining_sections()}"}), 200

@app.route('/retrieve_related_term_response', methods=['POST'])
def get_related_term_response():
    data = request.get_json()
    term = data.get('term')
    related_term = data.get('related_term')
    if term and related_term:
        try:
            response = term_manager.get_rt_response(term, related_term)
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
    return jsonify({'message': f"Sure, here are the remaining terms:\n{term_manager.get_remaining_terms()}"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
