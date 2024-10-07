import tempfile
from typing import Literal

from ant31box.clients import filedl_client
from typing_extensions import TypeAlias

from opticr.ocr.googlevision import GoogleVisionOcr
from opticr.ocr.tesseract import TesseractOcr

OCR: TypeAlias = TesseractOcr | GoogleVisionOcr


class OpticR:
    processors: dict[str, type[OCR]] = {
        "tesseract": TesseractOcr,
        "google-vision": GoogleVisionOcr,
    }

    def __init__(
        self, processor: str = "tesseract", language: Literal["eng", "deu"] = "eng"
    ) -> None:
        self.processor: OCR = self.processors[processor](language)

    async def get_pages(
        self, filepath: str, dest_dir: str = "", cache: bool = False
    ) -> list[str]:
        tmpdir = None
        if dest_dir == "":
            # pylint: disable=consider-using-with
            tmpdir = tempfile.TemporaryDirectory()
            dest_dir = tmpdir.name

        localpath = (
            await filedl_client().download(source=filepath, dest_dir=dest_dir)
        ).path
        if localpath is None:
            raise FileNotFoundError(f"File {filepath} not found")
        res = self.processor.get_pages(str(localpath), cache=cache)
        if tmpdir is not None:
            tmpdir.cleanup()
        return res

    def processor_name(self) -> str:
        return self.processor.name
