from .reviewer import ResponseReviewer


class CriticAgent:
    def __init__(self):
        self.reviewer = ResponseReviewer()

    def review(self, response: str):
        return self.reviewer.review(response)