import json

# Load the JSON files
with open('terms.json', 'r') as terms_file:
    terms_data = json.load(terms_file)

with open('concept_lists.json', 'r') as concept_lists_file:
    concept_lists_data = json.load(concept_lists_file)

with open('understand_data_with_specificity.json', 'r') as understand_data_file:
    understand_data = json.load(understand_data_file)

# Extract concepts from terms.json
def extract_terms_concepts(terms_data):
    terms_concepts = set()
    for section, section_data in terms_data.items():
        terms_concepts.update(section_data.keys())
    return terms_concepts

# Extract concepts from concept_lists.json
def extract_concept_lists_concepts(concept_lists_data):
    concept_lists_concepts = set()
    for section, specificity_data in concept_lists_data.items():
        for concepts_list in specificity_data.values():
            concept_lists_concepts.update(concepts_list)
    return concept_lists_concepts

# Extract concepts from understand_data_with_specificity.json
def extract_understand_data_concepts(understand_data):
    understand_concepts = set()
    for section, section_data in understand_data.items():
        understand_concepts.update(section_data.keys())
    return understand_concepts

# Extract concepts from all three files
terms_concepts = extract_terms_concepts(terms_data)
concept_lists_concepts = extract_concept_lists_concepts(concept_lists_data)
understand_concepts = extract_understand_data_concepts(understand_data)

# Find mismatches between the three sets
def find_mismatches(set1, set2, set3):
    all_concepts = set1 | set2 | set3
    mismatches = {
        "only_in_terms": sorted(all_concepts - set2 - set3),
        "only_in_concept_lists": sorted(all_concepts - set1 - set3),
        "only_in_understand_data": sorted(all_concepts - set1 - set2)
    }
    return mismatches

mismatches = find_mismatches(terms_concepts, concept_lists_concepts, understand_concepts)

# Print results
if any(mismatches.values()):
    print("Mismatches found:")
    if mismatches["only_in_terms"]:
        print("\nConcepts only in terms.json:")
        for concept in mismatches["only_in_terms"]:
            print(concept)

    if mismatches["only_in_concept_lists"]:
        print("\nConcepts only in concept_lists.json:")
        for concept in mismatches["only_in_concept_lists"]:
            print(concept)

    if mismatches["only_in_understand_data"]:
        print("\nConcepts only in understand_data_with_specificity.json:")
        for concept in mismatches["only_in_understand_data"]:
            print(concept)
else:
    print("All concept names are consistent across all three files.")
