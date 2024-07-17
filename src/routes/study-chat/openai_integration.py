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

# Set your OpenAI API key from an environment variable
api_key = ""  # Use environment variable for security
client = OpenAI(api_key=api_key)

# Define the assistant ID from an environment variable
assistant_id = ""

term_manager = TermManager('terms_fixed.json')

def create_thread():
    start_time = time.time()
    thread = client.beta.threads.create()
    print(f"create_thread took {time.time() - start_time} seconds")
    return thread.id

class ResponseEventHandler(AssistantEventHandler):
    question_data = None  # Class variable to store question data

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

    @override
    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []
        ResponseEventHandler.question_data = "None"
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "update_status":
                arguments = json.loads(tool.function.arguments)
                section = arguments["section"].capitalize()
                term = arguments["term"]
                passed = arguments["passed"]
                term_manager.update_status(section, term, passed)
                update_status_called = True  # Set the flag to True when update_status is called
                tool_outputs.append({"tool_call_id": tool.id, "output": "Status updated"})
            # elif tool.function.name == "update_section":
            #     arguments = json.loads(tool.function.arguments)
            #     term_manager.section = arguments["section"].capitalize()
            # elif tool.function.name == "get_remaining_sections":
            #     remaining_sections = term_manager.get_remaining_sections()
            #     tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(remaining_sections)})  # Convert list to JSON string
            # elif tool.function.name == "get_remaining_terms":
            #     remaining_terms = term_manager.get_remaining_terms(tool.function.arguments)
            #     tool_outputs.append({"tool_call_id": tool.id, "output": json.dumps(remaining_terms)})  # Convert list to JSON string
            # elif tool.function.name == "retrieve_question":
            #     arguments = json.loads(tool.function.arguments)
            #     section = arguments["section"].capitalize()

            #     question_dict = term_manager.retrieve_question(section)
            #     question = question_dict["question"]
            #     term = question_dict["term"]
            #     option1 = question_dict["option1"]
            #     option2 = question_dict["option2"]
            #     option3 = question_dict["option3"]
            #     option4 = question_dict["option4"]
            #     answer = question_dict["answer"]
            #     ResponseEventHandler.question_data = {
            #         "section": section,
            #         "term": term,
            #         "question": question,
            #         "options": [option1, option2, option3, option4],
            #         "related_terms": term_manager.related_terms[section][term],
            #         "answer": answer
            #     }
            #     json_data = json.dumps(ResponseEventHandler.question_data)  # Ensure it's a string
            #     tool_outputs.append({"tool_call_id": tool.id, "output": json_data})
        start_time = time.time()
        self.submit_tool_outputs(tool_outputs, run_id)
        print(f"handle_requires_action took {time.time() - start_time} seconds")

    def submit_tool_outputs(self, tool_outputs, run_id):
        start_time = time.time()
        with client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=ResponseEventHandler(),  # Create a new instance without passing question_data
        ) as stream:
            for text in stream.text_deltas:
                self.response_text.append(text)
        print(f"submit_tool_outputs took {time.time() - start_time} seconds")

    def get_response(self):
        start_time = time.time()
        full_response = ''.join(self.response_text)
        if not full_response and ResponseEventHandler.question_data:
            # If no full_response, use the question data
            full_response = json.dumps(ResponseEventHandler.question_data)
        print(f"get_response took {time.time() - start_time} seconds")
        return full_response

update_status_called = False  # Add a flag to track when update_status is called

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

    print(f"HERE IS THE RESPONSE: {response}")

    # Replace these conditions with something better
    response = response.replace("CorrectCorrect", "Correct")
    response = response.replace("NotNot", "Not")

    print(f"HERE IS THE RESPONSE AFTER EDITING: {response}")

    print(f"send_message_endpoint took {time.time() - start_time} seconds")
    return jsonify(response_data)

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

@app.route('/update_section', methods=['POST'])
def update_section_endpoint():
    data = request.json
    term_manager.section = data['section'].capitalize()
    print("Changed section to ", term_manager.section)
    return jsonify({'message': f"Sure, here are the remaining sections {term_manager.section}"}), 200

@app.route('/get_remaining_sections', methods=['POST'])
def get_remaining_sections():
    return jsonify({'message': f"Sure, here are the remaining sections:\n{term_manager.get_remaining_sections()}"}), 200

@app.route('/get_remaining_terms', methods=['POST'])
def get_remaining_terms():
    print(f"Remaining terms returned by /get_remaining_terms: {term_manager.get_remaining_terms()}")
    return jsonify({'message': f"Sure, here are the remaining terms:\n{term_manager.get_remaining_terms()}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)