import json
import random
import time
from pathlib import Path

class TermManager:
    SPECIFICITY_ORDER = ["foundational", "intermediate", "special topics"]

    def __init__(self, module_name="learn_data", userID=None):
        self.module = module_name
        self.userID = userID
        self.terms_path = Path(userID) / f"{module_name}_terms.json"
        self.hierarchy_path = Path(userID) / f"hierarchy.json"
        self.hierarchy = self._read_json_hierarchy()
        self.section = "Account Management"  # Default section; can be set dynamically
        self.terms = self._read_json_terms()  # Read terms.json on initialization
        self.specificity = self._figure_out_specificity()  # Default specificity; can be set dynamically
        self.total_terms, self.total_specificity_terms = self._calculate_total_terms()
        self.solved_terms = self._calculate_solved_terms()
        self.number_incorrect = -1
        if module_name == "apply_data":
            self.number_incorrect = self._get_number_incorrect() # number you got incorrect in the diagnostic module
        self.number_completed = self._get_number_completed() # number of terms you have completed in this module
        self.total = 0
        self.section_order = [
            "Account Management",
            "Services",
            "Auto Scaling Group",
            "Cloudshell",
            "Edge Functions",
            "Data and Databases",
            "Machine Learning",
            "CloudFront",
            "S3 Basics",
            "Containers on AWS",
            "EC2 advanced",
            "Access Management",
            "Disaster Recovery",
            "S3 Security",
            "IAM",
            "DNS",
            "Monitoring and Auditing",
            "S3 Advanced",
            "Data Analytics",
            "Snow Family",
            "Serverless",
            "EC2 Basics",
            "Decoupling Applications",
            "Encryption",
            "EC2 Instance Storage",
            "AWS Fundamentals",
            "High Availability and Scalability",
            "Networking"
        ]
        

    def _get_number_completed(self):
        count = 0
        for category in self.terms.values():
            for level in category.values():
                count += sum(1 for value in level.values() if value is True)
        return count
    
    def _get_number_incorrect(self):
        count = sum(1 for item in self.hierarchy.values() if item.get("weight", 0) > 0)
        return count

    def _figure_out_specificity(self):
        """
        Determine the specificity level based on terms.json.
        If any 'false' values are found in a specificity level, return that level.
        """
        for specificity in self.SPECIFICITY_ORDER:  # Check specificity levels in order
            # Iterate over all sections (e.g., "Account Management", "Services")
            for section, terms_by_specificity in self.terms.items():
                if specificity in terms_by_specificity:
                    # Check if any term within this specificity level is marked as False
                    for term, value in terms_by_specificity[specificity].items():
                        if not value:  # If the term is not solved
                            return specificity  # Return the current specificity level

        # If all terms are solved, return the highest specificity level
        return self.SPECIFICITY_ORDER[-1]

    def _build_term_weight_lookup(self):
        """Precompute a lookup table of term weights from the hierarchy."""
        print("Building term weight lookup table...")
        weights = {}

        # Traverse the hierarchy and collect term weights based on the module type
        for scenario in self.hierarchy.values():
            if self.module == "understand_data":
                # Collect weights for second-level concepts
                for concept_name, concept_data in scenario.get('downstream', {}).items():
                    weights[concept_name] = concept_data.get('weight', 0)

            elif self.module == "learn_data":
                # Collect weights for bottom-level terms (leaf nodes)
                for concept_data in scenario.get('downstream', {}).values():
                    # Ensure downstream structure is a dictionary
                    downstream_terms = concept_data.get('downstream', {})
                    if isinstance(downstream_terms, dict):
                        for term_name, weight in downstream_terms.items():
                            if weight > 0:  # Only include terms with weight > 0
                                weights[term_name] = weight

        return weights  # Return the flattened lookup table


    def _read_json_terms(self):
        """Read the user's terms.json, filtering terms based on hierarchy.json weights."""

        # Ensure the user directory exists
        user_dir = self.terms_path.parent
        user_dir.mkdir(parents=True, exist_ok=True)

        # Load terms.json
        with open(self.terms_path, 'r') as f:
            all_terms = json.load(f)

        if self.module == "apply_data":
            return all_terms

        # Build a lookup table for term weights from hierarchy.json
        term_weights = self._build_term_weight_lookup()

        # If not "apply_data", filter terms based on hierarchy weights
        filtered_terms = {}

        # Iterate through sections and specificities
        for section, specificities in all_terms.items():
            filtered_specificities = {}

            for specificity, terms in specificities.items():
                if self.module == "understand_data":
                    # Filter second-level terms based on their weight in term_weights
                    filtered_terms_for_specificity = {
                        term: value
                        for term, value in terms.items()
                        if term_weights.get(term, 0) > 0
                    }

                elif self.module == "learn_data":
                    # Filter third-level (leaf) terms based on their weight in term_weights
                    filtered_terms_for_specificity = {
                        term: value
                        for term, value in terms.items()
                        if term in term_weights and term_weights[term] > 0
                    }

                if filtered_terms_for_specificity:
                    filtered_specificities[specificity] = filtered_terms_for_specificity

            if filtered_specificities:
                filtered_terms[section] = filtered_specificities
        return filtered_terms  # Return the filtered terms
                
        
    def _read_json_hierarchy(self):
        """Read the user's hierarchy.json."""
        user_dir = self.hierarchy_path.parent
        user_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.hierarchy_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Hierarchy file not found. Returning an empty dictionary.")
            return {}
    
    def submit_hierarchy_changes(self):
        """Submit changes to the hierarchy by updating the saved JSON file."""

        with open(self.hierarchy_path, 'w') as f:
            json.dump(self.hierarchy, f, indent=4)

    def write_terms_to_file(self):
        # there is something wrong with the section progress, it doesn't match with the data sent to cleanup_env which you can see in the console.
        """Write the stored terms to the user's terms.json, merging only true values."""

        # Write the updated terms back to terms.json
        with open(self.terms_path, 'w') as f:
            json.dump(self.terms, f, indent=4)

        with open("terms_write_test.json", 'w') as f:
            json.dump(self.terms, f, indent=4)

        # Submit section progress for the user manager
        section_progress_data = self.get_section_data()
        print(f"Section progress data within term_manager.write_terms_to_file() before calculating sections completed: {section_progress_data}")

        # Calculate sections_completed and sections_total
        sections_completed = sum(section["progressValue"] for section in section_progress_data)
        sections_total = sum(section["progressMax"] for section in section_progress_data)

        # Create section progress dictionary
        section_progress = {
            "sections_completed": sections_completed,
            "sections_total": sections_total
        }
        
        # Return section progress
        return section_progress


    def _calculate_total_terms(self):
        """Calculate the total number of terms for the current specificity."""
        total_specificity_terms = 0  # Initialize the counter for the current specificity
        total_terms = 0  # Initialize the counter for all specificities

        # Iterate over all sections
        for section_name, section_content in self.terms.items():
            # Add the number of terms in all specificities to the total_terms counter
            total_terms += sum(len(terms) for terms in section_content.values())

            # Check if the current specificity exists in this section
            if self.specificity in section_content:
                # Add the number of terms in the current specificity
                total_specificity_terms += len(section_content[self.specificity])

        return total_terms, total_specificity_terms


    def _calculate_solved_terms(self):
        """Calculate the total number of solved terms for the current specificity."""
        return sum(
            1
            for section in self.terms.values()
            if self.specificity in section  # Check if the current specificity exists in the section
            for term, solved in section[self.specificity].items()
            if solved  # Count only solved terms (True)
        )


    def _update_specificity(self):
        """Advance specificity when all terms in the current level are solved."""
        if self.solved_terms == self.total_specificity_terms:
            current_index = self.SPECIFICITY_ORDER.index(self.specificity)
            if current_index < len(self.SPECIFICITY_ORDER) - 1:
                    self.specificity = self.SPECIFICITY_ORDER[current_index + 1]
                    self.update_term_data()
                    self.solved_terms = 0
                    print(f"Specificity advanced to {self.specificity}.")
        else:
            return None

    def _all_terms_solved_in_specificity(self, specificity):
        """Check if all terms in the given specificity level are solved."""
        return self.solved_terms == self.total_specificity_terms
    
    def get_section_data(self):
        """Returns the completed sections for each specificity level."""
        SECTIONS_DATA = []
        # Define the sections and descriptions
        section_definitions = [
            {
                "title": "Foundational",
                "description": "Build your foundation on concepts essential to proceeding.",
            },
            {
                "title": "Intermediate",
                "description": "Take your knowledge of concepts to the next level, achieving a well-rounded understanding.",
            },
            {
                "title": "Special Topics",
                "description": "Master special topics by applying the knowledge gained from previous sections.",
            },
        ]

        for i, section_def in enumerate(section_definitions):
            title = section_def["title"].lower()
            
            # Initialize section data structure
            section_data = {
                "title": section_def["title"],
                "description": section_def["description"],
                "isLocked": i != 0,  # Lock all but the first section initially
                "progressValue": 0,
                "progressMax": 0,
                "sections": []
            }

            # Track completion status for determining the active section
            active_set = False

            for topic, levels in self.terms.items():
                # Only proceed if the topic has the current level (e.g., "foundational" or "intermediate")
                if title in levels:
                    # Increment the maximum progress count for each section within the topic
                    section_data["progressMax"] += 1
                    
                    # Check if the current topic's level is completed
                    is_completed = all(levels[title].values())
                    if is_completed:
                        section_data["progressValue"] += 1

                    # Define the topic section structure
                    section_info = {
                        "title": topic,
                        "isCompleted": is_completed,
                        "isActive": False  # Default to inactive
                    }

                    # Set the first incomplete section as active if not locked
                    if not active_set and not is_completed and not section_data["isLocked"]:
                        section_info["isActive"] = True
                        active_set = True  # Prevent further sections from being marked active

                    # Add this topic to the section list
                    section_data["sections"].append(section_info)

            # Mark the last section as "isEndSection"
            if section_data["sections"]:
                section_data["sections"][-1]["isEndSection"] = True

            # Append the section data to the main list
            SECTIONS_DATA.append(section_data)
        print("SECTIONS DATA returned by get_section_data in term_manager.py: ", SECTIONS_DATA)

        return SECTIONS_DATA
    
    def get_term_list(self, active_section):
        """Get the list of terms for the active section with completion status."""

        # Initialize an empty list to hold the transformed terms
        terms_list = []

        # Get the terms for the active section and specificity
        terms = self.terms.get(active_section, {}).get(self.specificity, {})

        # Iterate over terms to build the list with id and isCompleted fields
        for idx, (term, is_completed) in enumerate(terms.items(), start=1):
            terms_list.append({
                "id": idx,
                "isCompleted": is_completed,
                "title": term
            })


        return terms_list


    def update_progress(self, term):
        """Update progress of a term."""
        try:
            if not self.terms[self.section][self.specificity][term]:
                self.terms[self.section][self.specificity][term] = True
                self.solved_terms += 1
                self._update_specificity()  # Check if specificity needs to advance
        except KeyError:
            raise ValueError(f"Term '{term}' not found in section '{self.section}' with specificity '{self.specificity}'")
        
    def update_incorrect(self, name):
        """
        Update the 'weight' for the given name at the level specified
        by self.module (either 'apply_data', 'understand_data', or 'learn_data').
        If the item is incorrect, its weight increases by 1, and all downstream items get 0.5 added.
        """
        if self.module not in {"apply_data", "understand_data", "learn_data"}:
            raise ValueError("Invalid module name. Must be 'apply_data', 'understand_data', or 'learn_data'.")

        def increment_downstream_weights(downstream):
            """Recursively add 0.5 to the 'weight' of all downstream elements."""
            for key, item in downstream.items():
                if isinstance(item, dict):
                    # Add 0.5 to the weight at this level
                    item['weight'] = item.get('weight', 0) + 0.5

                    # Continue recursively if there are more nested elements
                    if 'downstream' in item:
                        increment_downstream_weights(item['downstream'])
                elif isinstance(item, (int, float)):  # Handling numerical leaf nodes
                    # Update the numerical leaf node directly
                    downstream[key] += 0.5

        # Apply updates based on the specified module level
        if self.module == "apply_data":  # Top level
            if name in self.hierarchy:
                entry = self.hierarchy[name]
                entry['weight'] = entry.get('weight', 0) + 1  # Increment weight by 1
                if 'downstream' in entry:
                    increment_downstream_weights(entry['downstream'])
            else:
                raise KeyError(f"Entry '{name}' not found at the 'apply_data' level.")

        elif self.module == "understand_data":  # Middle level
            found = False
            for scenario in self.hierarchy.values():
                if name in scenario.get('downstream', {}):
                    concept = scenario['downstream'][name]
                    concept['weight'] = concept.get('weight', 0) + 1  # Increment weight by 1
                    if 'downstream' in concept:
                        increment_downstream_weights(concept['downstream'])
                    found = True
                    break
            if not found:
                raise KeyError(f"Concept '{name}' not found at the 'understand_data' level.")

        elif self.module == "learn_data":  # Bottom level
            found = False
            for scenario in self.hierarchy.values():
                for concept in scenario.get('downstream', {}).values():
                    if name in concept.get('downstream', {}):
                        # Increment the weight of the term (numerical value)
                        concept['downstream'][name] += 1  # Directly increment leaf node
                        found = True
                        break
                if found:
                    break
            if not found:
                raise KeyError(f"Term '{name}' not found at the 'learn_data' level.")


    def get_not_passed_terms(self):
        """Retrieve terms that haven't been solved yet in the current specificity.
        If no terms are unsolved in the current section, iterate through other sections
        to find unsolved terms at the same specificity level, updating self.section."""
        
        print(f"Starting get_not_passed_terms. Current section: {self.section}, specificity: {self.specificity}")

        # Get unsolved terms in the current section and specificity
        not_passed_terms = [
            term for term, solved in self.terms.get(self.section, {}).get(self.specificity, {}).items() if not solved
        ]
        print(f"Unsolved terms in section '{self.section}' with specificity '{self.specificity}': {not_passed_terms}")

        # If there are unsolved terms, return them
        if not_passed_terms:
            print(f"Returning unsolved terms: {not_passed_terms}")
            return not_passed_terms

        # Otherwise, iterate through other sections to find unsolved terms in the same specificity
        section_index = self.section_order.index(self.section)
        print(f"Current section index: {section_index}, total sections: {len(self.section_order)}")

        if section_index + 1 == len(self.section_order):
            print(f"No more sections to check. Current specificity: {self.specificity}")
            if self.specificity == "special topics":
                print("Reached the end of specificity levels. Returning None.")
                return None
            else:
                # Move to the next specificity level
                next_specificity_index = self.SPECIFICITY_ORDER.index(self.specificity) + 1
                self.specificity = self.SPECIFICITY_ORDER[next_specificity_index]
                print(f"Moved to next specificity level: {self.specificity}")
        else:
            # Move to the next section
            self.section = self.section_order[section_index + 1]
            print(f"Moved to next section: {self.section}")

        # Recursive call to check the new section or specificity
        print(f"Recursively calling get_not_passed_terms with section '{self.section}' and specificity '{self.specificity}'")
        return self.get_not_passed_terms()


    def get_remaining_terms(self):
        """Get unsolved terms in the current specificity."""
        return "\n".join(
            term for term, solved in self.terms.get(self.section, {}).get(self.specificity, {}).items() if not solved
        )

    def get_total_specificity_terms(self):
        """Return the total number of terms."""
        return self.total_specificity_terms
    
    def update_term_data(self):
        self.total_specificity_terms = self._calculate_total_terms()
        self.solved_terms = self._calculate_solved_terms()

    def reset_all_terms(self):
        """Reset all terms to unsolved."""
        for section in self.terms:
            for specificity in self.terms[section]:
                for term in self.terms[section][specificity]:
                    self.terms[section][specificity][term] = False
        self.solved_terms = 0

    def get_solved_terms(self):
        """Return the number of solved terms."""
        return self.solved_terms

    def pass_all_terms(self):
        """Mark all terms as solved."""
        for section in self.terms:
            for specificity in self.terms[section]:
                if specificity == self.specificity:
                    for term in self.terms[section][specificity]:
                        self.terms[section][specificity][term] = True
        self.solved_terms = self.total_specificity_terms
        self._update_specificity()


    def get_remaining_sections(self):
        """Get sections with unsolved terms."""
        start_time = time.time()
        result = "\n".join(
            section
            for section, specificities in self.terms.items()
            if any(not all(terms.values()) for terms in specificities.values())
        )
        return result

    def retrieve_question(self, data, term=None, section=None):
        """Retrieve a question for the given section, specificity, and optional term."""
        # If no term is provided, get the list of unsolved terms in the current section and specificity
        self.section = section if section else self.section
        if term is None:
            terms = self.get_not_passed_terms()  # Filtered by self.section and self.specificity

            if not terms:
                return "No more terms available in any specificity."

            # Randomly select a term if one wasn't specified
            term = random.choice(terms)

        try:
            # Retrieve the question details from the data
            question_data = data[self.section][term]["questions"]
            question_data["section"] = self.section
            question_data["term"] = term
            if self.module != 'apply_data':
                question_data["related_terms"] = data[self.section][term]["related_terms"]
                question_data["incorrect_response"] = data[self.section][term]["incorrect_response"]
                question_data["correct_response"] = data[self.section][term]["correct_response"]
            else:
                question_data["related_terms"] = None

            return question_data
        except KeyError as e:
            return f"Error retrieving question: {str(e)}"


    def get_rt_from_lookup(self, data, section, term, related_term):
        """Retrieve the related term response."""
        if self.module == 'apply_data':
            return None
        return data[section][term]["related_terms"].get(related_term)

    def get_correct_response(self, data, term):
        """Retrieve the correct response."""
        if self.module == 'apply_data':
            return None
        return data[self.section][term]["correct_response"]

    def get_incorrect_response(self, data, term, answer):
        """Retrieve the incorrect response for a given answer."""
        if self.module == 'apply_data':
            return None
        return data[self.section][term]["incorrect_response"].get(answer)
    
    def get_demo_report(self, data):
        """
        From self.terms and self.hierarchy, create two dictionaries:
        strong_dict and weak_dict, organizing terms and concepts by the parent question.
        """
        import logging

        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        strong_dict = {}
        weak_dict = {}

        # Step 1: Find answered questions
        answered_questions = []
        for section, levels in self.terms.items():
            foundational = levels.get("foundational", {})
            for question, answered in foundational.items():
                if answered:
                    answered_questions.append(question)
                    logger.debug(f"Answered question added: {question}")
                if len(answered_questions) == 10:  # Stop at 10 answered questions
                    break
            if len(answered_questions) == 10:
                break

        # Step 2: Process hierarchy for answered questions
        for question in answered_questions:
            if question in self.hierarchy:
                hierarchy_entry = self.hierarchy[question]
                weight = hierarchy_entry.get("weight", 0)
                downstream = hierarchy_entry.get("downstream", {})

                # Initialize dictionaries for this question
                if weight > 0:
                    weak_dict[question] = {}
                    target_dict = weak_dict
                else:
                    strong_dict[question] = {}
                    target_dict = strong_dict

                logger.debug(f"Processing question: {question}, weight: {weight}, downstream: {downstream}")

                # Iterate through first level of downstream
                for concept, concept_details in downstream.items():
                    target_dict[question][concept] = []

                    # Get second level downstream (leaf nodes)
                    second_level_downstream = concept_details.get("downstream", {})
                    target_dict[question][concept].extend(second_level_downstream.keys())

        logger.debug(f"Final strong_dict: {strong_dict}")
        logger.debug(f"Final weak_dict: {weak_dict}")

        return {
            "strong": strong_dict,
            "weak": weak_dict,
            "number_correct": len(strong_dict),
            "number_incorrect": len(weak_dict),
        }



