from typing_extensions import TypeAlias

from .ocr.googlevision import GoogleVisionOcr
from .ocr.tesseract import TesseractOcr

OCR: TypeAlias = TesseractOcr | GoogleVisionOcr


class OpticR:
    processors: dict[str, type[OCR]] = {
        "tesseract": TesseractOcr,
        "google-vision": GoogleVisionOcr,
    }

    def __init__(self, processor: str = "tesseract") -> None:
        self.processor: OCR = self.processors[processor]()

    def get_pages(self, filepath: str) -> list[str]:
        return self.processor.get_pages(filepath)

    def processor_name(self) -> str:
        return self.processor.name
