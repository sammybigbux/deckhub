import json

def load_json(file_path):
    """Helper function to load a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_concepts_from_terms(terms_data):
    """Extract all concept names from terms.json."""
    concepts = set()
    for section in terms_data.values():
        concepts.update(section.keys())
    return concepts

def extract_concepts_from_understand_data(understand_data):
    """Extract all concept names from understand_data_with_specificity.json."""
    concepts = set()
    for section in understand_data.values():
        concepts.update(section.keys())
    return concepts

def find_differences(terms_concepts, understand_concepts):
    """Find concepts present in one file but not the other."""
    extra_in_terms = terms_concepts - understand_concepts
    missing_in_terms = understand_concepts - terms_concepts

    return extra_in_terms, missing_in_terms

def main():
    # Load the JSON files
    terms_data = load_json('terms.json')
    understand_data = load_json('understand_data_with_specificity.json')

    # Extract concepts from both files
    terms_concepts = extract_concepts_from_terms(terms_data)
    understand_concepts = extract_concepts_from_understand_data(understand_data)

    # Find differences
    extra_in_terms, missing_in_terms = find_differences(terms_concepts, understand_concepts)

    # Print the results
    if extra_in_terms:
        print("Concepts in 'terms.json' but NOT in 'understand_data_with_specificity.json':")
        for concept in extra_in_terms:
            print(concept)
    else:
        print("No extra concepts in 'terms.json'.")

    if missing_in_terms:
        print("\nConcepts in 'understand_data_with_specificity.json' but NOT in 'terms.json':")
        for concept in missing_in_terms:
            print(concept)
    else:
        print("No missing concepts in 'terms.json'.")

if __name__ == "__main__":
    main()
