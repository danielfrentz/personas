from typing import List

from pydantic import BaseModel

from models.universe_metadata import UniverseMetadata


class UniverseInput(BaseModel):
    description: str = None
    inhabitants: str = None
    metadata: List[UniverseMetadata]  = None