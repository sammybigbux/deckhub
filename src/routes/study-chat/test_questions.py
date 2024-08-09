import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_corpus_list(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [eval(line.strip()) for line in lines]

def check_terms_and_categories_in_json(json_data, corpus_list):
    missing_entries = []

    for item in corpus_list:
        term, category = item[0], item[1]
        if category not in json_data or term not in json_data[category]:
            missing_entries.append((category, term))

    return missing_entries

def log_missing_entries(missing_entries, log_file_path):
    with open(log_file_path, 'w') as file:
        for category, term in missing_entries:
            file.write(f"Category: {category}, Term: {term}\n")

def main():
    json_file_path = 'questions.json'
    corpus_list_path = 'corpus_lists.txt'
    log_file_path = 'missing_terms_learn.txt'

    json_data = load_json(json_file_path)
    corpus_list = load_corpus_list(corpus_list_path)

    missing_entries = check_terms_and_categories_in_json(json_data, corpus_list)

    if missing_entries:
        log_missing_entries(missing_entries, log_file_path)
        print(f"Missing categories and terms have been logged to {log_file_path}")
    else:
        print("All categories and terms are present in the JSON file.")

if __name__ == "__main__":
    main()
