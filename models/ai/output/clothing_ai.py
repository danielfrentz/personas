from pydantic import BaseModel, Field

class ClothingAI(BaseModel):
    how_this_clothing_affects_personality: str
    how_this_clothing_affects_appearance: str
    how_this_clothing_type_is_unique_to_person: str
    how_this_clothing_type_is_new_to_person: str
    clothing_name: str = Field(description="The name of the clothing")
    clothing_type: str = Field(description="The type of the clothing")
    diffusion_model_description: str = Field(description="A description that can be used with a diffusion model to recreate the clothing visually.")
    purpose: str = Field(description="The purpose of the clothing")
    occasion: str = Field(description="The occasion in which the person wears this clothing.")
    personal_significance: str = Field(description="The personal significance of the clothing.")
    detailed_description: str = Field(description="The detailed description of the clothing.")