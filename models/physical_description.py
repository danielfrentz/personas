from typing import List, Optional

from pydantic import BaseModel, Field

from models.accessory import Accessory
from models.ai.output.accessory_ai import AccessoryAI
from models.ai.output.clothing_ai import ClothingAI
from models.ai.output.physical_description_ai import PhysicalDescriptionAI
from models.backstory import Backstory
from models.clothing import Clothing
from models.hair_style import HairStyle
from models.interesting_physical_description_note import InterestingPhysicalDescriptionNote
from models.universe_description import UniverseDescription


class PhysicalDescription(BaseModel):
    id: Optional[int] = None
    height: str
    weight: str
    hair_color: str
    hair_style: Optional[list[HairStyle]] = Field(description="A list of ways they wear their hair, N/A if this does not apply.", default_factory=list)
    accessories: Optional[List[Accessory]] = Field(description="A list of accessories associated with this physical description.", default_factory=list)
    clothing: Optional[List[Clothing]] = Field(description="A list of their clothing pieces from their closet, an assortment such that the user understands how this person dresses.", default_factory=list)
    detailed_description: str = Field(description="Extremely detailed description combining all other fields into something people can visualize", min_length=500)
    interesting_notes: Optional[List[InterestingPhysicalDescriptionNote]] = Field(description="A list of interesting notes associated with this physical description.", default_factory=list)
    presentation: str = Field(description="How they like to present themselves")
    diffusion_model_description: str = Field(description="A description that can be used with a diffusion model to recreate the physical description visually.")


class PhysicalDescriptionInput(BaseModel):
    backstory: Backstory
    universe: UniverseDescription
    basics: Optional[PhysicalDescriptionAI] = Field(description="A list of basics associated with this physical description.", default_factory=list)
    clothing: Optional[List[ClothingAI]] = Field(description="A list of clothings associated with this physical description.", default_factory=list)
    accessories: Optional[List[AccessoryAI]] = Field(description="A list of accessories associated with this physical description.", default_factory=list)