from flask import Flask, request, jsonify
from flask_cors import CORS
from openai_integration import run_assistant_query, create_thread

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/start_thread', methods=['POST'])
def start_thread():
    # Create a thread to start a conversation
    thread_id = create_thread()
    return jsonify({"thread_id": thread_id})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    thread_id = data.get('thread_id')
    message_content = data.get('message')

    if not thread_id or not message_content:
        return jsonify({"error": "Invalid request"}), 400

    # Get the assistant's response
    response = run_assistant_query(thread_id, message_content)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Explicitly set host and port
