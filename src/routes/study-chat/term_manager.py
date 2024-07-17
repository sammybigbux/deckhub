import json
import random
import time
from functools import lru_cache

class TermManager:
    def __init__(self, file_path='terms_fixed.json'):
        self.file_path = file_path
        self.data = self._read_json()
        self.related_terms = self._get_related_terms()
        self.completion = self._calculate_completion()
        self.term_questions = self._get_term_questions()
        self.correct_answer = False
        self.section = "Databases"

    @lru_cache(maxsize=None)
    def _read_json(self):
        start_time = time.time()
        with open(self.file_path, 'r') as f:
            result = json.load(f)
        print(f"_read_json took {time.time() - start_time} seconds")
        return result

    @lru_cache(maxsize=None)
    def _get_related_terms(self):
        start_time = time.time()
        with open("related_terms.json", 'r') as f:
            result = json.load(f)
        print(f"_get_related_terms took {time.time() - start_time} seconds")
        return result

    @lru_cache(maxsize=None)
    def _get_term_questions(self):
        start_time = time.time()
        with open("term_questions_fixed.json", 'r') as f:
            result = json.load(f)
        print(f"_get_term_questions took {time.time() - start_time} seconds")
        return result

    def _write_json(self):
        start_time = time.time()
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f"_write_json took {time.time() - start_time} seconds")

    def _calculate_completion(self):
        start_time = time.time()
        completion = {
            section: (sum(info for info in terms.values()) / len(terms)) * 100 if terms else 0
            for section, terms in self.data.items()
        }
        print(f"_calculate_completion took {time.time() - start_time} seconds")
        return completion

    def get_not_passed_terms(self, section):
        start_time = time.time()
        result = [term for term, info in self.data.get(section, {}).items() if not info]
        print(f"get_not_passed_terms took {time.time() - start_time} seconds")
        return result

    def get_total_terms(self):
        start_time = time.time()
        result = sum(len(terms) for terms in self.data.values())
        print(f"get_total_terms took {time.time() - start_time} seconds")
        return result

    def get_solved_terms(self):
        start_time = time.time()
        result = sum(sum(1 for passed in terms.values() if passed) for terms in self.data.values())
        print(f"get_solved_terms took {time.time() - start_time} seconds")
        return result

    def update_status(self, section, term, passed):
        start_time = time.time()
        section = section.capitalize()
        if section in self.data and term in self.data[section]:
            self.correct_answer = True
            print(f"!!!!!!!!The term {term} in section {section} has been updated to {passed}!!!!!!!!!")
            self.data[section][term] = passed
            self._write_json()
            self.completion[section] = (sum(info for info in self.data[section].values()) / len(self.data[section])) * 100
        else:
            raise ValueError(f"Term '{term}' not found in section '{section}'")
        print(f"update_status took {time.time() - start_time} seconds")

    def get_remaining_sections(self):
        start_time = time.time()
        result = "\n".join(section for section, terms in self.data.items() if not all(terms.values()))
        print(f"get_remaining_sections took {time.time() - start_time} seconds")
        return result

    def get_remaining_terms(self):
        start_time = time.time()
        print(f"Trying to get the terms from this section: {self.section}")
        return "\n".join([term for term in self.data[self.section] if not self.data[self.section][term]])

    def get_completion(self):
        start_time = time.time()
        result = self.completion
        print(f"get_completion took {time.time() - start_time} seconds")
        return result

    def reload_data(self):
        start_time = time.time()
        self.data = self._read_json()
        self.completion = self._calculate_completion()
        print(f"reload_data took {time.time() - start_time} seconds")

    def retrieve_question(self, section, term=None):
        start_time = time.time()
        terms = self.get_not_passed_terms(section)
        if terms:
            random_term = random.choice(terms) if term is None else term
            assert section in self.term_questions, f"Section {section} not found in term_questions_fixed.json"
            question = self.term_questions[section][random_term]
            question["section"] = section
            question["term"] = random_term
            question["related_terms"] = self.related_terms[section][random_term]
            result = question
        else:
            result = "No more terms available in this section."
        print(f"retrieve_question took {time.time() - start_time} seconds")
        return result

    def reset_all_terms(self):
        start_time = time.time()
        for section in self.data:
            for term in self.data[section]:
                self.data[section][term] = False
        self._write_json()
        print(f"reset_all_terms took {time.time() - start_time} seconds")

    def pass_all_terms(self):
        start_time = time.time()
        for section in self.data:
            for term in self.data[section]:
                self.data[section][term] = True
        self._write_json()
        print(f"pass_all_terms took {time.time() - start_time} seconds")
