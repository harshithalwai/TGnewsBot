import hashlib


class HashUtil:

    @staticmethod
    def generate(text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()