from typing import List, Optional

from pydantic import BaseModel, Field

from models.backstory import Backstory
from models.group_reasoning_style import GroupReasoningStyle
from models.life_event import LifeEvent
from models.persona_knowledge import PersonaKnowledge
from models.persona_skill import PersonaSkill
from models.physical_description import PhysicalDescription
from models.relationship import Relationship
from models.speech_profile import SpeechProfile


class Persona(BaseModel):
    id: Optional[int] = None
    universe_id: int
    backstory: Optional[Backstory] = None
    historical: Optional[bool] = False
    relationships: Optional[List[Relationship]] = Field(default_factory=list)
    physical_description: Optional[PhysicalDescription] = None
    speech_profile: Optional[SpeechProfile] = None
    life_events: Optional[List[LifeEvent]] = Field(default_factory=list)
    group_reasoning_profile: Optional[GroupReasoningStyle] = None
    skills: Optional[List[PersonaSkill]] = Field(default_factory=list)
    knowledge: Optional[List[PersonaKnowledge]] = Field(default_factory=list)