from typing import Optional

from pydantic import BaseModel


class BackstoryGenerateRequest(BaseModel):
    name: str
    description: str
    historical: Optional[bool] = False