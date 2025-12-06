from dao.conversation_dao import ConversationDAO
from dao.persona_aspect_conversation_dao import PersonaAspectConversationDAO
from models.http.request.generate.persona_aspect_conversation_request import PersonaAspectConversationRequest
from models.persona_aspect_conversation import PersonaAspectConversation
from service.ai.ai_service import AIService


class PersonaAspectConversationService:
    def __init__(self,
                 ai_service: AIService,
                 persona_conversation_dao: PersonaAspectConversationDAO,
                 conversation_dao: ConversationDAO):
        self.ai_service = ai_service
        self.persona_conversation_dao = persona_conversation_dao
        self.conversation_dao = conversation_dao

    def generate(self, persona_aspect_conversation_request: PersonaAspectConversationRequest):
        pass

    def save(self, persona_aspect_conversation: PersonaAspectConversation):
        pass

    def find_by_persona_id(self, persona_id: int):
        self.persona_conversation_dao.find_by_persona_id(persona_id=persona_id)