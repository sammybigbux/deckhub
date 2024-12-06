import json
from collections import defaultdict, Counter

# Load the co-occurrence data from 'related_terms_lookups_learn.json'
with open('related_terms_lookups_learn.json', 'r') as file:
    cooccurrence_data = json.load(file)

# Load the original JSON data from 'learn_data.json'
with open('learn_data.json', 'r') as file:
    data = json.load(file)

# Function to add 'lookups' to each related term
def add_lookups_to_related_terms(data, cooccurrence_data):
    for section, concepts in data.items():
        for concept, concept_data in concepts.items():
            related_terms = concept_data.get('related_terms', {})
            for term, term_data in related_terms.items():
                # Get the lookups for the term from cooccurrence_data
                lookups = cooccurrence_data.get(term, [])
                # Add the 'lookups' key to the term's dictionary
                term_data['lookups'] = lookups
    return data

# Add 'lookups' to each related term in the data
updated_data = add_lookups_to_related_terms(data, cooccurrence_data)

# Write the updated data to a new JSON file
with open('learn_data_with_lookups.json', 'w') as outfile:
    json.dump(updated_data, outfile, indent=4)
