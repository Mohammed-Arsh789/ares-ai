from .models import QuizQuestion, QuizResult


class QuizEngine:
    def create_question(
        self,
        question: str,
        correct_answer: str,
        explanation: str = "",
    ) -> QuizQuestion:
        return QuizQuestion(
            question=question,
            correct_answer=correct_answer,
            explanation=explanation,
        )

    def evaluate(
        self,
        questions: list[QuizQuestion],
        answers: list[str],
    ) -> QuizResult:
        correct = 0
        incorrect_questions = []

        for question, answer in zip(questions, answers):
            if answer.strip().lower() == question.correct_answer.strip().lower():
                correct += 1
            else:
                incorrect_questions.append(question.question)

        return QuizResult(
            total=len(questions),
            correct=correct,
            incorrect_questions=incorrect_questions,
        )