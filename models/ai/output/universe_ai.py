from pydantic import Field, BaseModel


class UniverseDescriptionAI(BaseModel):
    subtractions_to_be_made: str = Field(description="Subtractions to be made to the description.")
    additions_to_be_made: str = Field(description="Additions to be made to the description.")
    changes_to_be_made: str = Field(description="Changes to be made to the description.")
    estimate_of_quality_increase_after_changes: str = Field(description="Estimate of quality increase in the description.")
    updated_environment_description: str = Field(description="Description of the places that everything revolves around.")
    updated_inhabitants_description: str = Field(description="Description of the inhabitants that everything revolves around.")