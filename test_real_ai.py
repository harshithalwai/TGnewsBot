import multiprocessing

from repositories.news_repository import NewsRepository

from services.ai.ollama_service import OllamaService


def main():

    print("=" * 60)
    print("TESTING AI WITH REAL NEWS")
    print("=" * 60)

    news_repo = NewsRepository()

    news_list = news_repo.get_unposted()

    if not news_list:

        print()
        print("NO UNPOSTED NEWS")
        return

    news = news_list[0]

    print()

    print("NEWS ID:", news.id)

    print("TITLE:", news.title)

    print(
        "SOURCE:",
        news.source.name
        if news.source
        else "Unknown"
    )

    print()

    print("=" * 60)
    print("GENERATING AI")
    print("=" * 60)

    ai = OllamaService()

    try:

        result = ai.generate(

            title=news.title,

            article=(
                news.summary
                or news.title
            ),

            source=(
                news.source.name
                if news.source
                else "Unknown"
            ),
        )

        print()

        print("=" * 60)
        print("AI GENERATION SUCCESSFUL")
        print("=" * 60)

        print("CATEGORY:", result.category)

        print("HEADLINE:", result.headline)

        print("SUMMARY:", result.summary)

        print(
            "HIGHLIGHTS:",
            result.highlights
        )

        print(
            "AI EXPLAINS:",
            result.ai_explains
        )

        print(
            "EXAM NOTES:",
            result.exam_notes
        )

        print(
            "INTERVIEW:",
            result.interview_question
        )

        print(
            "RECOMMENDATIONS:",
            result.recommendations
        )

        print(
            "TERMS:",
            result.important_terms
        )

        print(
            "HASHTAGS:",
            result.hashtags
        )

        print(
            "IMAGE PROMPT:",
            result.image_prompt
        )

        print()

        print("=" * 60)
        print("TEST COMPLETED")
        print("=" * 60)

    except Exception as exc:

        print()

        print("=" * 60)
        print("AI GENERATION FAILED")
        print("=" * 60)

        print("ERROR:", exc)


if __name__ == "__main__":

    multiprocessing.freeze_support()

    main()