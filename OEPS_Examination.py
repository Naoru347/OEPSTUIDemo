import json
import random
from datetime import datetime

DATA_FILE = "OEPS_data.json"

QUESTIONS_BANK = {
    1:
    [
        "Can you give us a brief professional introduction, including your academic background and current research focus?",
        "How would you describe your primary research interests and their significance in the broader context of your field?",
        "What motivated you to pursue your specific area of study within your field?",
        "Can you share a recent project you worked on, highlighting your role and contributions?",
        "What are your future career aspirations, and how do you see your current research contributing to those goals?"
    ],
    2:
    [
        "Can you explain the procedure for submitting assignments in your course?",
        "How do you handle late submissions or requests for extensions?",
        "What is your policy on academic integrity and plagiarism?",
        "How are grades determined in your course?",
        "What should a student do if they need extra help outside of class?"
    ], 
    3:
    [
        "Please begin your mini-lesson now. I'll ask a few Q & A questions at the end. You have 5-6 minutes for your demo mini-lesson."
    ]
}

QUESTION_WEIGHTS = {1: 0.20, 2: 0.30, 3: 0.50}

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=2)

def validate_name(prompt, min_length=2):
    while True: 
        name = input(prompt).strip()
        if(len(name) >= min_length and name.replace(' ', '').replace('-', '').isalpha()):
            return name
        else:
            print(f"Please enter a valid name that is at least {min_length} charactes long using letters, spaces, and hypens only: ")

def get_examiner_name():
    return validate_name("\nEnter EXAMINER name: ")

def get_student_name():
    return validate_name("\nEnter STUDENT name: ")

def get_notes():
    notes = []
    print("Enter notes (type 'stop' on a new line to finish):")
    while True:
        note = input().strip()
        if note.lower() == 'stop':
            break
        notes.append(note)
    return notes

def get_question_data(num):
    question = random.choice(QUESTIONS_BANK[num])
    print(f"Question {num}: {question}")
    notes = get_notes()
    question_score = get_score("Enter a score between 1 and 3: ")
    return{"question": question, "notes": notes, "question score": question_score}

def get_score(prompt, max_attempts=3):
    for _ in range(max_attempts):
        try:
            score = int(input(prompt))
            if 1 <= score <= 3:
                return score
            print("Score must be between 1 and 3: ")
        except ValueError:
            print("Please enter a valid number.")
    print(f"Maximum attempts ({max_attempts}) reached. Defaulting to score 1.")
    return 1    

def calculate_total_score(questions):
    # Calcuate the totale score by getting the weighted value of each questions score 
    # and summing them together
    total_score = sum(q['question score'] * QUESTION_WEIGHTS[i+1] for i, q in enumerate(questions))
    return round(total_score, 2)

def determine_band(total_score):
    if 0 <= total_score <= 1.99:
        return "No Pass"
    elif 2 <= total_score < 2.99:
        return "Low Pass"
    elif total_score == 3:
        return "High Pass"
    else:
        return "Invalid Score"  # This is a safeguard for unexpected scores

def get_EAP_requirement(total_score):
    if total_score < 2:
        return "EAP 6016 REQUIRED"
    else:
        return "EAP 6016 NOT REQUIRED"

def create_new_entry(examiner, student): 
    # Set up our data entry
    entry = {
        "examiner": examiner, 
        "student": student,
        "date": datetime.now().isoformat(),
        "questions":[]
    }

    # Pull the questions at random from the questions list
    # And display that question before getting notes and a score
    # Append that data to our entry
    for i in range(1, 4):
        entry["questions"].append(get_question_data(i))

    # Add a total score item to our entry using helper function
    entry["total score"] = calculate_total_score(entry["questions"])

    # Identify the student's band for internal report
    entry["band"] = determine_band(entry["total score"])

    # Identify the student's EAP requirement
    entry["EAP requirement"] = get_EAP_requirement(entry["total score"])

    #debuggin printly
    # print(entry)
    return entry

def main():
    # Start with loading the data
    data = load_data()
    # Get the name of the examiner
    examiner = get_examiner_name()
    # Get the student examinee's name
    student = get_student_name()
    # Begin examination loop
    new_entry = create_new_entry(examiner, student)
    #Append new entry to loaded data
    data.append(new_entry)
    # Save the data to the JSON file
    save_data(data)
    # Debugging printlns
    # print(data)
    # print(examiner)
    # print(student)
    # print(data)

if __name__ == "__main__":
    main()