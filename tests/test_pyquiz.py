from apps.quiz import Quiz
import os

TEST_QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "test_questions.json")

def create_temp_questions_file(tmp_path):
    file_path = tmp_path / "questions.json"
    with open(TEST_QUESTIONS_PATH, "r") as src, open(file_path, "w") as dst:
        dst.write(src.read())
    return str(file_path)


def test_load_questions(tmp_path):
    questions_file = create_temp_questions_file(tmp_path)
    quiz = Quiz(questions_file=questions_file)
    assert quiz.total_questions == 2
    assert quiz.questions[0]["question"] == "What is the capital of France?"


def test_run_quiz(monkeypatch, tmp_path, capsys):
    questions_file = create_temp_questions_file(tmp_path)
    quiz = Quiz(questions_file=questions_file)
    answers = iter(["a", "a"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    quiz.run()
    out = capsys.readouterr().out
    assert "Welcome to PyQuiz" in out
    assert "Question 1/2" in out
    assert "Question 2/2" in out
    assert "Correct" in out
    assert "Incorrect" in out
    assert "Quiz Complete" in out


def test_check_answer():
    quiz = Quiz(questions_file=None)
    assert quiz.check_answer("a", "A")
    assert not quiz.check_answer("b", "a")
