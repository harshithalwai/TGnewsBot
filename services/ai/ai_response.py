from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class InterviewQuestion(BaseModel):

    question: Optional[str] = None

    answer: Optional[str] = None


class AIResponse(BaseModel):

    category: Optional[str] = None

    headline: Optional[str] = None

    summary: Optional[str] = None

    highlights: List[str] = Field(
        default_factory=list
    )

    ai_explains: Optional[str] = None

    exam_notes: List[str] = Field(
        default_factory=list
    )

    interview_question: Optional[
        InterviewQuestion
    ] = None

    recommendations: List[str] = Field(
        default_factory=list
    )

    important_terms: List[str] = Field(
        default_factory=list
    )

    hashtags: List[str] = Field(
        default_factory=list
    )

    image_prompt: Optional[str] = None

    sections: List[str] = Field(
        default_factory=list
    )

    # ============================================================
    # LIST VALIDATION
    # ============================================================

    @field_validator(
        "highlights",
        "exam_notes",
        "recommendations",
        "important_terms",
        "hashtags",
        "sections",
        mode="before",
    )
    @classmethod
    def none_to_empty_list(cls, value):

        if value is None:
            return []

        if not isinstance(value, list):
            return [str(value)]

        return [
            str(item)
            for item in value
            if item is not None
        ]