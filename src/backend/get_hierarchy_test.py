import json

# Load apply_data_terms.json to extract Networking scenario names
with open("apply_data_terms.json", "r") as f:
    apply_data_terms = json.load(f)

# Get all scenario names from the Networking section in apply_data_terms.json
networking_scenarios = []
if "Networking" in apply_data_terms:
    for level in apply_data_terms["Networking"].values():
        networking_scenarios.extend(level.keys())

# Load hierarchy.json to filter entries based on the Networking scenarios
with open("hierarchy.json", "r") as f:
    hierarchy_data = json.load(f)

# Filter hierarchy_data to only include entries with keys in networking_scenarios
filtered_hierarchy = {key: value for key, value in hierarchy_data.items() if key in networking_scenarios}

# Save the filtered data to hierarchy_test.json
with open("hierarchy_test.json", "w") as f:
    json.dump(filtered_hierarchy, f, indent=4)

print("Filtered hierarchy saved to hierarchy_test.json")
