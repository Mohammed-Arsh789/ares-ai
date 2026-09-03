from vision.ocr import OCR
from vision.vision_model import VisionModel


class VisionAnalyzer:
    def __init__(self):
        self.ocr = OCR()
        self.model = VisionModel()

    def analyze(
        self,
        image_path,
        question=None,
    ):
        ocr_result = self.ocr.extract_text(
            image_path
        )

        vision_result = self.model.analyze(
            image_path,
            question,
        )

        return {
            "ocr": ocr_result,
            "vision": vision_result,
        }