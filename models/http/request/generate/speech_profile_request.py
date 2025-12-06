from typing import Optional

from pydantic import BaseModel


class SpeechProfileRequest(BaseModel):
    emojis_allowed: Optional[bool] = False
    verbose: Optional[bool] = False


