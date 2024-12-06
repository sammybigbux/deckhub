import json
import os

# Define file paths
QUESTIONS_FILE_PATH = '../questions.json'
CORPUS_LIST_PATH = '../corpus_lists.txt'
LOG_FILE_PATH = 'error_logs/missing_questions.txt'
MISSING_KEYS_LOG_FILE_PATH = 'error_logs/missing_keys.txt'

REQUIRED_KEYS = ["question", "option1", "option2", "option3", "option4", "answer"]

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

def check_required_keys(json_data):
    missing_keys_entries = []

    for category in json_data:
        for term in json_data[category]:
            term_data = json_data[category][term]
            missing_keys = [key for key in REQUIRED_KEYS if key not in term_data]
            if missing_keys:
                missing_keys_entries.append((category, term, missing_keys))

    return missing_keys_entries

def log_missing_entries(missing_entries, log_file_path):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as file:
        for category, term in missing_entries:
            file.write(f"Category: {category}, Term: {term}\n")

def log_missing_keys_entries(missing_keys_entries, log_file_path):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as file:
        for category, term, missing_keys in missing_keys_entries:
            file.write(f"Category: {category}, Term: {term}, Missing Keys: {missing_keys}\n")

def test_questions():
    """
    Tests that questions.json matches up with corpus_lists.txt
    and checks for required keys within each term's dictionary
    """
    json_data = load_json(QUESTIONS_FILE_PATH)
    corpus_list = load_corpus_list(CORPUS_LIST_PATH)

    missing_entries = check_terms_and_categories_in_json(json_data, corpus_list)
    missing_keys_entries = check_required_keys(json_data)

    if missing_entries:
        log_missing_entries(missing_entries, LOG_FILE_PATH)
        length = sum(1 for _ in open(LOG_FILE_PATH))
        assert 0, f"There are {length} missing categories and terms logged to {LOG_FILE_PATH}"

    if missing_keys_entries:
        log_missing_keys_entries(missing_keys_entries, MISSING_KEYS_LOG_FILE_PATH)
        length = sum(1 for _ in open(MISSING_KEYS_LOG_FILE_PATH))
        assert 0, f"There are {length} terms with missing keys logged to {MISSING_KEYS_LOG_FILE_PATH}"

    if not missing_entries and not missing_keys_entries:
        print("All categories, terms, and required keys are present in the JSON file.")
