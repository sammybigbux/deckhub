import json

# Load the input JSON file
with open('understand_data.json', 'r') as file:
    data = json.load(file)

# Create a new dictionary to store the output
output = {}

# Loop through each section
for section, concepts in data.items():
    section_dict = {"foundational": [], "intermediate": [], "special topics": []}

    for concept, details in concepts.items():
        # Extract the specificity from the concept's details
        specificity = details.get('specificity', 'unknown')

        # Append the concept to the appropriate specificity list
        if specificity in section_dict:
            section_dict[specificity].append(concept)
        else:
            section_dict['special topics'].append(concept)  # Default to 'special topics' if unknown

    output[section] = section_dict

# Write the output to a new JSON file
with open('concept_lists.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)

print("Output saved to 'concept_lists.json'")
