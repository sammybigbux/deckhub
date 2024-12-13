from pathlib import Path
from term_manager import TermManager
import os

if os.getenv('TEST_ENV_URL', 'http://localhost:5000') == 'http://localhost:5000':
    from firebase_admin_init_local import storage
else:
    from firebase_admin_init_cloud import storage

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
            # Define the directory for storing both files
            user_directory = Path(f'{userID}')
            user_directory.mkdir(parents=True, exist_ok=True)

            # Define file paths
            files = [f"{module_name}_terms.json", f'hierarchy.json']
            local_paths = {file: user_directory / file for file in files}

            # Process each file (terms.json and hierarchy.json)
            for file_name, local_path in local_paths.items():
                # Reference the file in Firebase Cloud Storage
                blob = storage.bucket().blob(f'{userID}/{file_name}')

                if blob.exists():
                    # Download the file if it exists in Cloud Storage
                    blob.download_to_filename(local_path)
                    print(f"{file_name} exists in the cloud so downloading it from cloud")
                    print(f'Downloaded {userID}/{file_name} to {local_path}')
                else:
                    # Determine the default path based on the file name
                    print(f"{file_name} does not exist in the cloud so using the default")
                    if file_name == f'hierarchy.json':
                        # Default hierarchy.json in the root directory
                        default_path = Path('hierarchy.json')
                    else:
                        # Default terms.json follows {module_name}_terms.json naming
                        default_path = Path(f'{file_name}')

                    # Check if the default file exists
                    if not default_path.exists():
                        print(f"Default {default_path} not found.")
                        return None

                    # Copy the default version to the user's directory
                    with open(default_path, 'r') as default_file:
                        with open(local_path, 'w') as user_file:
                            user_file.write(default_file.read())

                    print(f'Created default {local_path} from {default_path}')

            return local_paths  # Return paths to both files

        except Exception as e:
            print(f"Error managing JSON files for user {userID}: {e}")
            return None
        
    def reset_user_progress(self, userID):
        for filename in ['apply_data_terms.json', 'hierarchy.json']:
            blob = storage.bucket().blob(f'{userID}/{filename}')
            if blob.exists():
                blob.delete()
                print(f"File {filename} for user {userID} has been successfully removed.")
            else:
                print(f"File {filename} for user {userID} does not exist and cannot be removed.")


    def initialize_user_session(self, userID, module_type):
        # Initialize the user session and download the terms.json file
        module_name = self.get_module_name(module_type)
        if userID in self.term_managers and self.term_managers[userID]["module"] == module_type:
            print(f"User {userID} already has a session running")
        else:
            print(f"Getting module name: {module_name} for user {userID}")
            print(f"About to call manage_user_json for user {userID} and module {module_name}")
            json_path_dict = self.manage_user_json(userID, module_name)
            if f"{module_name}_terms.json" not in json_path_dict or f"hierarchy.json" not in json_path_dict:
                raise Exception(f"Failed to initialize {module_name}_terms.json or hierarchy.json for user {userID}")

            # Store the term_manager and module type in the dictionary
            self.term_managers[userID] = {
                "term_manager": TermManager(module_name=module_name, userID=userID),
                "module": module_type
            }

    def cleanup_user_session(self, userID):
        print("Cleaning up user session...")
        try:
            # Get the module name and user directory
            module_name = self.get_module_name(self.term_managers[userID]["module"])
            user_directory = Path(f'{userID}')

            # Write changes to both terms.json and hierarchy.json
            section_progress = self.term_managers[userID]["term_manager"].write_terms_to_file()
            print(f"Section progress within user_manager.cleanup_user_session after calling write_terms_to_file: {section_progress}")
            self.term_managers[userID]["term_manager"].submit_hierarchy_changes()

            # Define the files to process
            files = [f'{module_name}_terms.json', f'hierarchy.json']

            # Loop over both files to upload and clean up
            for file_name in files:
                local_path = user_directory / file_name
                cloud_path = f"{userID}/{file_name}"

                if local_path.exists():
                    # Upload the file to Firebase Cloud Storage
                    blob = storage.bucket().blob(cloud_path)
                    blob.upload_from_filename(str(local_path))
                    print(f'Uploaded {local_path} to Firebase Cloud Storage at {cloud_path}')

                    # Clean up the local file after upload
                    os.remove(local_path)
                    print(f"Deleted local {local_path} after uploading")
                else:
                    print(f"Local {local_path} not found, skipping upload")

            # Remove the user from term_managers after cleanup

            if userID in self.term_managers:
                del self.term_managers[userID]
                print(f"Removed user {userID} from term_managers")

            return module_name.split("_")[0], section_progress

        except Exception as e:
            print(f"Error cleaning up session for user {userID}: {e}")
