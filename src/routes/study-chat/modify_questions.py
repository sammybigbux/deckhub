import json
import random

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_random_answer(answers, current_answer, existing_options):
    available_answers = [ans for ans in answers if ans != current_answer and ans not in existing_options]
    return random.choice(available_answers) if available_answers else ""

def fix_term_questions(data):
    for section, terms in data.items():
        all_answers = []
        for term, term_data in terms.items():
            for option_key in ['option1', 'option2', 'option3', 'option4']:
                if term_data[option_key] != "":
                    all_answers.append(term_data[option_key])
        
        for term, term_data in terms.items():
            existing_options = set(term_data[option_key] for option_key in ['option1', 'option2', 'option3', 'option4'] if term_data[option_key] != "")
            for option_key in ['option1', 'option2', 'option3', 'option4']:
                if term_data[option_key] == "":
                    term_data[option_key] = get_random_answer(all_answers, term_data['answer'], existing_options)
                    existing_options.add(term_data[option_key])
    return data

def main():
    input_file = 'term_questions.json'
    output_file = 'term_questions_fixed.json'

    term_questions = read_json_file(input_file)
    fixed_term_questions = fix_term_questions(term_questions)
    write_json_file(fixed_term_questions, output_file)

if __name__ == "__main__":
    main()
