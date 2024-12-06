import json
from pathlib import Path

# Load the hierarchy.json file
with open('hierarchy.json', 'r') as f:
    hierarchy = json.load(f)

# Use a stack to process elements iteratively
nodes_to_process = [hierarchy]  # Start with the top-level dictionary

while nodes_to_process:
    current_node = nodes_to_process.pop()  # Get the current node

    if isinstance(current_node, dict):
        # If 'correct' exists, replace it with 'weight' set to 0
        if 'correct' in current_node:
            current_node['weight'] = 0
            del current_node['correct']  # Remove the old 'correct' key

        # If 'downstream' exists, add its children to the stack
        if 'downstream' in current_node:
            for key, value in current_node['downstream'].items():
                nodes_to_process.append(value)  # Add nested dictionaries to the stack

# Save the modified hierarchy to hierarchy_updated.json
with open('hierarchy_updated.json', 'w') as f:
    json.dump(hierarchy, f, indent=4)

print("Updated hierarchy saved to hierarchy_updated.json")
