import json
import os
import re
import pytest

# Define file paths
CORPUS_LISTS_PATH = '../corpus_lists.txt'
RELATED_TERMS_DATA_PATH = '../related_terms_data.json'
RELATED_TERMS_PATH = '../related_terms.json'
RELATED_TERMS_LISTS_PATH = '../related_terms_lists.txt'
LOG_FILE_PATH_CORPUS = 'error_logs/missing_rt_corpus.txt'
LOG_FILE_PATH_RT = 'error_logs/missing_rt.txt'
LOG_FILE_PATH_LISTS = 'error_logs/missing_rt_lists.txt'

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def check_related_terms(data, terms):
    missing_terms = {}

    for section, section_terms in terms.items():
        if section in data:
            for term, related_terms_list in section_terms.items():
                if term in data[section]:
                    for related_term in related_terms_list:
                        if related_term not in data[section][term]:
                            if section not in missing_terms:
                                missing_terms[section] = {}
                            if term not in missing_terms[section]:
                                missing_terms[section][term] = []
                            missing_terms[section][term].append(related_term)
                else:
                    if section not in missing_terms:
                        missing_terms[section] = {}
                    missing_terms[section][term] = related_terms_list
        else:
            missing_terms[section] = section_terms

    return missing_terms

def log_missing_terms(missing_terms, log_file_path):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, 'w') as file:
        for section, section_terms in missing_terms.items():
            for term, related_terms_list in section_terms.items():
                for related_term in related_terms_list:
                    file.write(f"{section} -> {term} -> {related_term}\n")

def load_list_of_lists(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    list_of_lists = []
    for line in lines:
        try:
            # Replace single quotes with double quotes
            line_json = line.strip().replace("'", '"')
            # Handle the case where there are escaped single quotes
            line_json = re.sub(r'\\\'', "'", line_json)
            list_of_lists.append(json.loads(line_json))
        except json.JSONDecodeError as e:
            print(f"Failed to parse line: {line.strip()} with error: {e}")
    return list_of_lists

def convert_list_to_dict(list_of_lists):
    result = {}
    for term, section, related_term in list_of_lists:
        if section not in result:
            result[section] = {}
        if term not in result[section]:
            result[section][term] = []
        result[section][term].append(related_term)
    return result

def convert_corpus_lists_to_dict(list_of_lists):
    result = {}
    for term, section in list_of_lists:
        if section not in result:
            result[section] = {}
        if term not in result[section]:
            result[section][term] = ""
    return result

def assert_dicts_equal(dict1, dict2):
    mismatches = []
    all_keys = set(dict1.keys()).union(set(dict2.keys()))
    
    for key in all_keys:
        if key not in dict1:
            mismatches.append(f"Key {key} is missing in the first dictionary.")
        elif key not in dict2:
            mismatches.append(f"Key {key} is missing in the second dictionary.")
        else:
            terms1 = dict1[key]
            terms2 = dict2[key]
            if set(terms1) != set(terms2):
                mismatches.append(f"Mismatch in section '{key}':")
                all_terms = set(terms1.keys()).union(set(terms2.keys()))
                for term in all_terms:
                    if term not in terms1:
                        mismatches.append(f"  Term {term} is missing in the first dictionary.")
                    elif term not in terms2:
                        mismatches.append(f"  Term {term} is missing in the second dictionary.")
                    elif set(terms1[term]) != set(terms2[term]):
                        mismatches.append(f"  Term '{term}' has different related terms.")
                        mismatches.append(f"    First: {terms1[term]}")
                        mismatches.append(f"    Second: {terms2[term]}")
    
    if mismatches:
        mismatch_message = "\n".join(mismatches)
        print(mismatch_message)
        assert False, f"Dictionaries are not equal:\n{mismatch_message}"

def test_related_terms_data():
    """
    Tests that related_terms.json matches up with related_terms_data.json
    """
    related_terms_data = load_json(RELATED_TERMS_DATA_PATH)
    related_terms = load_json(RELATED_TERMS_PATH)

    missing_terms = check_related_terms(related_terms_data, related_terms)

    if missing_terms:
        log_missing_terms(missing_terms, LOG_FILE_PATH_RT)
        length = sum(1 for _ in open(LOG_FILE_PATH_RT))
        assert 0, f"{length} terms are in {RELATED_TERMS_PATH} but not in {RELATED_TERMS_DATA_PATH} and have been logged to {LOG_FILE_PATH_RT}"

@pytest.mark.skip(reason="Can't read in the lists file because some of them contain apostrophes which messes up eval")
def test_related_terms_lists():
    """
    Tests that related_terms_data.json matches up with related_terms_lists.txt
    """
    related_terms_data = load_json(RELATED_TERMS_PATH)
    list_of_lists = load_list_of_lists(RELATED_TERMS_LISTS_PATH)
    list_dict = convert_list_to_dict(list_of_lists)

    assert_dicts_equal(list_dict, related_terms_data)

def test_related_terms_corpus():
    """
    Tests that related_terms.json matches up with corpus_lists.txt
    """
    related_terms_data = load_json(RELATED_TERMS_PATH)
    list_of_lists = load_list_of_lists(CORPUS_LISTS_PATH)
    list_dict = convert_corpus_lists_to_dict(list_of_lists)
    # list_dict is of format {section: {term1: "", term2: "", ...}, ...}
    # related_terms_data is of format {section: {term1: [related_term1, related_term2, ...], ...}, ...}
    missing_terms = []

    for section in list_dict:
        if section not in related_terms_data:
            missing_terms.append(f"Section missing: {section}")
        else:
            for term in list_dict[section]:
                if term not in related_terms_data[section]:
                    missing_terms.append(f"Term missing in section {section}: {term}")

    if missing_terms:
        os.makedirs(os.path.dirname(LOG_FILE_PATH_CORPUS), exist_ok=True)
        with open(LOG_FILE_PATH_CORPUS, 'w') as file:
            for term in missing_terms:
                file.write(f"{term}\n")
        assert 0, f"{len(missing_terms)} missing terms have been logged to {LOG_FILE_PATH_CORPUS}"

