from typing import Optional

from pydantic import BaseModel, Field


class AccessoryAI(BaseModel):
    how_this_accessory_type_is_unique_to_person: str
    how_this_accessory_type_is_new_to_person: str
    accessory_name: str
    accessory_type: str
    detailed_accessory_description: str
    wearing_occasion: Optional[str]
    personal_significance: Optional[str]
    diffusion_model_description: str = Field(
        description="A description that can be used with a diffusion model to recreate the accessory visually.")
