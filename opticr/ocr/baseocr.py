from abc import ABC, abstractmethod


class BaseOcr(ABC):
    name: str = "baseocr"

    @abstractmethod
    def get_pages(self, filepath: str) -> list[str]:
        raise NotImplementedError("")

    @abstractmethod
    def ocr(self, document_path: str) -> list[str]:
        raise NotImplementedError("")
