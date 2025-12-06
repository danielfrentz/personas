from typing import List

from pydantic import BaseModel, Field

from models.accessory import Accessory
from models.backstory import Backstory
from models.physical_description import PhysicalDescription


class AccessoryInput(BaseModel):
    existing_accessories: List[Accessory] = Field(description="List of existing accessories")
    backstory: Backstory = Field(description="the backstory of the person who uses the accessory")
    physical_description: PhysicalDescription = Field(description="the physical description of the person")