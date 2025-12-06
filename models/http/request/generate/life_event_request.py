from typing import Optional

from pydantic import BaseModel


class LifeEventRequest(BaseModel):
    title: Optional[str] = None
    context: Optional[str] = None
    date: Optional[str] = None