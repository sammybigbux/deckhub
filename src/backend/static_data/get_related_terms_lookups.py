import json
from collections import defaultdict, Counter

# Load the JSON data from the file
with open('learn_data.json', 'r') as file:
    big_dict = json.load(file)

# Initialize dictionaries to store occurrences and co-occurrences
related_term_occurrences = defaultdict(set)    # {related_term: set of (section, term)}
related_term_cooccurrences = defaultdict(Counter)  # {related_term: Counter of co-occurring related_terms}

# First pass: Build mappings of occurrences and co-occurrences
for section, terms in big_dict.items():
    for term, term_data in terms.items():
        related_terms = term_data.get('related_terms', {}).keys()
        related_terms = list(related_terms)
        
        # Record occurrences
        for related_term in related_terms:
            related_term_occurrences[related_term].add((section, term))
        
        # Record co-occurrences
        for rt1 in related_terms:
            for rt2 in related_terms:
                if rt1 != rt2:
                    related_term_cooccurrences[rt1][rt2] += 1

# Second pass: Add 'lookups' to each related term in the original data
for section, terms in big_dict.items():
    for term, term_data in terms.items():
        related_terms = term_data.get('related_terms', {})
        
        for related_term in related_terms.keys():
            # Get co-occurring terms for this related term
            co_terms_counter = related_term_cooccurrences.get(related_term, Counter())
            top_co_terms = co_terms_counter.most_common(9)
            
            lookups = []
            for co_term, weight in top_co_terms:
                # Get one occurrence of the co-occurring term
                co_occurrences = related_term_occurrences.get(co_term, set())
                if co_occurrences:
                    co_section, co_term_term = next(iter(co_occurrences))
                    lookup_entry = {
                        "section": co_section,
                        "term": co_term_term,
                        "related_term": co_term,
                        "weight": weight
                    }
                    lookups.append(lookup_entry)
            
            # Add 'lookups' to the related term in the data
            related_term_data = term_data['related_terms'][related_term]
            related_term_data['lookups'] = lookups

# Write the updated data back to the JSON file
with open('learn_data_updated.json', 'w') as outfile:
    json.dump(big_dict, outfile, indent=4)
