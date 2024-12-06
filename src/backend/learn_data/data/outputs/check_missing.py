import json
from collections import defaultdict
from pathlib import Path

def load_json(file_path):
    """Helper function to load JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def get_unique_concepts(concept_lists):
    """
    Extract unique concepts from concept_lists.json.
    Handles duplicate section names by merging their concepts.
    """
    unique_concepts = defaultdict(dict)

    for section, section_data in concept_lists.items():
        # Merge concepts from duplicate sections
        for subsection, concepts in section_data.items():
            for concept, concept_data in concepts.items():
                unique_concepts[section][concept] = concept_data

    return unique_concepts

def compare_concept_lists(concept_lists, terms_concepts):
    """Compare concept_lists.json with terms_concepts.json."""
    missing_sections = []
    missing_concepts = defaultdict(list)

    # Extract unique concepts from concept_lists.json
    unique_concepts = get_unique_concepts(concept_lists)

    # Compare sections
    for section in terms_concepts:
        if section not in unique_concepts:
            missing_sections.append(section)
        else:
            # Compare concepts within the section
            for concept in terms_concepts[section]:
                if concept not in unique_concepts[section]:
                    missing_concepts[section].append(concept)

    return missing_sections, missing_concepts

def main():
    # Load the JSON files
    concept_lists = load_json('concept_terms_mapping.json')
    terms_concepts = load_json('terms_concepts.json')

    # Compare the two files
    missing_sections, missing_concepts = compare_concept_lists(concept_lists, terms_concepts)

    # Display the results
    if missing_sections:
        print("Missing Sections:")
        for section in missing_sections:
            print(f"  - {section}")
    else:
        print("No missing sections found.")

    if missing_concepts:
        print("\nMissing Concepts:")
        for section, concepts in missing_concepts.items():
            print(f"Section: {section}")
            for concept in concepts:
                print(f"  - {concept}")
    else:
        print("No missing concepts found.")

if __name__ == "__main__":
    main()
