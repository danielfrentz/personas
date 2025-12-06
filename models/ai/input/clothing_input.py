from typing import List

from pydantic import BaseModel, Field

from models.backstory import Backstory
from models.clothing import Clothing
from models.physical_description import PhysicalDescription


class ClothingInput(BaseModel):
    backstory: Backstory = Field(description="Backstory of the persona to whom the clothing belongs.")
    existing_clothing: List[Clothing] = Field(description="List of existing clothing.")
    physical_description: PhysicalDescription = Field(description="Description of the physical characteristics of the clothing.")