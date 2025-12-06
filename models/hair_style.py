from typing import Optional

from pydantic import BaseModel


class HairStyle(BaseModel):
    id: Optional[int] = None
    physical_description_id: int = None
    name: str
    description: str
    occasion: str