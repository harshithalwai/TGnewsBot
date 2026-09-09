import textwrap


class PromptBuilder:

    @staticmethod
    def build(
        title: str,
        article: str,
        source: str,
    ):

        return textwrap.dedent(
            f"""
            You are an expert news analyst and educator.

            Convert the provided news article into accurate,
            useful educational content for Telegram.

            IMPORTANT:
            You MUST analyze the actual article.
            Do not assume that every article is cybersecurity.

            ============================================================
            ABSOLUTE RULES
            ============================================================

            1. Return ONLY valid JSON.

            2. Do NOT use markdown.

            3. Do NOT use ```json.

            4. Do NOT write anything before or after JSON.

            5. Do NOT think aloud.

            6. Use ONLY information supported by the article.

            7. NEVER invent facts.

            8. If information is unavailable, use null or [].

            9. Never invent:
               - CVE IDs
               - CVSS scores
               - vulnerabilities
               - attack status
               - exploitation status
               - vendors
               - products
               - threat actors
               - malware
               - dates
               - statistics
               - locations
               - organizations
               - technical specifications

            10. Every list item must be a string.

            11. sections must contain strings only.

            12. Keep all content factual.

            ============================================================
            CATEGORY
            ============================================================

            Choose the category based on the actual article.

            Examples:

            cybersecurity
            technology
            AI
            science
            space
            business
            world
            India
            privacy
            economics
            politics
            sports

            ============================================================
            HEADLINE
            ============================================================

            Create a concise factual headline.

            Do NOT use clickbait.

            ============================================================
            SUMMARY
            ============================================================

            Give a concise factual summary.

            ============================================================
            HIGHLIGHTS
            ============================================================

            Provide 3 to 6 important points.

            ============================================================
            AI EXPLAINS
            ============================================================

            Explain an important technical or conceptual idea
            from the article in simple educational language.

            If there is no useful concept:

            null

            ============================================================
            EXAM NOTES
            ============================================================

            Provide useful study points directly related
            to the article.

            ============================================================
            INTERVIEW QUESTION
            ============================================================

            Create one useful interview question.

            Include a concise answer.

            If meaningless:

            null

            ============================================================
            RECOMMENDATIONS
            ============================================================

            Only provide recommendations supported by the article.

            Do NOT invent risks.

            ============================================================
            IMPORTANT TERMS
            ============================================================

            List important terms appearing in or directly supported
            by the article.

            ============================================================
            HASHTAGS
            ============================================================

            Generate relevant hashtags.

            Do not create misleading hashtags.

            ============================================================
            IMAGE PROMPT
            ============================================================

            Create a concise visual prompt representing the actual
            article.

            Do NOT include:

            - text
            - logos
            - trademarks
            - watermarks
            - invented events

            ============================================================
            SECTIONS
            ============================================================

            Create 2 to 5 educational sections.

            Each section MUST be a plain string.

            Example:

            [
                "Background: ...",
                "What Happened: ...",
                "Why It Matters: ..."
            ]

            ============================================================
            ARTICLE
            ============================================================

            Title:
            {title}

            Source:
            {source}

            Article:
            {article}

            ============================================================
            REQUIRED JSON
            ============================================================

            {{
                "category": null,
                "headline": null,
                "summary": null,
                "highlights": [],
                "ai_explains": null,
                "exam_notes": [],
                "interview_question": null,
                "recommendations": [],
                "important_terms": [],
                "hashtags": [],
                "image_prompt": null,
                "sections": []
            }}

            RETURN ONLY VALID JSON.
            """
        )