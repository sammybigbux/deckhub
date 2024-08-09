import json
import os

# Define file paths
CORRECT_JSON_FILE_PATH = '../correct_response_api.json'
QUESTIONS_JSON_FILE_PATH = '../questions.json'
LOG_FILE_PATH = 'error_logs/missing_terms_correct.txt'

INCORRECT_JSON_FILE_PATH = '../incorrect_response_api.json'
INCORRECT_LOG_FILE_PATH = 'error_logs/missing_terms_incorrect_learn.txt'

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_text_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [eval(line.strip()) for line in lines]

def check_terms_in_json(json_data, terms_list):
    missing_terms = []

    for item in terms_list:
        term, section = item[0], item[1]
        if section not in json_data or term not in json_data[section]:
            missing_terms.append((section, term))

    return missing_terms

def log_missing_terms(missing_terms, log_file_path):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as file:
        for section, term in missing_terms:
            file.write(f"Section: {section}, Term: {term}\n")

def _test_response(json_file_path, text_file_path, log_file_path):
    json_data = load_json(json_file_path)
    terms_list = load_text_file(text_file_path)

    missing_terms = check_terms_in_json(json_data, terms_list)

    if missing_terms:
        log_missing_terms(missing_terms, log_file_path)
        length = sum(1 for _ in open(log_file_path))
        assert 0, f"terms are in {text_file_path} but not {log_file_path} and have been logged to {log_file_path}"

def check_terms_in_json(correct_json, questions_json):
    missing_terms = []

    for section in questions_json:
        if section not in correct_json:
            missing_terms.append((section, "ALL TERMS"))
            continue
        for term in questions_json[section]:
            if term not in correct_json[section]:
                missing_terms.append((section, term))

    return missing_terms
def test_correct_response():
    correct_json = load_json(CORRECT_JSON_FILE_PATH)
    questions_json = load_json(QUESTIONS_JSON_FILE_PATH)

    missing_terms = check_terms_in_json(correct_json, questions_json)

    if missing_terms:
        log_missing_terms(missing_terms, LOG_FILE_PATH)
        length = sum(1 for _ in open(LOG_FILE_PATH))
        assert 0, f"{length} terms are in {QUESTIONS_JSON_FILE_PATH} but not in {CORRECT_JSON_FILE_PATH} and have been logged to {LOG_FILE_PATH}"


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def log_missing_terms_incorrect(missing_terms, log_file_path):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as file:
        for section, term, incorrect_answer in missing_terms:
            file.write(f"Section: {section}, Term: {term}, Missing Incorrect Answer: {incorrect_answer}\n")

def check_incorrect_terms_in_json(incorrect_json, questions_json):
    missing_terms = []

    for section in questions_json:
        if section not in incorrect_json:
            missing_terms.append((section, "ALL TERMS", "ALL INCORRECT ANSWERS"))
            continue
        for term, details in questions_json[section].items():
            if term not in incorrect_json[section]:
                missing_terms.append((section, term, "ALL INCORRECT ANSWERS"))
                continue
            correct_answer = details['answer']
            for option_key in ['option1', 'option2', 'option3', 'option4']:
                if option_key != correct_answer:
                    incorrect_answer = details[option_key]
                    if incorrect_answer not in incorrect_json[section][term]:
                        missing_terms.append((section, term, incorrect_answer))

    return missing_terms

def test_incorrect_response():
    incorrect_json = load_json(INCORRECT_JSON_FILE_PATH)
    questions_json = load_json(QUESTIONS_JSON_FILE_PATH)

    missing_terms = check_incorrect_terms_in_json(incorrect_json, questions_json)

    if missing_terms:
        log_missing_terms_incorrect(missing_terms, INCORRECT_LOG_FILE_PATH)
        length = sum(1 for _ in open(INCORRECT_LOG_FILE_PATH))
        assert 0, f"{length} terms are in {QUESTIONS_JSON_FILE_PATH} but not in {INCORRECT_JSON_FILE_PATH} and have been logged to {INCORRECT_LOG_FILE_PATH}"
