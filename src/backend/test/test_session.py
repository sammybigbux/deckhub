import unittest
import os
import requests
import sys
from pathlib import Path

# Add the directory above 'tests' to sys.path to import firebase_admin_init
sys.path.append(str(Path(__file__).resolve().parent.parent))

if os.getenv('TEST_ENV_URL', 'http://localhost:5000') == 'http://localhost:5000':
    from firebase_admin_init_local import bucket
else:
    from firebase_admin_init_cloud import bucket

class TestEnvManagement(unittest.TestCase):

    def setUp(self):
        """Set up any pre-requisites."""
        # Path to the directory one level above /tests
        self.parent_dir = Path(__file__).resolve().parent.parent

        # Local path setup
        self.userID = "JPqzMvLnJSQvfxw841ibYWDyqVl2"
        self.module_type = "learn"
        self.local_terms_path = self.parent_dir / f"learn_data/{self.userID}/terms.json"
        self.default_terms_path = self.parent_dir / "learn_data_terms.json"
        self.cloud_terms_path = f"learn_data/{self.userID}/terms.json"

        # Backend URL (staging or production) set via environment variable
        self.base_url = os.getenv('TEST_ENV_URL', 'http://localhost:5000')  # Fallback to localhost for local tests

    def test_initialize_and_cleanup_env(self):
        """Test the /initialize_env and /cleanup_env endpoints."""
        
        # --- Test initialize_env ---
        # Check that the terms file does not exist in Firebase Cloud Storage initially
        blob = bucket.blob(self.cloud_terms_path)
        #self.assertFalse(blob.exists(), "Terms file should not exist in Firebase Cloud Storage initially")

        # Check that the default learn_data_terms.json exists locally
        self.assertTrue(self.default_terms_path.exists(), "Default learn_data_terms.json should exist locally")

        # Call the /initialize_env endpoint with the userID and module type
        url = f"{self.base_url}/initialize_env"
        payload = {
            "userID": self.userID,
            "module": self.module_type
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, "Failed to initialize environment")

        # Check that the terms.json file is now created locally
        # TODO make this work with cloud self.assertTrue(self.local_terms_path.exists(), "terms.json should be created locally after initialization")

        # --- Test cleanup_env ---
        # Call the /cleanup_env endpoint with the userID
        url = f"{self.base_url}/cleanup_env"
        payload = {
            "userID": self.userID
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, "Failed to clean up user session")

        # Check that the local terms.json file has been deleted
        # TODO make this work with cloudself.assertFalse(self.local_terms_path.exists(), "terms.json should be deleted locally after cleanup")

        # Check that the terms.json file has been uploaded to Firebase Cloud Storage
        blob = bucket.blob(self.cloud_terms_path)
        self.assertTrue(blob.exists(), "Terms file should be uploaded to Firebase Cloud Storage")

        # Clean up by deleting the cloud file after the test
        blob.delete()
        self.assertFalse(blob.exists(), "Cloud file should be deleted after test")

    def tearDown(self):
        """Clean up any remaining files."""
        # Remove the local file if it exists
        if self.local_terms_path.exists():
            os.remove(self.local_terms_path)

        # Clean up the local directory if it exists and is empty
        if self.local_terms_path.parent.exists() and not os.listdir(self.local_terms_path.parent):
            os.rmdir(self.local_terms_path.parent)

if __name__ == '__main__':
    unittest.main()
