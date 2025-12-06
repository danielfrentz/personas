from typing import List, Optional

from pydantic import BaseModel, Field

from models.http.request.data.data_generation_persona_request import DataGenerationPersonaRequest


class DataGenerationRequest(BaseModel):
    universe_id: int
    personas: Optional[List[DataGenerationPersonaRequest]] = Field(default_factory=list)

