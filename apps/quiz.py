import json
import os
import sys




class Quiz:
    """Main Quiz class that handles quiz logic and user interaction."""

    def __init__(self, questions_file: str = "../data/questions.json"):
        """Initialize the quiz with questions from a JSON file."""
        self.questions_file = questions_file
        self.questions = []
        self.score = 0
        self.total_questions = 0
        self.load_questions()

    def load_questions(self):
        """Load questions from JSON file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        questions_path = os.path.join(script_dir, self.questions_file)

        try:
            with open(questions_path) as f:
                data = json.load(f)
                self.questions = data.get("questions", [])
                self.total_questions = len(self.questions)
        except FileNotFoundError:
            print(f"Error: Questions file '{self.questions_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{self.questions_file}'.")
            sys.exit(1)

    def display_welcome(self):
        """Display welcome message."""
        print("\n" + "=" * 60)
        print("  Welcome to PyQuiz - Interactive Terminal Quiz")
        print("=" * 60)
        print(f"\nYou will be asked {self.total_questions} questions.")
        print("Type the letter of your answer (a, b, c, or d) and press Enter.")
        print("=" * 60 + "\n")



    def display_question(self, question_num: int, question: dict):
        """Display a single question with its options."""
        print(f"\nQuestion {question_num}/{self.total_questions}")
        print("-" * 60)
        print(f"Q: {question['question']}")
        print()

        for option_key, option_value in question["options"].items():
            print(f"  {option_key}) {option_value}")
        print()

    def get_user_answer(self) -> str:
        """Get and validate user input."""
        valid_options = ["a", "b", "c", "d"]

        while True:
            answer = input("Your answer: ").strip().lower()

            if answer in valid_options:
                return answer
            else:


                print("Invalid input. Please enter a, b, c, or d.")

    def check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Check if the user's answer is correct."""
        return user_answer == correct_answer.lower()

    def display_result(
        self, is_correct: bool, correct_answer: str, explanation: str = None
    ):
        """Display whether the answer was correct or incorrect."""
        if is_correct:

            print("✓ Correct!")
            self.score += 1
        else:
            print(f"✗ Incorrect. The correct answer was: {correct_answer.upper()}")

        if explanation:
            print(f"Explanation: {explanation}")

        print()

    def display_final_score(self):
        """Display the final score and percentage."""
        percentage = (
            (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0
        )

        print("\n" + "=" * 60)
        print("  Quiz Complete!")
        print("=" * 60)
        print(f"\nYour Score: {self.score}/{self.total_questions}")
        print(f"Percentage: {percentage:.1f}%")

        if percentage == 100:
            print("Grade: Perfect! Outstanding performance! 🌟")
        elif percentage >= 80:
            print("Grade: Excellent! Great job! 🎉")
        elif percentage >= 60:
            print("Grade: Good! Well done! 👍")
        elif percentage >= 40:
            print("Grade: Fair. Keep practicing! 📚")
        else:
            print("Grade: Needs improvement. Don't give up! 💪")

        print("=" * 60 + "\n")

    def run(self):
        """Main method to run the quiz."""
        if not self.questions:
            print(
                "No questions available. Please add questions to the questions.json file."
            )
            return

        self.display_welcome()

        for i, question in enumerate(self.questions, 1):
            self.display_question(i, question)
            user_answer = self.get_user_answer()
            is_correct = self.check_answer(user_answer, question["correct_answer"])
            self.display_result(
                is_correct, question["correct_answer"], question.get("explanation")
            )

        self.display_final_score()
