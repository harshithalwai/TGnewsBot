import requests

from bs4 import BeautifulSoup


class ArticleExtractor:

    REQUEST_TIMEOUT = 10

    USER_AGENT = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )

    @classmethod
    def extract(
        cls,
        url: str,
    ) -> str | None:

        try:

            response = requests.get(
                url,
                timeout=cls.REQUEST_TIMEOUT,
                headers={
                    "User-Agent": cls.USER_AGENT
                },
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.content,
                "html.parser",
            )

            # ====================================================
            # REMOVE NON-CONTENT
            # ====================================================

            for element in soup.find_all(
                [
                    "script",
                    "style",
                    "nav",
                    "header",
                    "footer",
                    "aside",
                    "form",
                    "noscript",
                    "iframe",
                    "svg",
                ]
            ):

                element.decompose()

            # ====================================================
            # PREFER ARTICLE TAG
            # ====================================================

            container = soup.find("article")

            if container is None:

                container = soup.body

            if container is None:

                return None

            paragraphs = []

            for paragraph in container.find_all("p"):

                text = paragraph.get_text(
                    " ",
                    strip=True,
                )

                if len(text) < 40:
                    continue

                paragraphs.append(text)

            if not paragraphs:

                return None

            # ====================================================
            # REMOVE DUPLICATE PARAGRAPHS
            # ====================================================

            unique_paragraphs = []

            seen = set()

            for paragraph in paragraphs:

                normalized = paragraph.lower().strip()

                if normalized in seen:
                    continue

                seen.add(normalized)

                unique_paragraphs.append(
                    paragraph
                )

            article_text = "\n\n".join(
                unique_paragraphs
            )

            # ====================================================
            # LIMIT ARTICLE SIZE
            # ====================================================

            return article_text[:12000]

        except requests.RequestException as exc:

            print(
                f"Article request failed: {exc}"
            )

            return None

        except Exception as exc:

            print(
                f"Article extraction failed: {exc}"
            )

            return None