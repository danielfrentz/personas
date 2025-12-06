from converter.persona_skill_converter import PersonaSkillConverter
from dao.persona_skill_dao import PersonaSkillDAO
from service.ai.ai_service import AIService


class PersonaSkillService:
    def __init__(self,
                 ai_service: AIService,
                 persona_skill_dao: PersonaSkillDAO,
                 persona_skill_converter: PersonaSkillConverter):
        self.ai_service = ai_service
        self.persona_skill_dao = persona_skill_dao
        self.persona_skill_converter = persona_skill_converter

    def generate(self, persona_id: int):
        pass