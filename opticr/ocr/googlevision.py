from .baseocr import BaseOcr


class GoogleVisionOcr(BaseOcr):
    name: str = "google-vision"

    def get_pages(self, filepath: str) -> list[str]:
        raise NotImplementedError

    def ocr(self, document_path: str) -> list[str]:
        raise NotImplementedError
