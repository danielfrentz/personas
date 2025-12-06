from fastapi import APIRouter, Depends

from endpoint import get_story_service
from endpoint.generate.introspection import introspection_generate_router
from endpoint.generate.story_conversation import story_conversation_generate_router
from models.story import Story
from service.persona_domain.story_service import StoryService

story_generate_router = APIRouter(prefix="/{life_event_id}/story",)
story_generate_router.include_router(story_conversation_generate_router)
story_generate_router.include_router(introspection_generate_router)
@story_generate_router.post("/")
async def generate(persona_id: int, life_event_id: int, story_service: StoryService = Depends(get_story_service)) -> Story:
    return story_service.generate(persona_id=persona_id, life_event_id=life_event_id)
