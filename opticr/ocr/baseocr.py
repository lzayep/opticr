from abc import ABC, abstractmethod
from functools import lru_cache


class BaseOcr(ABC):
    name: str = "baseocr"

    def get_pages(self, filepath: str, cache=False) -> list[str]:
        if cache:
            return self.ocr_cache(filepath)
        return self.ocr(filepath)

    @abstractmethod
    def ocr(self, document_path: str) -> list[str]:
        raise NotImplementedError("")

    @lru_cache
    def ocr_cache(self, document_path: str) -> list[str]:
        return self.ocr(document_path)
