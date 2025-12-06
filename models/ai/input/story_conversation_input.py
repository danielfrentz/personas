from typing import Dict, List

from pydantic import BaseModel

from models.backstory import Backstory
from models.relationship import Relationship
from models.speech_profile import SpeechProfile


class ConversationInput(BaseModel):
    story: str
    relationships: List[Relationship]
    speech_profiles: Dict[str, SpeechProfile]
    backstory: Backstory