from typing import Optional, List

from pydantic import BaseModel


class Event(BaseModel):
    id: Optional[int] = None
    title: str
    character_names: List[str]
    life_event_id: int
    lead_up: str
    neutral_retelling: str
    outcome: str
    main_character_id: int