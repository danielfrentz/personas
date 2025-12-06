from typing import Optional

from pydantic import BaseModel


class Hobby(BaseModel):
    id: Optional[int] = None
    backstory_id: Optional[int] = None
    name: str
    description: str