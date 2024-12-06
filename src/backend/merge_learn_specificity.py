import json

# Load data from JSON files
with open("learn_data_terms.json") as terms_file, open("learn_specificity.json") as specificity_file:
    terms_data = json.load(terms_file)
    specificity_data = json.load(specificity_file)

# Create the merged structure
merged_data = {}

for section, terms in specificity_data.items():
    merged_data[section] = {"foundational": {}, "intermediate": {}, "special topics": {}}
    for term, specificity in terms.items():
        # Assign the term as False within the appropriate specificity level
        merged_data[section][specificity][term] = False

# Save the merged data to a new JSON file
with open("merged_data.json", "w") as merged_file:
    json.dump(merged_data, merged_file, indent=4)

print("Data merged successfully into 'merged_data.json'")
