from typing import List, Dict

from pydantic import BaseModel

from models.backstory import Backstory


class LikeInput(BaseModel):
    current_likes: List[Dict[str, str]]
    backstory: Backstory