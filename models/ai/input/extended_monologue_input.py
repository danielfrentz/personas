from pydantic import Field

from models.backstory import Backstory
from models.speech_profile import SpeechProfile


class ExtendedMonologueInput:
    theme: str = Field(description="The theme of the conversation.")
    prompt: str = Field(description="The text that the user spoke to start the conversation.")
    speaker: Backstory = Field(description="The speaker in the conversation. This is the only one that should speak after the first prompt.")
    speaker_speech_profile: SpeechProfile = Field(description="The speech profile of the person who gives the monologue")
    speaker_name: str = Field(description="The name of the speaker.")