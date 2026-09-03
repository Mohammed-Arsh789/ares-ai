class VisionModel:
    def analyze(self, image_path, question=None):
        return {
            "success": False,
            "image": str(image_path),
            "question": question,
            "message": (
                "Vision model is not connected yet."
            ),
        }