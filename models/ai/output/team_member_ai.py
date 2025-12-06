from pydantic import BaseModel


class TeamMemberAI(BaseModel):
    name: str
    description: str