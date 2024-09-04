import json
from google.cloud import firestore
from pathlib import Path
import os

# Set the Google Application Credentials environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\deck_hub\firebase_key.json"
print("Credentials file:", os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))

# Initialize Firestore client
db = firestore.Client(project="deckhubapp", database="awssa003")  # Use "(default)" if 'awssa003' was meant to be the default database

# Path to the JSON file
json_file_path = Path(__file__).parent.parent / "data" / "outputs" / "merged_data.json"

# Name of the collection where the data will be uploaded
collection_name = "apply"

# Load the JSON data
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Upload each top-level key as a separate document in the collection
def upload_to_firestore(data, collection_name):
    collection_ref = db.collection(collection_name)

    # Iterate over each top-level key-value pair in the JSON
    for key, value in data.items():
        # The key will be the document ID, and the value will be the document data
        doc_ref = collection_ref.document(key)
        doc_ref.set(value)
        print(f"Uploaded document '{key}' to collection '{collection_name}'.")

# Perform the upload
upload_to_firestore(data, collection_name)

print(f"All top-level keys from the JSON file have been uploaded as separate documents to the Firestore collection '{collection_name}'.")
