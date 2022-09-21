import pytest

from opticr import OpticR


@pytest.fixture(autouse=True)
def ocr() -> OpticR:
    return OpticR()


def test_init_opticr() -> None:
    assert OpticR()


def test_get_pages(ocr: OpticR) -> None:
    assert ocr.get_pages("data/contract.pdf") == []
