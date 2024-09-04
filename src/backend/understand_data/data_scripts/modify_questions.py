import json

def convert_related_terms_to_list(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    lines = []
    for section, terms in data.items():
        for term, related_terms in terms.items():
            for related_term in related_terms:
                lines.append(f"['{term}', '{section}', '{related_term}']\n")

    with open(output_file, 'w') as outfile:
        outfile.writelines(lines)

    print(f"Conversion complete. Results written to {output_file}")

if __name__ == "__main__":
    input_file = 'related_terms.json'
    output_file = 'related_terms_lists.txt'
    convert_related_terms_to_list(input_file, output_file)
