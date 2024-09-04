import json

def process_json(input_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    result = []
    for section, terms in data.items():
        for term in terms:
            result.append([term, section])
    
    return result

def save_to_file(data, output_file):
    with open(output_file, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

if __name__ == "__main__":
    input_file = 'questions.json'
    output_file = 'corpus_lists.txt'

    processed_data = process_json(input_file)
    save_to_file(processed_data, output_file)
