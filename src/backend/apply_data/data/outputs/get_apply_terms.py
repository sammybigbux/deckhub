import json

def transform_json(input_json):
    # Initialize the result dictionary
    transformed = {}

    # Iterate through the first level of keys (sections)
    for section, concepts in input_json.items():
        if isinstance(concepts, dict):
            # Prepare a nested dictionary using specificity values
            section_dict = {}
            for concept, details in concepts.items():
                if isinstance(details, dict) and "specificity" in details:
                    specificity_value = details["specificity"]
                    if specificity_value not in section_dict:
                        section_dict[specificity_value] = {}
                    section_dict[specificity_value][concept] = False
                else:
                    # Handle cases where specificity is missing
                    if "undefined" not in section_dict:
                        section_dict["undefined"] = {}
                    section_dict["undefined"][concept] = False

            # Assign the section dictionary to the section key
            transformed[section] = section_dict
        else:
            # If not a dictionary, assign 'undefined' specificity
            transformed[section] = {"undefined": {section: False}}

    return transformed

def main():
    # Read the input JSON file
    with open("apply_data.json", "r") as infile:
        input_data = json.load(infile)

    # Transform the JSON data
    output_data = transform_json(input_data)

    # Write the transformed data to the output JSON file
    with open("apply_data_terms.json", "w") as outfile:
        json.dump(output_data, outfile, indent=4)

    print("Transformation complete! Output written to 'apply_data_terms.json'.")

# Entry point for the script
if __name__ == "__main__":
    main()
