class OCR:
    def extract_text(self, image_path):
        return {
            "success": False,
            "text": "",
            "message": (
                "OCR engine is not connected yet."
            ),
            "image": str(image_path),
        }