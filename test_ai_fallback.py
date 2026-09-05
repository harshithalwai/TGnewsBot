import multiprocessing

from services.ai.ollama_service import OllamaService


def main():

    service = OllamaService()

    print("=" * 60)
    print("TESTING AI FALLBACK")
    print("=" * 60)

    result = service.generate(

        title=(
            "Major technology companies announce "
            "new cybersecurity measures"
        ),

        article=(
            "Several major technology companies have "
            "announced new cybersecurity measures "
            "designed to improve protection against "
            "emerging online threats."
        ),

        source="Test Source",
    )

    print()

    print("=" * 60)
    print("AI RESULT")
    print("=" * 60)

    print("CATEGORY:", result.category)

    print("HEADLINE:", result.headline)

    print("SUMMARY:", result.summary)

    print("HIGHLIGHTS:", result.highlights)

    print("AI EXPLAINS:", result.ai_explains)

    print("EXAM NOTES:", result.exam_notes)

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


if __name__ == "__main__":

    multiprocessing.freeze_support()

    main()