from fastapi import APIRouter, Depends

from endpoint import get_reasoning_conversation_service
from models.http.request.reasoning import ReasoningRequest
from models.reasoning_conversation import ReasoningConversation
from service.persona_domain.reasoning_conversation_service import ReasoningConversationService

reasoning_generate_router = APIRouter(prefix="/{persona_id}/reasoning")

@reasoning_generate_router.post("/")
async def generate(persona_id: int, universe_id: int, reasoning_request: ReasoningRequest, reasoning_service: ReasoningConversationService = Depends(get_reasoning_conversation_service)) -> ReasoningConversation:
    return reasoning_service.generate(persona_id, universe_id, reasoning_request)
