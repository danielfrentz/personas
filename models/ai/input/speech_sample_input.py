from pydantic import BaseModel, Field

from models.backstory import Backstory
from models.speech_profile import SpeechProfile


class SpeechSampleInput(BaseModel):
    speech_profile: SpeechProfile = Field(description="The description of what we know about how the person speaks, including existing samples.")
    backstory: Backstory = Field(description="The profile of the person whose speech is being generated.")