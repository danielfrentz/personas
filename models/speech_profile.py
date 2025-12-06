from typing import List, Optional

from pydantic import BaseModel, Field

from models.speech_sample import SpeechSample


class SpeechProfile(BaseModel):
    id: Optional[int] = None
    description: str
    emotional_description: str
    emojis_allowed: Optional[bool] = False
    samples: Optional[List[SpeechSample]] = Field(default_factory=list)
    verbose: Optional[bool] = False