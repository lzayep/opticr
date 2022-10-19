from typing import Literal
from .baseocr import BaseOcr


class GoogleVisionOcr(BaseOcr):
    name: str = "google-vision"

    def __init__(self, language: Literal['en', 'de'] = 'en') -> None:
        self.language = language

    def get_pages(self, filepath: str) -> list[str]:
        raise NotImplementedError

    def ocr(self, document_path: str) -> list[str]:
        raise NotImplementedError
