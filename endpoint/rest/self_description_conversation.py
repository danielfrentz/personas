from typing import List

from fastapi import APIRouter, Depends

from endpoint import get_self_description_conversation_service
from models.ai.output.self_description_conversation import SelfDescriptionConversation
from service.persona_domain.self_description_conversation_service import SelfDescriptionConversationService

self_description_conversation_rest_router = APIRouter(prefix="/{persona_id}/self_description_conversation")

@self_description_conversation_rest_router.post("/")
async def save(conversation: SelfDescriptionConversation, self_description_conversation_service: SelfDescriptionConversationService = Depends(get_self_description_conversation_service)):
    return self_description_conversation_service.save(conversation)


@self_description_conversation_rest_router.get("/")
async def get_all(persona_id: int, self_description_conversation_service: SelfDescriptionConversationService = Depends(get_self_description_conversation_service)) -> List[SelfDescriptionConversation]:
    return self_description_conversation_service.find_by_persona_id(persona_id=persona_id)