from fastapi import APIRouter, Depends

from endpoint import get_story_conversation_service
from endpoint.generate.memory import memory_generate_router
from models.conversation import Conversation
from service.persona_domain.story_conversation_service import StoryConversationService

story_conversation_generate_router = APIRouter(prefix="/{story_id}/conversation")
story_conversation_generate_router.include_router(memory_generate_router)
@story_conversation_generate_router.post("/")
async def generate(persona_id: int,
             universe_id:int,
             story_id: int,
             story_conversation_service: StoryConversationService = Depends(get_story_conversation_service)) -> Conversation:
    return story_conversation_service.generate(story_id=story_id, universe_id=universe_id, persona_id=persona_id)

