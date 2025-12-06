from pydantic import BaseModel, Field


class UniverseLocationAI(BaseModel):
    name: str = Field(description="A descriptive and unique name for this location.")
    purpose: str = Field(description="Indepth description as to why people go to this place and what they do there.")
    visual_description: str = Field(description="Indepth description as to what the place looks like.")