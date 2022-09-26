import hashlib
from pathlib import PurePath
from shutil import copyfile
import logging
from urllib.parse import urlparse

import requests


logger: logging.Logger = logging.getLogger(__name__)


def build_path(content: bytes, source_path: str, dest: str) -> str:
    hashsha = hashlib.sha256(content)
    path = PurePath(source_path)
    suffix = path.suffix
    return str(path.joinpath(dest, hashsha.hexdigest() + suffix))


async def copy_local_file(source_path: str, destdir: str) -> str:
    with open(source_path, "rb") as fopen:
        content = fopen.read()
    dest_path = build_path(content, source_path, destdir)
    copyfile(source_path, dest_path)
    return dest_path


async def download_file(source: str, source_path: str, dest: str) -> str:
    """Download the file from http(s)"""
    resp = requests.get(source, timeout=60)
    resp.raise_for_status()
    dest_path = build_path(resp.content, source_path, dest)
    with open(dest_path, "wb") as fopen:
        fopen.write(resp.content)
    return dest_path


async def download(source: str, dest_dir: str) -> str:
    """
    Determine the protocol to fetch the document:
    file://,
    http://,
    s3:// ...
    """
    parsedurl = urlparse(source)
    logger.info("download %s, %s", parsedurl.scheme, parsedurl.path)
    if parsedurl.scheme in ["file", ""]:
        return await copy_local_file(parsedurl.path, dest_dir)
    if parsedurl.scheme in ["http", "https"]:
        return await download_file(source, parsedurl.path, dest_dir)

    raise AttributeError(
        f"Unsupported file source: scheme={parsedurl.scheme} - path={parsedurl.path}"
    )
