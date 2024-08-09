import json

# Load dictionary from related_terms.json
with open('related_terms.json', 'r') as file:
    data = json.load(file)

# Open the output file related_terms.txt
with open('related_terms_lists.txt', 'w') as file:
    # Iterate over sections and terms
    for section, terms in data.items():
        for term, related_terms in terms.items():
            for related_term in related_terms:
                # Write each term, its section, and the related term to the file
                file.write(f"['{term}', '{section}', '{related_term}']\n")

print("Conversion complete. Check related_terms.txt for the output.")
