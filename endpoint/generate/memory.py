from fastapi import APIRouter
from fastapi.params import Depends

from endpoint import get_memory_service
from models.memory import Memory
from service.persona_domain.memory_service import MemoryService

memory_generate_router = APIRouter(prefix="/{conversation_id}/memory")


@memory_generate_router.post("/")
async def generate_memory(conversation_id: int, persona_id: int, story_id: int, universe_id: int, memory_service: MemoryService = Depends(get_memory_service)) -> Memory:
    return memory_service.generate(persona_id=persona_id,
                                   story_id=story_id,
                                   universe_id=universe_id,
                                   conversation_id=conversation_id)
