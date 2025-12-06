from fastapi import APIRouter, Depends

from endpoint import get_story_service
from endpoint.rest.introspection import introspection_rest_router
from endpoint.rest.story_conversation import story_conversation_rest_router
from models.story import Story
from service.persona_domain.story_service import StoryService

story_rest_router = APIRouter(prefix="/{life_event_id}/story")
story_rest_router.include_router(story_conversation_rest_router)
story_rest_router.include_router(introspection_rest_router)
@story_rest_router.post("/")
async def create(story: Story, story_service: StoryService = Depends(get_story_service)) -> Story:
    return story_service.save(story)

@story_rest_router.get("/{story_id}")
async def get_story(story_id: int, story_service: StoryService = Depends(get_story_service)):
    return story_service.find_by_id(story_id)

@story_rest_router.get("/")
async def get_all(life_event_id: int, story_service: StoryService = Depends(get_story_service)):
    return story_service.find_by_life_event(life_event_id)

@story_rest_router.delete("/{story_id}")
async def delete(story_id: int, story_service: StoryService = Depends(get_story_service)):
    return story_service.delete(story_id)