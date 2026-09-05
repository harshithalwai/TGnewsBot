import hashlib
import re


class HashUtil:

    @staticmethod
    def generate(text: str) -> str:

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def normalize_title(title: str) -> str:

        title = title.lower()

        title = re.sub(
            r"[^\w\s]",
            " ",
            title,
        )

        title = re.sub(
            r"\s+",
            " ",
            title,
        )

        return title.strip()

    @staticmethod
    def generate_title_hash(title: str) -> str:

        normalized = HashUtil.normalize_title(
            title
        )

        return HashUtil.generate(
            normalized
        )