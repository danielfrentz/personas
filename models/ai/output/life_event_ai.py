from pydantic import BaseModel, Field


class LifeEventAI(BaseModel):
    detail_learned_about_persona: str = Field(description="What was learned about the persona.")
    event_title: str = Field(description="The title of the event.")
    description: str = Field(description="An indepth description of what happened and why this was important.")
    date: str = Field(description="The date of the event, if unknow then a description relative to others.")
    persona_knowledge_gained: str
    aspects_shown_for_first_time: str = Field(
        description="A list of aspects that were shown to the user about this person.")
    personality_aspects_involved: list[str] = Field()