from converter.persona_knowledge_converter import PersonaKnowledgeConverter
from dao.persona_knowledge_dao import PersonaKnowledgeDAO
from service.ai.ai_service import AIService


class PersonaKnowledgeService:
    def __init__(self, ai_service: AIService,
                 persona_knowledge_dao: PersonaKnowledgeDAO,
                 persona_knowledge_converter: PersonaKnowledgeConverter):
        self.ai_service = ai_service
        self.persona_knowledge_dao = persona_knowledge_dao
        self.persona_knowledge_converter = persona_knowledge_converter

    def generate(self, persona_id: int, universe_id: int):
        pass