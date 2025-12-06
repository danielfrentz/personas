from pydantic import BaseModel, Field


class SpeechProfileAI(BaseModel):
    speech_description: str = Field(description="A detailed description of how this person speaks and how their speech changes with the situation.")
    emotional_description: str = Field(description="A detailed description of how this persons emotions are displayed as they speak, or if they are monotoned hiding their speech in a shroud of mystery.")