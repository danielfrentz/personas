from typing import List

from pydantic import BaseModel

from models.backstory import Backstory
from models.persona_aspect import PersonaAspect
from models.speech_profile import SpeechProfile


class SelfDescriptionConversationInput(BaseModel):
    persona_id: int
    backstory: Backstory
    prompter_backstory: Backstory
    speech_profile: SpeechProfile
    topic: str
    aspects: List[PersonaAspect]
    minimum_turns: int