import json

# Define the input and output file names
input_file = 'processed_corpus.txt'
output_file = 'terms.json'

# Initialize an empty dictionary to store the concepts and categories
concept_dict = {}

# Read the input file and process each line
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        # Strip whitespace and split the line into concept and category
        line = line.strip()
        if '(' in line and ')' in line:
            concept, category = line.split(' (')
            category = category[:-1]  # Remove the closing ')'

            # Initialize the category if not already present
            if category not in concept_dict:
                concept_dict[category] = {}

            # Add the concept to the category with a value of False
            concept_dict[category][concept] = False

# Write the resulting dictionary to the output file in JSON format
with open(output_file, 'w') as file:
    json.dump(concept_dict, file, indent=4)

print(f"Processed concepts have been saved to {output_file}.")
