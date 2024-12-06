import firebase_admin
from firebase_admin import credentials, firestore, storage
from google.cloud import secretmanager
import os
import json

def access_secret_version(secret_id="DECKHUB_FIREBASE_KEY", version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    project_id = 'deckhubapp'
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

# Fetch Firebase credentials from Secret Manager
firebase_key_json = access_secret_version()

# Initialize Firebase Admin SDK with credentials from Secret Manager
cred = credentials.Certificate(json.loads(firebase_key_json))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'deckhubapp.appspot.com'
})

# Initialize Firestore and Storage
db = firestore.client()
bucket = storage.bucket()
