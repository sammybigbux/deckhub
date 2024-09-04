import json
from pathlib import Path

# Define the path to the directory containing the JSON files, starting from the parent directory of the script's location
json_directory = Path(__file__).parent.parent / "data" / "outputs"

# List of JSON files to merge, with updated names
json_files = [
    "correct_response_api.json", 
    "incorrect_response_api.json", 
    "questions.json", 
    "related_terms_data.json", 
]

# Mapping to rename the JSON keys as specified
key_mapping = {
    "correct_response_api": "correct_response",
    "incorrect_response_api": "incorrect_response",
    "related_terms_data": "related_terms"
}

# Initialize an empty dictionary for the final merged JSON
merged_data = {}

# Iterate over each JSON file
for json_file in json_files:
    # Get the file name without the extension to use as a key
    json_name = Path(json_file).stem

    # Apply the renaming based on the key_mapping
    json_name = key_mapping.get(json_name, json_name)

    # Load the current JSON file
    with (json_directory / json_file).open('r') as f:
        data = json.load(f)

    # Iterate over the sections and primary keys in the current JSON
    for section, primary_keys in data.items():
        if section not in merged_data:
            merged_data[section] = {}

        for primary_key, details in primary_keys.items():
            if primary_key not in merged_data[section]:
                merged_data[section][primary_key] = {}

            # Add the current JSON's data under its corresponding key
            merged_data[section][primary_key][json_name] = details

# Save the merged JSON to a new file
output_path = json_directory / "merged_data.json"
with output_path.open('w') as f:
    json.dump(merged_data, f, indent=4)
