import json

def process_questions(input_file, correct_output_file, incorrect_output_file):
    with open(input_file, 'r') as file:
        questions = json.load(file)

    correct_lines = []
    incorrect_lines = []

    for section, scenarios in questions.items():
        for scenario, details in scenarios.items():
            correct_answer_key = details['answer']
            correct_answer = details[correct_answer_key]
            correct_lines.append(f"['{scenario}', '{section}', '{correct_answer}']\n")
            
            for option_key in ['option1', 'option2', 'option3', 'option4']:
                if option_key != correct_answer_key:
                    incorrect_answer = details[option_key]
                    incorrect_lines.append(f"['{scenario}', '{section}', '{incorrect_answer}']\n")

    with open(correct_output_file, 'w') as file:
        file.writelines(correct_lines)

    with open(incorrect_output_file, 'w') as file:
        file.writelines(incorrect_lines)

    print(f"Correct responses written to {correct_output_file}")
    print(f"Incorrect responses written to {incorrect_output_file}")

if __name__ == "__main__":
    input_file = 'questions.json'
    correct_output_file = 'correct_response_lists.txt'
    incorrect_output_file = 'incorrect_response_lists.txt'
    process_questions(input_file, correct_output_file, incorrect_output_file)
