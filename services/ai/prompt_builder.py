import textwrap


class PromptBuilder:

    @staticmethod
    def build(title: str, article: str, source: str):

        return textwrap.dedent(f"""
You are an expert Cyber Security educator.

Your job is NOT to write an article.

Your job is to create educational content for Telegram.

Return ONLY valid JSON.

Do NOT wrap JSON inside markdown.

Do NOT explain anything.

Do NOT think aloud.

If information does not exist in the article,
return null.

Never invent:

- CVE IDs
- CVSS Scores
- Attack status
- Vendors
- Exploitation status

Title:
{title}

Source:
{source}

Article:
{article}

Return JSON matching this structure:

{{
  "category":"",
  "headline":"",
  "summary":"",
  "highlights":[],
  "ai_explains":"",
  "exam_notes":[],
  "interview_question": {{
      "question":"",
      "answer":""
  }},
  "recommendations":[],
  "important_terms":[],
  "hashtags":[],
  "image_prompt":"",
  "sections":[]
}}
""")