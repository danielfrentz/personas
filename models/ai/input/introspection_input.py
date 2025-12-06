from typing import List

from pydantic import BaseModel, Field

from models.backstory import Backstory
from models.conversation import Conversation
from models.persona_aspect import PersonaAspect
from models.relationship import Relationship
from models.speech_profile import SpeechProfile


class IntrospectionInput(BaseModel):
    relationships: List[Relationship] = Field(description="Relationships associated with the main character")
    speech_pattern: SpeechProfile = Field(description="Speech profile of the person thinking.")
    conversation: Conversation = Field(description="The conversations about which the main character is thinking.")
    backstory: Backstory = Field(description="The background information about the main character.")
    memories: List[str] = Field(description="The memory of the story.")
    aspect: PersonaAspect