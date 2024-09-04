from flask import Flask, request, jsonify
from firebase_admin_init import db
from firebase_admin import firestore, auth
from datetime import datetime, timedelta, timezone
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# endpoint for creating new user
@app.route('/create_user_if_not_exists', methods=['POST'])
def create_user_if_not_exists():
    data = request.json
    id_token = request.headers.get('Authorization').split('Bearer ')[1]

    try:
        # Verify the ID token and get the user's UID
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        display_name = data.get('display_name', '')

        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            # Create a new user document in Firestore
            user_ref.set({
                'displayName': display_name,
                'decks_owned': []  # Initialize with an empty array
            })
            return jsonify({"message": "New user created in Firestore!"}), 200
        else:
            return jsonify({"message": "User already exists in Firestore."}), 200

    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user"}), 500


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
    print(request)
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

if __name__ == '__main__':
    app.run(debug=True)
