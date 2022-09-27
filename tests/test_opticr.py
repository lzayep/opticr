import pytest

from opticr import OpticR


@pytest.fixture(
    params=["tesseract", pytest.param("google-vision", marks=pytest.mark.xfail)]
)
def ocr(request: pytest.FixtureRequest) -> OpticR:
    return OpticR(processor=request.param)


def test_init_opticr() -> None:
    assert OpticR()


def test_get_pages_pdf_2pages(ocr: OpticR) -> None:
    pages = ocr.get_pages("tests/data/test-2pages.pdf")
    assert len(pages) == 2
    assert len(pages[0]) == 563
    assert len(pages[1]) == 360


def test_get_pages_png_1page(ocr: OpticR) -> None:
    pages = ocr.get_pages("tests/data/test-1page.png")
    assert len(pages) == 1
    assert "Mac users will have to install poppler" in pages[0]
