from typing_extensions import TypeAlias

from .fetchdocument import download
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

    async def get_pages(self, filepath: str) -> list[str]:
        localpath: str = await download(filepath)
        print(localpath)
        return self.processor.get_pages(localpath)

    def processor_name(self) -> str:
        return self.processor.name
