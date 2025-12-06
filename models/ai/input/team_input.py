from pydantic import BaseModel


class TeamInput(BaseModel):
    team_size: int
    task_description: str