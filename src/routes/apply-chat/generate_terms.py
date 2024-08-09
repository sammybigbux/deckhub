import json
import re

# Define the input and output file names
input_file = 'corpus.txt'
output_file = 'terms.json'

# Initialize an empty dictionary to store the concepts and categories
concept_dict = {}

# Regular expression to match the concept and the last set of parentheses
pattern = re.compile(r'^(.*)\s+\(([^()]*)\)$')

# Read the input file and process each line
with open(input_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        # Strip whitespace and match the line with the regular expression
        line = line.strip()
        match = pattern.match(line)
        if match:
            concept, category = match.groups()
            
            # Initialize the category if not already present
            if category not in concept_dict:
                concept_dict[category] = {}

            # Add the concept to the category with a value of False
            concept_dict[category][concept] = False

# Write the resulting dictionary to the output file in JSON format
with open(output_file, 'w') as file:
    json.dump(concept_dict, file, indent=4)

print(f"Processed concepts have been saved to {output_file}.")
