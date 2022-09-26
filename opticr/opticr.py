from pathlib import PurePath

from PIL import Image
import pytesseract
import pdf2image


class OpticR:
    def __init__(self) -> None:
        pass

    def get_pages(self, filepath: str) -> list[str]:
        _ = filepath
        return []

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
