import hashlib


def sha256_file(filename: str) -> str:
    with open(filename, "rb") as f:
        b = f.read()
        readable_hash = hashlib.sha256(b).hexdigest()
    return readable_hash
