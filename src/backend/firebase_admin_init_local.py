# firebase_admin_init_local.py

import firebase_admin
from firebase_admin import credentials, firestore, storage
from pathlib import Path

# Since WORKDIR is set to /app, we can use a relative path
service_account_path = Path('firebase_key.json')

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'deckhubapp.appspot.com'
})

# Initialize Firestore and Storage
db = firestore.client()
bucket = storage.bucket()

print("Initialized Firebase using local credentials.")