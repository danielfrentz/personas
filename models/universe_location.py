from typing import Optional

from pydantic import BaseModel


class UniverseLocation(BaseModel):
    id: Optional[int] = None
    universe_id: Optional[int] = None
    historically_accurate: bool
    must_be_historically_accurate: bool
    location_name: str
    location_used_by: str
    location_purpose: str
    visual_description: str