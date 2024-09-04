import json
import random
import time
from functools import lru_cache
from pathlib import Path
import firebase_admin


class TermManager:
    def __init__(self, data_dir="learn_data", userID=None):
        self.userID = userID
        self.data_dir = Path(data_dir) / "data" / "outputs"
        self.terms_path = self.data_dir / userID /  "terms.json"
        self.data = self._read_json()
        self.related_terms = self._get_related_terms()
        self.term_questions = self._get_term_questions()
        self.section = "Networking"
        self.rt_responses = self._get_rt_responses()
        self.correct_responses = self._get_correct_responses()
        self.incorrect_responses = self._get_incorrect_responses()


    def _read_json(self):
        user_dir = self.data_dir / self.userID
        user_dir.mkdir(parents=True, exist_ok=True)
        with open(self.terms_path, 'r') as f:
            result = json.load(f)

        return result

    def _get_related_terms(self):
        start_time = time.time()
        related_terms_path = self.data_dir / "related_terms.json"
        with open(related_terms_path, 'r') as f:
            result = json.load(f)
        print(f"_get_related_terms took {time.time() - start_time} seconds")
        return result

    def _get_term_questions(self):
        questions_path = self.data_dir / "questions.json"
        with open(questions_path, 'r') as f:
            result = json.load(f)
        return result
    
    def _get_rt_responses(self):
        rt_responses_path = self.data_dir / "related_terms_data.json"
        with open(rt_responses_path, 'r') as f:
            result = json.load(f)
        return result

    def _get_incorrect_responses(self):
        incorrect_responses_path = self.data_dir / "incorrect_response_api.json"
        with open(incorrect_responses_path, 'r') as f:
            result = json.load(f)
        return result
    
    def _get_correct_responses(self):
        correct_responses_path = self.data_dir / "correct_response_api.json"
        with open(correct_responses_path, 'r') as f:
            result = json.load(f)
        return result

    def _write_json(self):
        start_time = time.time()
        with open(self.terms_path, 'w') as f:
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
    
    def get_rt_response(self, term, related_term):
        return self.rt_responses[self.section][term][related_term]
    
    def get_correct_response(self, term):
        return self.correct_responses[self.section][term]
    
    def get_incorrect_response(self, term, answer):
        return self.incorrect_responses[self.section][term][answer]

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

    def update_status(self, term):
        start_time = time.time()
        section = self.section.capitalize()
        if section in self.data and term in self.data[section]:
            self.data[section][term] = True
            self._write_json()
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

    def reload_data(self):
        start_time = time.time()
        self.data = self._read_json()
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
