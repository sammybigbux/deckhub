import unittest
import os
import requests
import json
from pathlib import Path
from random import choice

class TestTermManagerEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the environment once for all tests."""
        cls.parent_dir = Path(__file__).resolve().parent.parent
        cls.userID = "JPqzMvLnJSQvfxw841ibYWDyqVl2"
        cls.module_type = "learn"
        cls.local_terms_path = cls.parent_dir / f"{cls.module_type}_data/{cls.userID}/terms.json"
        cls.base_url = os.getenv('TEST_ENV_URL', 'http://localhost:5000')

        # Initialize the environment to ensure terms.json is available
        cls._initialize_env()

    @classmethod
    def _initialize_env(cls):
        """Helper method to initialize the environment."""
        url = f"{cls.base_url}/initialize_env"
        payload = {"userID": cls.userID, "module": cls.module_type}
        response = requests.post(url, json=payload)
        assert response.status_code == 200, "Failed to initialize environment."

    def _read_terms_file(self):
        """Helper method to read the local terms.json file."""
        with open(self.local_terms_path, 'r') as f:
            return json.load(f)

    def _update_status(self, term):
        """Helper method to update the status of a term."""
        url = f"{self.base_url}/update_status"
        payload = {"term": term, "userID": self.userID}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, f"Failed to update status for {term}")

    def _get_terms_data(self):
        """Helper method to get terms data."""
        url = f"{self.base_url}/get_terms_data"
        payload = {"userID": self.userID}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, "Failed to get terms data")
        return response.json()

    def _reset_terms(self):
        """Helper method to reset all terms."""
        url = f"{self.base_url}/reset_terms"
        payload = {"userID": self.userID}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, "Failed to reset terms")

    def test_update_status(self):
        """Test the /update_status endpoint."""
        terms_data = self._read_terms_file()
        section = next(iter(terms_data))  # Get the first section
        foundational_terms = terms_data[section].get('foundational', {})
        self.assertTrue(foundational_terms, "No foundational terms found in the terms.json file.")

        term_to_update = choice(list(foundational_terms.keys()))

        self._update_status(term_to_update)

        updated_data = self._read_terms_file()
        self.assertTrue(
            updated_data[section]['foundational'][term_to_update],
            f"Status for {term_to_update} was not updated correctly."
        )

    def test_get_terms_data_after_update_status(self):
        """Test that solvedTerms increments by one after update_status."""
        initial_response = self._get_terms_data()
        initial_solved_terms = initial_response['solvedTerms']

        terms_data = self._read_terms_file()
        section = next(iter(terms_data))
        foundational_terms = terms_data[section].get('foundational', {})
        self.assertTrue(foundational_terms, "No foundational terms found.")

        term_to_update = choice(list(foundational_terms.keys()))

        self._update_status(term_to_update)

        updated_response = self._get_terms_data()
        updated_solved_terms = updated_response['solvedTerms']

        self.assertEqual(
            updated_solved_terms, initial_solved_terms + 1,
            f"Expected solvedTerms to increment by 1. Got {updated_solved_terms} instead of {initial_solved_terms + 1}."
        )

    def test_reset_terms(self):
        """Test that resetting terms sets solvedTerms to zero."""
        # First, mark a term as solved to ensure solvedTerms is not zero
        terms_data = self._read_terms_file()
        section = next(iter(terms_data))
        foundational_terms = terms_data[section].get('foundational', {})
        self.assertTrue(foundational_terms, "No foundational terms found.")

        term_to_update = choice(list(foundational_terms.keys()))

        self._update_status(term_to_update)

        # Verify that solvedTerms is greater than zero
        intermediate_response = self._get_terms_data()
        self.assertGreater(
            intermediate_response['solvedTerms'], 0,
            "solvedTerms should be greater than 0 after updating a term."
        )

        # Now reset the terms
        self._reset_terms()

        # Verify that solvedTerms is reset to zero
        reset_response = self._get_terms_data()
        self.assertEqual(
            reset_response['solvedTerms'], 0,
            f"Expected solvedTerms to be 0 after reset. Got {reset_response['solvedTerms']} instead."
        )

    def _get_question(self, term=None):
        """Helper method to retrieve a question."""
        url = f"{self.base_url}/get_question"
        payload = {"userID": self.userID}
        if term:
            payload["term"] = term  # Add specific term to the payload if provided

        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, "Failed to retrieve question")
        
        question_data = response.json()
        self.assertIsInstance(question_data, dict, "Question data should be a dictionary")
        
        # Ensure the required keys are present
        required_keys = {"question", "option1", "option2", "option3", "option4", "answer"}
        self.assertTrue(
            required_keys.issubset(question_data.keys()),
            f"Missing keys in question data. Expected: {required_keys}, Got: {question_data.keys()}"
        )

        return question_data

    def test_get_question(self):
        """Test the /get_question endpoint."""
        # Retrieve a random question and validate the response structure
        question_data = self._get_question()

        # Print the question data for debugging purposes (optional)
        print("Retrieved Question Data:", question_data)

    def _pass_all_terms(self):
        """Helper method to pass all terms."""
        url = f"{self.base_url}/pass_all_terms"
        payload = {"userID": self.userID}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200, "Failed to pass all terms")

    def test_pass_all_terms_and_switch_specificity(self):
        """Test that passing all terms switches specificity and eventually completes all terms."""

        # Helper to check if solvedTerms resets after passing all terms
        def assert_solved_terms_reset():
            terms_data = self._get_terms_data()
            self.assertEqual(
                terms_data['solvedTerms'], 0,
                "Expected solvedTerms to reset to 0 after passing all terms at current specificity."
            )

        # Pass terms for the first specificity level (e.g., 'foundational')
        self._pass_all_terms()
        assert_solved_terms_reset()  # Verify that solvedTerms is reset

        # Pass terms for the second specificity level (e.g., 'intermediate')
        self._pass_all_terms()
        assert_solved_terms_reset()  # Verify that solvedTerms is reset

        # Pass terms for the third specificity level (e.g., 'special topics')
        self._pass_all_terms()

        # Now that all terms are passed, solvedTerms should not reset anymore
        final_terms_data = self._get_terms_data()
        self.assertGreater(
            final_terms_data['solvedTerms'], 0,
            "Expected solvedTerms to remain greater than 0 after completing all terms."
        )

    # Some more tests we can add: 
    # - Test that getting a question right leads to solvedTerms going up by one
    # - Test that getting a question wrong does not affect solvedTerms
    # - Test that totalTerms changes for each specificity level
    # - Add endpoint that somehow gets which modules and specificities are locked and unlocked (9 total)
    # Then you can add the part where for each wrong answer there is a hierarchy that updates in the backend in a json file.


    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        if cls.local_terms_path.exists():
            os.remove(cls.local_terms_path)

if __name__ == '__main__':
    unittest.main()
