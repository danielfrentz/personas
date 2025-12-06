from fastapi import APIRouter, Depends

from endpoint import get_reasoning_conversation_service
from models.reasoning_conversation import ReasoningConversation
from service.persona_domain.reasoning_conversation_service import ReasoningConversationService

reasoning_rest_router = APIRouter(prefix="/{persona_id}/reasoning")

@reasoning_rest_router.post("/")
async def save(reasoning_conversation: ReasoningConversation, reasoning_conversation_service: ReasoningConversationService = Depends(get_reasoning_conversation_service)):
    return reasoning_conversation_service.save(reasoning_conversation)

@reasoning_rest_router.get("/")
async def find_by_persona(persona_id: int, reasoning_conversation_service: ReasoningConversationService = Depends(get_reasoning_conversation_service)):
    return reasoning_conversation_service.find_by_persona(persona_id)

@reasoning_rest_router.delete("/{reasoning_conversation_id}")
async def delete(reasoning_conversation_id: int, reasoning_conversation_service: ReasoningConversationService = Depends(get_reasoning_conversation_service)):
    reasoning_conversation_service.delete_by_id(reasoning_conversation_id)