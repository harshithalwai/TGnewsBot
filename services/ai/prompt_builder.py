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

            Your job is to convert the provided news article
            into accurate, useful educational content for Telegram.

            The article may be about:
            - cybersecurity
            - technology
            - artificial intelligence
            - science
            - space
            - business
            - world news
            - India
            - privacy
            - economics
            - or another legitimate news topic.

            Analyze the ACTUAL article subject.

            ============================================================
            STRICT OUTPUT RULES
            ============================================================

            1. Return ONLY valid JSON.

            2. Do NOT wrap JSON inside markdown.

            3. Do NOT use ```json.

            4. Do NOT explain anything outside the JSON.

            5. Do NOT think aloud.

            6. Use only information supported by the article.

            7. Do NOT invent facts.

            8. If information does not exist in the article,
               return null for an optional string field.

            9. Never invent:
               - CVE IDs
               - CVSS scores
               - attack status
               - exploitation status
               - vendors
               - affected products
               - threat actors
               - malware names
               - dates
               - statistics
               - locations
               - organizations
               - technical specifications

            10. Keep the content factual and educational.

            11. All list fields MUST contain strings.

            12. sections MUST contain strings only.

            ============================================================
            FIELD RULES
            ============================================================

            category:
            - Choose a short category based on the actual article.
            - Examples:
              cybersecurity, technology, AI, space, science,
              world, India, business, privacy, economics, politics.
            - Do not force every article into cybersecurity.

            headline:
            - Create a concise informative headline.
            - Do not exaggerate.
            - Do not use clickbait.

            summary:
            - Give a concise factual summary.
            - Do not add information not present in the article.

            highlights:
            - Give 3 to 6 important points.
            - Every item must be a string.

            ai_explains:
            - Explain an important technical or conceptual aspect
              of the article in simple educational language.
            - If there is no useful concept to explain, return null.

            exam_notes:
            - Give useful study points directly related to the article.
            - Do not invent facts.
            - Every item must be a string.

            interview_question:
            - Create one useful interview question related to the article.
            - Include a concise answer.
            - If not meaningful, return null.

            recommendations:
            - Give practical recommendations only when supported
              by the article.
            - Do not invent threats or risks.
            - Every item must be a string.

            important_terms:
            - List important domain-specific terms appearing in
              or directly supported by the article.
            - Every item must be a string.

            hashtags:
            - Generate relevant hashtags.
            - Every item must be a string.
            - Do not create misleading hashtags.

            image_prompt:
            - Create a concise visual prompt representing the actual article.
            - Do not include text, logos, trademarks, or watermarks.
            - Do not invent events.

            sections:
            - Create 2 to 5 useful educational sections.
            - Each section MUST be a plain string.
            - Example:
              [
                "Background: ...",
                "What Happened: ...",
                "Why It Matters: ..."
              ]

            ============================================================
            ARTICLE INFORMATION
            ============================================================

            Title:
            {title}

            Source:
            {source}

            Article:
            {article}

            ============================================================
            REQUIRED JSON STRUCTURE
            ============================================================

            {{
              "category": "",
              "headline": "",
              "summary": "",
              "highlights": [],
              "ai_explains": null,
              "exam_notes": [],
              "interview_question": {{
                "question": "",
                "answer": ""
              }},
              "recommendations": [],
              "important_terms": [],
              "hashtags": [],
              "image_prompt": "",
              "sections": []
            }}

            RETURN ONLY VALID JSON.
            """
        )