from pydantic import BaseModel, Field


class SpeechSampleAI(BaseModel):
    justification_that_situation_is_unique: str
    justification_that_tone_is_unique: str
    justification_that_feeling_is_unique: str
    justification_that_example_aligns_with_speech_profile: str
    how_aspects_affect_tone_and_words: str
    justification_that_example_is_realistic_and_not_metaphorical: str
    justification_that_example_does_not_violate_speech_profile: str
    justification_that_example_starts_uniquely: str
    personality_aspects_depicted: list[str]
    audience_description: str
    tone: str = Field(description="A single tone that would be used as they speak this example.")
    feeling: str = Field(description="The feeling that the persona is having as they say this example.")
    example: str
    situation: str
    explanation: str