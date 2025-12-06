from typing import Optional

from pydantic import BaseModel


class UniverseMetadata(BaseModel):
    id:Optional[int] = None
    universe_id: Optional[int] = None
    name: str
    description: str