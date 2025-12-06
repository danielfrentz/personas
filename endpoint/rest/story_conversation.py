from fastapi import APIRouter, Depends

from endpoint import get_story_conversation_service
from endpoint.rest.memory import memory_rest_router
from models.conversation import Conversation
from service.persona_domain.story_conversation_service import StoryConversationService

story_conversation_rest_router = APIRouter(prefix="/{story_id}/conversation")
story_conversation_rest_router.include_router(memory_rest_router)
@story_conversation_rest_router.post("/")
async def save(story_conversation: Conversation, story_id: int, story_conversation_service: StoryConversationService = Depends(get_story_conversation_service)) -> Conversation:
    result = story_conversation_service.save(story_conversation, story_id=story_id)
    return result


@story_conversation_rest_router.get("/{story_conversation_id}/")
async def get_story(story_conversation_id: int, story_conversation_service: StoryConversationService = Depends(get_story_conversation_service)):
    return story_conversation_service.find_by_story_id(story_conversation_id)

@story_conversation_rest_router.delete("/{story_conversation_id")
async def delete(story_conversation_id, story_conversation_service: StoryConversationService = Depends(get_story_conversation_service)):
    return story_conversation_service.delete_by_id(story_conversation_id)

@story_conversation_rest_router.get("/")
async def get_story_conversation_all(story_id: int, story_conversation_service: StoryConversationService = Depends(get_story_conversation_service)):
    return story_conversation_service.find_by_story_id(story_id)