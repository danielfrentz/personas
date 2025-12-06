from models.ai.input.team_input import TeamInput
from models.ai.output.team_ai import TeamAI
from models.http.request.team_request import TeamRequest
from service.ai.ai_service import AIService


class TeamService:
    def __init__(self,
                 ai_service: AIService):
        self.ai_service = ai_service

    def generate(self, team_request: TeamRequest) -> TeamAI:
        user_input = TeamInput(
            team_size=team_request.team_size,
            task_description=team_request.task_description
        )
        response = self.ai_service.call_llm(system_prompt_name="create_team",
                                            return_type=TeamAI,
                                            user_data=user_input)
        return response