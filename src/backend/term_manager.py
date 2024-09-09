import json
import random
import time
from functools import lru_cache
from pathlib import Path



class TermManager:
    def __init__(self, module_name="learn_data", userID=None):
        print(f"Tm initializing")
        self.userID = userID
        self.terms_path = Path(module_name) / userID / "terms.json"
        self.section = "Networking"  # Default section; can be set dynamically
        self.terms = self._read_json()  # Only terms.json is read and written locally
        print(f"If you see this then tm initialized")
        self.total_terms = sum([len(self.terms[section]) for section in self.terms])
        self.solved_terms = sum([len([term for term in self.terms[section] if self.terms[section][term]]) for section in self.terms])
        

    def _read_json(self):
        """Read the user's terms.json."""
        print(f"Trying to read json at {self.terms_path}")
        user_dir = self.terms_path.parent
        user_dir.mkdir(parents=True, exist_ok=True)
        with open(self.terms_path, 'r') as f:
            return json.load(f)

    def write_terms_to_file(self):
        """Write the stored terms to the user's terms.json at the end of the session."""
        with open(self.terms_path, 'w') as f:
            json.dump(self.terms, f, indent=4)

    def get_rt_response(self, data, term, related_term):
        """Retrieve the related term response from the passed-in data dictionary."""
        return data[self.section][term]["related_terms"][related_term]

    def get_correct_response(self, data, term):
        """Retrieve the correct response for a term from the passed-in data dictionary."""
        return data[self.section][term]["correct_response"]

    def get_incorrect_response(self, data, term, answer):
        """Retrieve the incorrect response for a given answer from the passed-in data dictionary."""
        return data[self.section][term]["incorrect_response"][answer]

    def retrieve_question(self, data, section, term=None):
        """Retrieve a question for a given section and term from the passed-in data dictionary."""
        terms = self.get_not_passed_terms(section)
        if terms:
            random_term = random.choice(terms) if term is None else term
            question = data[section][random_term]["questions"]
            question["section"] = section
            question["term"] = random_term
            question["related_terms"] = data[section][random_term]["related_terms"]
            return question
        return "No more terms available in this section."

    def update_status(self, term):
        """Update the status of a term in self.terms without writing to terms.json."""
        section = self.section.capitalize()
        if section in self.terms and term in self.terms[section]:
            self.terms[section][term] = True
            self.solved_terms += 1
        else:
            raise ValueError(f"Term '{term}' not found in section '{section}'")

    def get_not_passed_terms(self, section):
        """Retrieve terms that have not yet been passed for a section."""
        return [term for term, info in self.terms.get(section, {}).items() if not info]

    def get_remaining_terms(self):
        """Get terms that haven't been solved for the current section."""
        return "\n".join([term for term in self.terms[self.section] if not self.terms[self.section][term]])
    
    def get_total_terms(self):
        """Get the total number of terms in the user's terms.json."""
        return self.total_terms
    
    def get_solved_terms(self):
        """Get the total number of terms that have been solved."""
        return self.solved_terms

    def reset_all_terms(self):
        """Reset the status of all terms in self.terms to False."""
        for section in self.terms:
            for term in self.terms[section]:
                self.terms[section][term] = False

    def pass_all_terms(self):
        """Mark all terms in self.terms as passed (True)."""
        for section in self.terms:
            for term in self.terms[section]:
                self.terms[section][term] = True

    def reload_terms(self):
        """Reload the user's terms.json data."""
        self.terms = self._read_json()

    def get_remaining_sections(self):
        start_time = time.time()
        result = "\n".join(section for section, terms in self.terms.items() if not all(terms.values()))
        print(f"get_remaining_sections took {time.time() - start_time} seconds")
        return result
