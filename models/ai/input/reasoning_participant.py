
from pydantic import BaseModel, Field

from models.group_reasoning_style import GroupReasoningStyle
from models.speech_profile import SpeechProfile


class ReasoningParticipant(BaseModel):
    name: str = Field(description="The name of the possible participant")
    description: str = Field(description="The background information about this person")
    group_reasoning_style: GroupReasoningStyle = Field(description="the style they bring to the conversation")
    speech_profile: SpeechProfile = Field(description="The description of how they speak")