import json

def transform_understand_data(input_file, output_file):
    # Load the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Initialize the transformed structure
    transformed_data = {}

    # Iterate through each section (first-level key)
    for section, concepts in data.items():
        # Ensure the section exists in the new structure
        if section not in transformed_data:
            transformed_data[section] = {}

        # Iterate through each concept (second-level key)
        for concept_name, concept_data in concepts.items():
            # Extract the specificity from the concept data
            specificity = concept_data.get('specificity', 'unknown').lower().replace(' ', '_')

            # Ensure the specificity exists in the section
            if specificity not in transformed_data[section]:
                transformed_data[section][specificity] = {}

            # Add the exact concept name as a key with the value set to False
            transformed_data[section][specificity][concept_name] = False

    # Write the transformed structure to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(transformed_data, f, indent=4)

    print(f"Transformation complete! Data saved to {output_file}")

# Usage example
transform_understand_data('understand_data.json', 'understand_data_terms.json')
