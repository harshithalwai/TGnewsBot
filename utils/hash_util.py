import hashlib
import re


class HashUtil:

    @staticmethod
    def generate(text: str) -> str:

        if not text:
            return ""

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    # ============================================================
    # NORMALIZE TITLE
    # ============================================================

    @staticmethod
    def normalize_title(title: str) -> str:

        if not title:
            return ""

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

    # ============================================================
    # TITLE HASH
    # ============================================================

    @staticmethod
    def generate_title_hash(title: str) -> str:

        normalized = HashUtil.normalize_title(
            title
        )

        return HashUtil.generate(
            normalized
        )