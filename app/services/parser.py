import re

def parse_mcq(text: str):
    """
    Parses multiple-choice questions from the text.
    Returns a list of dicts:
    [
        {
            "question": "What is 2+2?",
            "choices": {"A": "3", "B": "4", "C": "5", "D": "6"}
        },
        ...
    ]
    """
    questions = []

    # Split by question numbers (assumes format: 1. Question text)
    pattern = re.compile(r"(\d+)\.\s*(.*?)\n(?:A\..*?B\..*?C\..*?D\..*?)(?=\n\d+\.|\Z)", re.DOTALL)
    matches = pattern.findall(text)

    for num, q_block in matches:
        # Extract question text
        question_text = re.split(r"A\.", q_block)[0].strip()

        # Extract choices
        choices_pattern = re.findall(r"([A-D])\.\s*(.*?)\n", q_block)
        choices = {letter: choice for letter, choice in choices_pattern}

        questions.append({"question": question_text, "choices": choices})

    return questions
