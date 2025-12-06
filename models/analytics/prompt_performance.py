from typing import Optional

from pydantic import BaseModel


class PromptPerformance(BaseModel):
    id: Optional[int] = None
    prompt: str
    response: str
    time_taken: float
    model: str
    template_name: str