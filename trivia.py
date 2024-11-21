'''
This is for being able to ask the user questions for a quiz/triva game
'''

import random
import json
import html

#file imports
from tools import *

class Trivia():
    def __init__(self):
        with open("data/datasets/trivia.json") as f:
            self.data = json.load(f)
        self.score = 0

    def ask_questions(self, data):
        for i, question in enumerate(data):
            question_text = html.unescape(question['question'])

            if question['type'] == 'boolean':
                print(f"Question {i+1}: True or False: {question_text}")
                answer = input().lower()
                if answer == question['correct_answer'].lower():
                    score += 1
                    print("Correct!")
                elif "stop" in answer or "exit" in answer or "quit" in answer or "end" in answer or "done" in answer or "finish" in answer or "leave" in answer or "break" in answer or "cancel" in answer or "abort" in answer:
                    print("No worries, we can finish the quiz here")
                    break
                else:
                    print(f"Incorrect! The correct answer was: {question['correct_answer']}")
            elif question['type'] == 'multiple':
                print(f"Question {i+1}: {question_text}")
                options = question['incorrect_answers'] + [question['correct_answer']]
                random.shuffle(options)
                print("\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)]))
                answer = input("")
                if options[int(answer)-1] == question['correct_answer']:
                    self.score += 1
                    print("Correct!")
                elif "stop" in answer or "exit" in answer or "quit" in answer or "end" in answer or "done" in answer or "finish" in answer or "leave" in answer or "break" in answer or "cancel" in answer or "abort" in answer:
                    print("No worries, we can finish the quiz here")
                    break
                else:
                    print(f"Incorrect! The correct answer was: {question['correct_answer']}")
            print()

        print(f"Quiz finished! Your score: {self.score}/{len(data)}")

    def start_quiz(self):
        # Ask the user for difficulty level
        difficulty = input("Of course, first, choose a difficulty (easy, medium, hard) you don't have to choose if you don't want: ").lower()
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = None
        
        # Ask the user for the number of questions
        num_questions = input("How many questions would you like? ")
        num_questions = int(num_questions)

        # Filter trivia data based on difficulty
        if difficulty is None:
            filtered_data = random.sample(self.data, num_questions)
        else:
            filtered_data = [q for q in self.data if q['difficulty'] == difficulty]

        # Randomly select the required number of questions
        if len(filtered_data) >= num_questions:
            quiz_data = random.sample(filtered_data, num_questions)
        else:
            quiz_data = filtered_data  # If there are not enough questions, use all available

        # Start the quiz
        self.ask_questions(quiz_data)

    def get_quiz_intent(self, intent):
        if intent == "play trivia": self.start_quiz()
        else: return 0
