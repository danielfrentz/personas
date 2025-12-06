from models.http.request.generate.raw_persona_request import ObjectivePersonaRequest
from models.http.response.raw_persona_description_response import RawPersonaDescriptionResponse
from service.ai.ai_service import AIService


class PersonaObjectiveDescriptionService:
    def __init__(self,
                 ai_service: AIService):
        self.ai_service = ai_service

    def generate(self, raw_persona_request: ObjectivePersonaRequest, universe_id: int):
        result = self.ai_service.call_llm(system_prompt_name="create_objective_persona",
                                 user_data=raw_persona_request,
                                 universe_id=universe_id,
                                 return_type=RawPersonaDescriptionResponse)
        return result