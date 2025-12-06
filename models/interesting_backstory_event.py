from typing import Optional

from pydantic import BaseModel


class InterestingBackstoryEvent(BaseModel):
    id: Optional[int] = None
    backstory_id: Optional[int] = None
    name: str
    description: str
    reason_for_importance: str