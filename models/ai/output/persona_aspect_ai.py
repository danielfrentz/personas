

from pydantic import BaseModel, Field


class PersonaAspectAI(BaseModel):
    aspect_name: str
    situations_in_which_aspect_is_positive: str
    situations_in_which_aspect_is_negative: str
    how_this_aspect_affects_personality: str
    how_this_aspect_interacts_with_other_aspects: str
    strength_of_aspect_in_personality: int = Field(ge=0, le=100)
    aspect_description: str = Field(min_length=1000)