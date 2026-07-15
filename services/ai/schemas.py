from typing import List, Optional

from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None


class AIResponse(BaseModel):
    category: str

    headline: str
    summary: str

    highlights: List[str] = []

    ai_explains: Optional[str] = None

    exam_notes: List[str] = []

    interview_question: Optional[InterviewQuestion] = None

    recommendations: List[str] = []

    important_terms: List[str] = []

    hashtags: List[str] = []

    image_prompt: str

    sections: List[str] = []