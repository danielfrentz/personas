from typing import Optional

from pydantic import BaseModel


class SpeechSample(BaseModel):
    id: Optional[int] = None
    tone: str
    example: str
    situation: str
    feeling: str
    speech_profile_id: Optional[int] = None
    explanation: str