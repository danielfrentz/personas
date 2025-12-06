from typing import Optional

from pydantic import BaseModel


class InterestingPhysicalDescriptionNote(BaseModel):
    id: Optional[int] = None
    description: str