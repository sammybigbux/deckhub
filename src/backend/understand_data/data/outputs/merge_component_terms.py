import json

def load_json(file_path):
    """Load a JSON file and return its content."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    """Save the provided data into a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def merge_component_terms(understand_data, concept_terms_mapping):
    """Merge component_terms into understand_data_with_specificity.json."""
    for section, nested_content in concept_terms_mapping.items():
        if section not in understand_data:
            print(f"Warning: Section '{section}' not found in understand_data_with_specificity.json.")
            continue

        # Access the nested section inside concept_terms_mapping
        section_concepts = nested_content.get(section, {})
        
        # Iterate over concepts within the section
        for concept, term_data in section_concepts.items():
            if concept in understand_data[section]:
                # Add component_terms to the concept
                understand_data[section][concept]["component_terms"] = term_data.get("component_terms", [])
            else:
                print(f"Warning: Concept '{concept}' not found in section '{section}' of understand_data_with_specificity.json.")

    return understand_data

def main():
    # File paths
    understand_data_path = 'understand_data_with_specificity.json'
    concept_terms_mapping_path = 'concept_terms_mapping.json'
    output_path = 'merged_understand_data_with_terms.json'

    # Load the JSON files
    understand_data = load_json(understand_data_path)
    concept_terms_mapping = load_json(concept_terms_mapping_path)

    # Merge the data
    merged_data = merge_component_terms(understand_data, concept_terms_mapping)

    # Save the merged data to a new file
    save_json(merged_data, output_path)

    print(f"Merged data has been saved to '{output_path}'.")

if __name__ == "__main__":
    main()
