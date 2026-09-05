import requests
from bs4 import BeautifulSoup


class ArticleExtractor:

    REQUEST_TIMEOUT = 10

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )

    @classmethod
    def extract(cls, url: str) -> str | None:

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

            # Remove elements that are not article content
            for element in soup(
                [
                    "script",
                    "style",
                    "nav",
                    "header",
                    "footer",
                    "aside",
                    "form",
                    "noscript",
                ]
            ):
                element.decompose()

            paragraphs = []

            for paragraph in soup.find_all("p"):

                text = paragraph.get_text(
                    " ",
                    strip=True,
                )

                if len(text) < 40:
                    continue

                paragraphs.append(text)

            if not paragraphs:
                return None

            # Avoid sending an enormous article to the AI
            article_text = "\n\n".join(
                paragraphs
            )

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