from fastapi import APIRouter, Depends

from endpoint import get_self_description_conversation_service
from models.http.request.generate.self_description_conversation_request import SelfDescriptionConversationRequest
from service.persona_domain.self_description_conversation_service import SelfDescriptionConversationService

self_description_conversation_generate_router = APIRouter(prefix="/{persona_id}/self_description_conversation")

@self_description_conversation_generate_router.post("/")
async def generate_self_description_conversation(universe_id: int,
                                                 self_description_conversation_request: SelfDescriptionConversationRequest,
                                                 self_description_conversation_service: SelfDescriptionConversationService = Depends(get_self_description_conversation_service)):
    return self_description_conversation_service.generate(universe_id = universe_id, self_description_conversation_request=self_description_conversation_request)
