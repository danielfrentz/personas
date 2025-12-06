from typing import Optional

from pydantic import BaseModel


class UniverseDescription(BaseModel):
    id: Optional[int] = None
    universe_id: Optional[int] = None
    description: str
    creatures: str