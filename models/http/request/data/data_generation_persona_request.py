from typing import Optional, List

from pydantic import Field, BaseModel


class DataGenerationPersonaRequest(BaseModel):
    persona_id: int
    aspects: Optional[List[str]] = Field(default_factory=list)