from typing import Optional

from pydantic import BaseModel, Field


class Clothing(BaseModel):
    id: Optional[int] = None
    clothing_name: str = Field(description="A name to identify this specific clothing.")
    clothing_category: Optional[str]
    description: Optional[str]
    occasion: Optional[str]
    diffusion_model_description: str = Field(
        description="A description that can be used with a diffusion model to recreate the clothing visually.")
    purpose: Optional[str] = Field(description="Why they wear this.")
    physical_description_id: Optional[int]
    personal_significance: Optional[str]