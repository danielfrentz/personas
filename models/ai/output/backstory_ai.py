from pydantic import BaseModel, Field


class BackstoryAI(BaseModel):
    name: str
    gender: str
    place_of_birth: str
    date_of_birth: str
    schools_attended: str = Field()
    interests: list[str] = Field()
    family_members: list[str] = Field()
    interested_in_continued_learning: str
    education_description: str = Field(min_length=500)
    social_description: str = Field(min_length=500)
    indepth_general_description: str = Field(min_length=1000)