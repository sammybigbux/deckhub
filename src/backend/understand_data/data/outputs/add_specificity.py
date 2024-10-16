import json

# Load the understand_data.json and specificity.json files
with open('understand_data.json', 'r') as f:
    understand_data = json.load(f)

with open('specificity.json', 'r') as f:
    specificity_data = json.load(f)

# Initialize a flag to track if any missing concepts are found
missing_concepts = False

# Check for sections and concepts in understand_data that are not in specificity_data
for section, concepts in understand_data.items():
    if section not in specificity_data:
        print(f"Section '{section}' is missing from specificity.json.")
        missing_concepts = True
    else:
        for concept in concepts:
            if concept not in specificity_data[section]:
                print(f"Concept '{concept}' in section '{section}' is missing from specificity.json.")
                missing_concepts = True

# If no missing concepts are found, print a message
if not missing_concepts:
    print("All sections and concepts in understand_data.json are present in specificity.json.")

# Save the modified data to understand_data_terms.json with "specificity" added
for section, concepts in understand_data.items():
    if section in specificity_data:
        for concept in concepts:
            if concept in specificity_data[section]:
                understand_data[section][concept]['specificity'] = specificity_data[section][concept]

# Save the updated JSON with specificity
with open('understand_data_with_specificity.json', 'w') as f:
    json.dump(understand_data, f, indent=4)

print("The new understand_data_terms.json file has been created with the 'specificity' attribute.")
