from pathlib import Path
from firebase_admin_init import storage
from term_manager import TermManager
import os

class UserManager:
    def __init__(self):
        # Dictionary to store term_manager for each user along with the module type
        self.term_managers = {}

    def get_module_name(self, module_type):
        # Get the module_name based on the module type provided in the request
        if module_type == 'learn':
            return 'learn_data'
        elif module_type == 'understand':
            return 'understand_data'
        elif module_type == 'apply':
            return 'apply_data'
        raise ValueError("Module type not recognized. Must be 'learn', 'understand', or 'apply'.")

    def manage_user_json(self, userID, module_name):
        try:
            # Define local directory and file path for storing terms.json in the root directory
            terms_directory = Path(f'{module_name}') / f'{userID}'
            terms_path = terms_directory / 'terms.json'
            terms_directory.mkdir(parents=True, exist_ok=True)
            
            # Create a reference to the file in Firebase Cloud Storage
            blob = storage.bucket().blob(f'{module_name}/{userID}/terms.json')

            if blob.exists():
                # If the file exists in Cloud Storage, download it
                blob.download_to_filename(terms_path)
                print(f'Downloaded {module_name}/{userID}/terms.json to {terms_path}')
            else:
                # If the file does not exist, use the default {module_name}_terms.json file from the root directory
                default_terms_path = Path(f'{module_name}_terms.json')
                if not default_terms_path.exists():
                    print(f"Default {module_name}_terms.json file not found at {default_terms_path}")
                    return None

                # Copy the default {module_name}_terms.json to the user's directory
                with open(default_terms_path, 'r') as default_file:
                    with open(terms_path, 'w') as user_file:
                        user_file.write(default_file.read())

                print(f'Created default {terms_path} from {default_terms_path}')
            
            return terms_path

        except Exception as e:
            print(f"Error managing terms.json for user {userID}: {e}")
            return None

    def initialize_user_session(self, userID, module_type):
        # Initialize the user session and download the terms.json file
        module_name = self.get_module_name(module_type)
        terms_json_path = self.manage_user_json(userID, module_name)
        if not terms_json_path:
            raise Exception(f"Failed to initialize terms.json for user {userID}")

        # Store the term_manager and module type in the dictionary
        self.term_managers[userID] = {
            "term_manager": TermManager(module_name=module_name, userID=userID),
            "module": module_type
        }

    def cleanup_user_session(self, userID):
        # Upload the user's terms.json file back to Cloud Storage and clean up local files
        print("Cleaning up user session...")
        try:
            module_name = self.get_module_name(self.term_managers[userID]["module"])
            
            self.term_managers[userID]["term_manager"].write_terms_to_file()
            terms_directory = Path(f'{module_name}') / f'{userID}'
            terms_path = terms_directory / 'terms.json'

            # Manually create the Cloud Storage path using forward slashes
            cloud_path = f"{module_name}/{userID}/terms.json"

            # Upload the file to Firebase Cloud Storage
            blob = storage.bucket().blob(cloud_path)
            blob.upload_from_filename(str(terms_path))  # Convert to string for uploading the local file
            print(f'Uploaded {terms_path} to Firebase Cloud Storage at {cloud_path}')

            # Clean up the local file after upload
            os.remove(terms_path)
            print(f"Deleted local {terms_path} after uploading")

            # Remove the user from term_managers
            if userID in self.term_managers:
                del self.term_managers[userID]

        except Exception as e:
            print(f"Error cleaning up session for user {userID}: {e}")