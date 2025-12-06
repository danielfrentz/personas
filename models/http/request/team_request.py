from pydantic import BaseModel


class TeamRequest(BaseModel):
    task_description: str
    team_size: int