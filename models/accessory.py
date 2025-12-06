from typing import Optional

from pydantic import BaseModel, Field


class Accessory(BaseModel):
    id: Optional[int] = None
    name: str
    item_type: Optional[str]
    description: Optional[str]
    occasion: Optional[str] = Field(description="When they typically wear it.")
    personal_significance: Optional[str]
    diffusion_model_description: str = Field(
        description="A description that can be used with a diffusion model to recreate the accessory visually.")
    physical_description_id: Optional[int] = None