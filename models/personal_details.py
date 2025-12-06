from typing import List

from pydantic import BaseModel

from .physical_description import PhysicalDescription


class PersonalDetails(BaseModel):
    likes: List[str]
    dislikes: List[str]
    attributes: List[str]
    short_term_goals: List[str]
    long_term_goals: List[str]
    physical_description: PhysicalDescription