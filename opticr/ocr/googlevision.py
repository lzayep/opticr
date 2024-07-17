from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
from functools import cache
from google.cloud import vision

from opticr.config import config
from opticr.ocr.baseocr import BaseOcr


@cache
def vision_client(key: str = "") -> vision.ImageAnnotatorClient:
    """
    Create a EPostClient instance with the given key
    It cache the answer for the same key
    use filedl_client.cache_clear() to clear the cache
    """
    _ = key
    client_options = {"api_endpoint": "eu-vision.googleapis.com"}
    sa = config().ocr.google_vision.service_account_json
    return vision.ImageAnnotatorClient.from_service_account_file(
        sa, client_options=client_options
    )


@dataclass
class GoogleVisionResponse:
    reponse_type: Literal["image", "file"] = ...
    image_annotation: vision.AnnotateImageResponse | None = None
    file_annotation: vision.AnnotateFileResponse | None = None
    pages: list[str] = field(default_factory=list)


class GoogleVisionOcr(BaseOcr):
    name: str = "google-vision"

    def __init__(self, language: Literal["eng", "deu"] = "eng") -> None:
        self.language = language

    def ocr(self, document_path: str) -> list[str]:
        if Path(document_path).suffix in [".pdf", ".PDF"]:
            return self.detect_text_file(document_path).pages
        return self.detect_text_image(document_path).pages

    def detect_text_file(self, path: str) -> GoogleVisionResponse:
        """Detects text in the file."""

        client = vision_client()
        if Path(path).suffix not in [".pdf", ".PDF"]:
            raise ValueError("Only PDF files are supported")

        with open(path, "rb") as pdf_file:
            content = pdf_file.read()

        mime_type = "application/pdf"
        feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
        input_config = vision.InputConfig(content=content, mime_type=mime_type)
        sync_request = vision.AnnotateFileRequest(
            features=[feature], input_config=input_config
        )
        sync_operation = client.batch_annotate_files(requests=[sync_request])
        res: vision.AnnotateFileResponse = sync_operation.responses[0]
        pages = []
        for response in res.responses:
            pages.append(response.full_text_annotation.text)

        return GoogleVisionResponse(
            reponse_type="file", file_annotation=res, pages=pages
        )

    def detect_text_image(self, path: str) -> GoogleVisionResponse:
        """Detects text in the Image."""

        client = vision_client()

        with open(path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
        request = vision.AnnotateImageRequest(image=image, features=[feature])
        response = client.annotate_image(request)
        if response.error.message:
            raise ValueError(
                f"{response.error.message}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors"
            )
        page1 = response.text_annotations[0].description
        return GoogleVisionResponse(
            reponse_type="image", image_annotation=response, pages=[page1]
        )


# def detect_text_async_gcs(uri: str) -> GoogleVisionResponse:
# https://cloud.google.com/vision/docs/pdf
#     client = vision_client()
#     feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
#     mime_type = "application/pdf"
#     gcs_destination_uri = uri +".res.json"
#     output_config = vision.OutputConfig(gcs_destination=gcs_destination_uri)
#     gcs_source = vision.GcsSource(uri=uri)
#     input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
#     async_request = vision.AsyncAnnotateFileRequest(
#         features=[feature], input_config=input_config, output_config=output_config)
#     async_operation = client.async_batch_annotate_files(requests=[async_request])
#     async_operation.result(timeout=42)
