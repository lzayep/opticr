from pathlib import PurePath

from PIL import Image
import pytesseract
import pdf2image

from .baseocr import BaseOcr


class TesseractOcr(BaseOcr):
    name: str = "tesseract"

    def __init__(self) -> None:
        pass

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
            pages_ocr.append(pytesseract.image_to_string(page))
        return pages_ocr
