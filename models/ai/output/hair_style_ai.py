from pydantic import BaseModel


class HairStyleAI(BaseModel):
    name: str
    description: str
