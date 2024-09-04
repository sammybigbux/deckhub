import firebase_admin
from firebase_admin import credentials, firestore, storage
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
service_account_path = root_dir / 'firebase_key.json'

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'deckhubapp.appspot.com'
})

# Initialize Firestore
db = firestore.client()

# Get 
bucket = storage.bucket()
