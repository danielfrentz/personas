from typing import List

from pydantic import BaseModel

from models.ai.output.team_member_ai import TeamMemberAI


class TeamAI(BaseModel):
    team_members: List[TeamMemberAI]
    setting_description: str
    team_description: str