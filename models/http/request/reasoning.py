from typing import Optional

from pydantic import BaseModel, Field


class ReasoningRequest(BaseModel):
    theme: str
    prompt: Optional[str] = Field(default=None)
    solution: Optional[str] = Field(default=None)
    participant_count: Optional[int] = Field(default=5)
    answer_expectation: str
    error_made: bool = Field(default=False)