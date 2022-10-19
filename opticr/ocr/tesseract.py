from pathlib import PurePath
from typing import Literal
import pdf2image
import pytesseract
from PIL import Image

from .baseocr import BaseOcr


class TesseractOcr(BaseOcr):
    name: str = "tesseract"

    def __init__(self, language: Literal['en', 'de'] = 'en') -> None:
        self.language = language

    def get_pages(self, filepath: str) -> list[str]:
        return self.ocr(filepath)

    def ocr(self, document_path: str) -> list[str]:
        path = PurePath(document_path)
        if path.suffix == ".pdf":
            pages = pdf2image.convert_from_path(str(path))
        else:
            pages = [Image.open(str(path))]
        pages_ocr = []
        for page in pages:
            pages_ocr.append(pytesseract.image_to_string(page, lang=self.language))
        return pages_ocr
