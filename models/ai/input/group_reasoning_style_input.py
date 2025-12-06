from pydantic import BaseModel, Field

from models.backstory import Backstory
from models.speech_profile import SpeechProfile


class GroupReasoningStyleInput(BaseModel):
    backstory: Backstory = Field(description="The profile of the person whose reasoning style is being generated.")
    speech_profile: SpeechProfile = Field(description="The speech profile of the person, this must be how they speak.")
