from typing import List

from pydantic import BaseModel, Field


class PhysicalDescriptionAI(BaseModel):
    possible_give_metrics_estimate_for_height: bool
    possible_give_metrics_estimate_for_weight: bool
    height: str = Field(max_length=20)
    weight: str = Field(max_length=20)
    detailed_description: str = Field(min_length=1000)
    presentation: str = Field(min_length=500)
    hair_color: str = Field(max_length=50)
    interesting_notes: str
    clothing_style: List[str]
    diffusion_model_description: str = Field(description="A description that can be used with a diffusion model to recreate the physical description visually.", min_length=1000)
