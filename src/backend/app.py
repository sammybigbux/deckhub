import os
import json
import time
from functools import lru_cache
from openai import OpenAI
from flask import Flask, request, jsonify, Response, stream_with_context, make_response
from flask_cors import CORS
import openai
import re
from dotenv import load_dotenv
from pathlib import Path
from firebase_admin import firestore, auth
from datetime import datetime, timedelta, timezone
from user_manager import UserManager
from response_event_handler import ResponseEventHandler
import stripe
if os.getenv('TEST_ENV_URL', 'http://localhost:5000') == 'http://localhost:5000':
    from firebase_admin_init_local import db, bucket
else:
    from firebase_admin_init_cloud import db, bucket
api_key = os.environ.get('OPENAI_API_KEY').replace("'", "")
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY').replace("'", "")
webhook_secret = os.environ.get('WEBHOOK_SECRET').replace("'", "")
client = OpenAI(api_key=api_key)
# Define the assistant ID from an environment variable
# This assistant is for answering questions
assistant_id = "asst_dlHW5pVVkce0IWgKZzz77tTm"
def load_json(file_name):
    file_path = Path(file_name)
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        print(f"{file_path} not found.")
        return None
# Load the data
static_data_dir = Path("static_data")
LEARN_DATA = load_json(static_data_dir / 'learn_data.json')
UNDERSTAND_DATA = load_json(static_data_dir / 'understand_data.json')
APPLY_DATA = load_json(static_data_dir / 'apply_data.json')
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'https://deckhubapp.web.app'])
user_manager = UserManager()
def get_data_from_id(userID):
    """Helper function to retrieve the module type from the userID."""
    if userID not in user_manager.term_managers:
        print(f"Can't get module name from id: {userID}")
        return None, jsonify({'error': 'User session not found'}), 404
    module = user_manager.term_managers[userID]['module']
    if module == 'learn':
        return LEARN_DATA
    elif module == 'understand':
        return UNDERSTAND_DATA  
    elif module == 'apply':
        return APPLY_DATA
    else:
        assert False, f"Invalid module type for userID: {userID}, module: {module}"
def get_term_manager(userID):
    """Helper function to retrieve the term_manager for a given userID."""
    if userID not in user_manager.term_managers:
        return None, jsonify({'error': 'User session not found'}), 404
    return user_manager.term_managers[userID]['term_manager'], None, None
# function for error handling
def get_user_id_and_term_manager(data):
    """Helper function to retrieve the userID from the request and the associated term_manager."""
    userID = data.get('userID')
    if not userID:
        return None, jsonify({'error': 'userID is required'}), 400, None
    term_manager, error_response, status_code = get_term_manager(userID)
    if error_response:
        return None, error_response, status_code, None
    return userID, term_manager, None, None
@app.route('/start_thread', methods=['POST'])
def start_thread_endpoint():
    def create_thread():
        thread = client.beta.threads.create()
        return thread.id
    thread_id = create_thread()
    return jsonify({'thread_id': thread_id})
@app.route('/set_assistant_id', methods=['POST'])
def set_assistant_id():
    global assistant_id 
    assistant_id = request.json.get('assistant_id')
    if not assistant_id:
        return jsonify({"error": "Assistant ID is required"}), 400
    # Logic to handle setting the assistant_id goes here
    print(f"Switching to assistant with ID: {assistant_id}")
    return jsonify({"message": f"Switched to assistant with ID: {assistant_id}"}), 200
        
@app.route('/send_message', methods=['GET'])
def send_message_endpoint():
    # Extract thread_id and message from query parameters (GET request)
    thread_id = request.args.get('thread_id')
    message = request.args.get('message')
    print("Message from frontend: ", message)
    def run_assistant_query(thread_id, query):
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        active_runs = [run for run in runs if run.status in ['in_progress', 'requires_action']]
        if active_runs:
            for active_run in active_runs:
                client.beta.threads.runs.terminate(
                    thread_id=thread_id,
                    run_id=active_run.id
                )
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
        return event_handler
    # Stream the assistant response as it's generated
    def event_stream():
        event_handler = run_assistant_query(thread_id, message)
        skip_first_token = True  # Flag to skip the first token
        for token in event_handler.response_text:
            if skip_first_token:
                skip_first_token = False  # Skip the first token
                continue  # Move to the next token without yielding
            # Stream each subsequent token immediately
            yield f"data: {token}\n\n"
        # End the stream with an 'end' event
        yield "event: end\ndata: Stream closed\n\n"
    # Return a streaming response using stream_with_context
    return Response(stream_with_context(event_stream()), content_type='text/event-stream')
@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    if not data or 'term' not in data or 'userID' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    userID = data.get('userID')
    term = data.get('term')
    # Ensure the user has a session initialized
    if userID not in user_manager.term_managers:
        return jsonify({'error': 'User session not found'}), 404
    # Update the status for the term using the user's term_manager
    try:
        term_manager = user_manager.term_managers[userID]['term_manager']
        term_manager.update_status(term)
        return jsonify({'message': f'Status for {term} updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/initialize_env', methods=['POST', 'OPTIONS'])
def initialize_with_user_information():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers["Access-Control-Allow-Origin"] = request.headers.get('Origin')
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response
    # Actual POST request handling
    userID = request.json.get('userID')
    module_type = request.json.get('module')  # Learn, Understand, or Apply
    if not userID or not module_type:
        return jsonify({"error": "No user information or module provided"}), 400
    
    try:
        # Initialize the session for the user with the given module type
        user_manager.initialize_user_session(userID, module_type)
        return jsonify({"message": "Environment initialized successfully"}), 200
    except Exception as e:
        print("Error initializing environment: ", e)
        return jsonify({"error": str(e)}), 500
@app.route('/cleanup_env', methods=['POST'])
def cleanup_user_session():
    if request.is_json:
        userID = request.json.get('userID')  # Handle JSON payload from fetch()
    else:
        data = request.data.decode('utf-8')  # Decode the blob data from sendBeacon
        userID = json.loads(data).get('userID')  # Parse the JSON string
    if not userID:
        return jsonify({"error": "No user information provided"}), 400
    try:
        user_manager.cleanup_user_session(userID)
        return jsonify({"message": "User session cleaned up successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/get_terms_data', methods=['POST'])
def get_terms_data():
    data = request.json
    userID = data.get('userID')
    if not userID:
        return jsonify({'error': 'userID is required'}), 400
    term_manager, error_response, status_code = get_term_manager(userID)
    if error_response:
        return error_response, status_code
    total_terms = term_manager.get_total_terms()
    solved_terms = term_manager.get_solved_terms()
    return jsonify({'totalTerms': total_terms, 'solvedTerms': solved_terms})
@app.route('/reset_terms', methods=['POST'])
def reset_terms():
    data = request.json
    userID = data.get('userID')
    if not userID:
        return jsonify({'error': 'userID is required'}), 400
    term_manager, error_response, status_code = get_term_manager(userID)
    if error_response:
        return error_response, status_code
    term_manager.reset_all_terms()
    return jsonify({'message': 'All terms reset successfully'})
@app.route('/pass_all_terms', methods=['POST'])
def pass_all_terms():
    data = request.json
    userID = data.get('userID')
    if not userID:
        return jsonify({'error': 'userID is required'}), 400
    term_manager, error_response, status_code = get_term_manager(userID)
    if error_response:
        return error_response, status_code
    term_manager.pass_all_terms()
    return jsonify({'message': 'All terms passed successfully'})
@app.route('/get_question', methods=['POST'])
def get_question():
    data = request.json
    userID = data.get('userID')
    if not userID:
        return jsonify({'error': 'userID is required'}), 400
    term_manager, error_response, status_code = get_term_manager(userID)
    if error_response:
        return error_response, status_code
    section = term_manager.section
    term = data.get('term')
    
    question_dict = term_manager.retrieve_question(get_data_from_id(userID), section, term)
    return jsonify(question_dict)
@app.route('/get_correct_response', methods=['POST'])
def get_correct_response():
    data = request.json
    userID, term_manager, error_response, status_code = get_user_id_and_term_manager(data)
    if error_response:
        return error_response, status_code
    term = data.get('term')
    response = term_manager.get_correct_response(get_data_from_id(userID), term)
    return jsonify({'explanation': response.get('explanation'), 'elaborate': response.get('elaborate')}), 200
@app.route('/get_incorrect_response', methods=['POST'])
def get_incorrect_response():
    data = request.json
    userID, term_manager, error_response, status_code = get_user_id_and_term_manager(data)
    if error_response:
        return error_response, status_code
    term = data.get('term')
    userAnswer = data.get('userAnswer')
    response = term_manager.get_incorrect_response(get_data_from_id(userID), term, userAnswer)
    return jsonify({'explanation': response.get('explanation'), 'elaborate': response.get('elaborate')}), 200
@app.route('/update_section', methods=['POST'])
def update_section_endpoint():
    data = request.json
    userID, term_manager, error_response, status_code = get_user_id_and_term_manager(data)
    if error_response:
        return error_response, status_code
    term_manager.section = data['section'].capitalize()
    return jsonify({'message': f"Section updated to {term_manager.section}"}), 200
@app.route('/get_remaining_sections', methods=['POST'])
def get_remaining_sections():
    data = request.json
    userID, term_manager, error_response, status_code = get_user_id_and_term_manager(data)
    if error_response:
        return error_response, status_code
    remaining_sections = term_manager.get_remaining_sections()
    return jsonify({'message': f"Sure, here are the remaining sections:\n{remaining_sections}"}), 200
@app.route('/retrieve_related_term_response', methods=['POST'])
def get_related_term_response():
    data = request.get_json()
    userID, term_manager, error_response, status_code = get_user_id_and_term_manager(data)
    if error_response:
        return error_response, status_code
    term = data.get('term')
    related_term = data.get('related_term')
    
    if term and related_term:
        try:
            response = term_manager.get_rt_response(get_data_from_id(userID), term, related_term)
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
    data = request.json
    userID, term_manager, error_response, status_code = get_user_id_and_term_manager(data)
    if error_response:
        return error_response, status_code
    remaining_terms = term_manager.get_remaining_terms()
    return jsonify({'message': f"Sure, here are the remaining terms:\n{remaining_terms}"}), 200
# The below endpoints are mainly for interacting with firebase for the purpose of the rest of the website (not the chat part)
@app.route('/create_user_if_not_exists', methods=['POST'])
def create_user_if_not_exists():
    print("Function called: /create_user_if_not_exists")
    
    # Try to retrieve the request data and authorization header
    data = request.json
    print(f"Request data: {data}")
    auth_header = request.headers.get('Authorization')
    print(f"Authorization header: {auth_header}")
    if not auth_header:
        print("Authorization header is missing")
        return jsonify({"error": "Authorization header is missing"}), 400
    try:
        # Extract and verify the ID token
        id_token = auth_header.split('Bearer ')[1]
        print(f"ID Token: {id_token}")
        decoded_token = auth.verify_id_token(id_token)
        print(f"Decoded token: {decoded_token}")
        user_id = decoded_token['uid']
        print(f"User ID from decoded token: {user_id}")
        display_name = data.get('display_name', '')
        email = data.get('email', '')
        print(f"Display name: {display_name}, Email: {email}")
        user_id = data.get('user_id', user_id)
        print(f"Final user ID: {user_id}")
        # Check if user exists in Firestore
        user_ref = db.collection('users').document(user_id)
        print(f"User reference object: {user_ref}")
        # Wrap the Firestore access in a try-except block for better error handling
        try:
            # Get the document and check if it exists
            user_doc = user_ref.get()
            if not user_doc.exists:
                # User does not exist, create a new Stripe customer and Firestore user
                print("User does not exist. Creating new user.")
                
                # Create a new Stripe customer
                customer = stripe.Customer.create(
                    email=email,
                    metadata={'user_id': user_id}
                )
                print(f"Stripe customer created: {customer}")
                # Create a new user document in Firestore
                user_ref.set({
                    'displayName': display_name,
                    'decks_owned': [],
                    'email': email,
                    'stripe_customer_id': customer['id'],
                    'user_id': user_id
                })
                print(f"User created in Firestore: {user_id}")
                return jsonify({
                    "message": "New user created in Firestore!",
                    "stripe_customer_id": customer['id']
                }), 200
            else:
                # User already exists, fetch the stripe_customer_id from the document
                stripe_customer_id = user_doc.get('stripe_customer_id')
                print(f"User already exists. Stripe customer ID: {stripe_customer_id}")
                return jsonify({
                    "message": "User already exists in Firestore.",
                    "stripe_customer_id": stripe_customer_id
                }), 200
        except Exception as firestore_error:
            print(f"Error accessing Firestore document: {firestore_error}")
            return jsonify({"error": "Failed to access Firestore document"}), 500
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500
# endpoints for search page
@app.route('/get_decks', methods=['GET'])
def get_decks():
    try:
        decks_ref = db.collection('decks')
        docs = decks_ref.stream()
        decks = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            data['lastUpdated'] = data['lastUpdated'].isoformat()  # Convert timestamp to ISO 8601 string
            decks.append(data)
        return jsonify(decks), 200
    except Exception as e:
        print(f"Error fetching decks: {e}")
        return jsonify({"error": "Failed to fetch decks"}), 500
@app.route('/get_user_decks', methods=['POST'])
def get_user_decks():
    id_token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        # Fetch and return the user's decks from Firestore
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            return jsonify(user_doc.to_dict().get('decks_owned', [])), 200
        else:
            return jsonify([]), 404
    except Exception as e:
        print(f"Error verifying ID token or fetching user decks: {e}")
        return jsonify({"error": "Failed to verify token or fetch user decks"}), 401
# endpoints for bounty page
@app.route('/submit_request', methods=['POST'])
def submit_request():
    data = request.json
    user_id = data.get('user_id')
    text = data.get('text')
    # Check if the user has submitted a request in the last 15 minutes
    fifteen_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=15)
    requests_ref = db.collection('requests')
    query = requests_ref.where('subscribers', 'array_contains', user_id).where('timestamp', '>=', fifteen_minutes_ago)
    docs = query.stream()
    if any(docs):
        return jsonify({"error": "You can only submit one request every 15 minutes."}), 400
    # Add the new request to Firestore
    request_data = {
        "upvotes": 1,
        "solved": False,
        "text": text,
        "subscribers": [user_id],
        "timestamp": datetime.now(timezone.utc)
    }
    requests_ref.add(request_data)
    return jsonify({"message": "Request submitted successfully."}), 200
@app.route('/fetch_requests', methods=['GET'])
def fetch_requests():
    try:
        requests_ref = db.collection('requests')
        docs = requests_ref.stream()
        requests = [{"id": doc.id, **doc.to_dict()} for doc in docs]
        requests.sort(key=lambda r: r['upvotes'], reverse=True)
        return jsonify(requests), 200
    except Exception as e:
        print(f"Error fetching requests: {e}")
        return jsonify({"error": "Failed to fetch requests"}), 500
@app.route('/toggle_upvote', methods=['POST'])
def toggle_upvote():
    data = request.json
    request_id = data.get('request_id')
    user_id = data.get('user_id')
    request_ref = db.collection('requests').document(request_id)
    request_doc = request_ref.get()
    if not request_doc.exists:
        return jsonify({"error": "Request not found."}), 404
    request_data = request_doc.to_dict()
    if user_id in request_data['subscribers']:
        request_data['upvotes'] -= 1
        request_data['subscribers'].remove(user_id)
    else:
        request_data['upvotes'] += 1
        request_data['subscribers'].append(user_id)
    request_ref.update(request_data)
    return jsonify({"message": "Upvote toggled successfully."}), 200
# This section is for endpoints related to payment processing using Stripe. 
# The first endpoint creates a new Stripe Checkout session, and the second endpoint handles the webhook event when a payment is completed. 
# The webhook endpoint is used to update the user's data in the backend after a successful payment.
@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    try:
        # Use the Stripe customer ID from the request
        stripe_customer_id = data['stripe_customer_id']  # The Stripe customer ID from the frontend
        # Create a new Stripe Checkout session
        session = stripe.checkout.Session.create(
            customer=stripe_customer_id,  # Ensure the session is tied to the correct Stripe customer
            payment_method_types=['card'],
            line_items=[
                {
                    'price': data['price_id'],  # Use the price_id from Stripe
                    'quantity': 50,
                },
            ],
            mode='payment',
            success_url='http://localhost:5173/payment-success',
            cancel_url='http://localhost:5173/search',
            metadata={
                'user_id': data['user_id'],  # Firebase user ID
                'product_name': data['product_name']  # Pass product name (or ID) for use in the webhook
            }
        )
        # Return the session ID to the client
        return jsonify({'id': session.id})
    
    except Exception as e:
        return jsonify(error=str(e)), 403
@app.route('/webhook', methods=['POST'])
def webhook_received():
    event = None
    payload = request.data.decode('utf-8')
    sig_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        return 'Invalid signature', 400
    # Handle the event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Retrieve the Stripe customer ID from the session
        stripe_customer_id = session['customer']
        # Retrieve the customer metadata (which contains the Firebase user_id)
        customer = stripe.Customer.retrieve(stripe_customer_id)
        user_id = customer.metadata['user_id']  # Firebase user ID
        # Retrieve product information from the session
        product_name = session['metadata']['product_name']  # Ensure this is passed during checkout session creation
        # Now you have the user_id and the product_name, so update Firebase
        db = firestore.client()
        # Get the user's document reference
        user_ref = db.collection('users').document(user_id)
        # Update the decks_owned array
        user_ref.update({
            'decks_owned': firestore.ArrayUnion([product_name])
        })
        print(f"Product {product_name} added to user {user_id}'s decks_owned")
    return 'Success', 200
if __name__ == '__main__':
    if os.getenv('TEST_ENV_URL', 'http://localhost:5000') == 'http://localhost:5000':
        app.run(host='localhost', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)
