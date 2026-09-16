class CriticRules:
    def check_empty(self, text: str) -> str | None:
        if not text.strip():
            return "Response is empty."

        return None

    def check_length(self, text: str) -> str | None:
        if len(text.strip()) < 20:
            return "Response may be too short to be useful."

        return None

    def check_uncertainty(self, text: str) -> str | None:
        uncertainty_terms = [
            "maybe",
            "possibly",
            "i think",
            "not sure",
        ]

        lowered = text.lower()

        if any(term in lowered for term in uncertainty_terms):
            return (
                "Response contains uncertain language. "
                "Verify important claims."
            )

        return None