from fastapi import APIRouter, Depends

from endpoint import get_memory_service
from models.memory import Memory
from service.persona_domain.memory_service import MemoryService

memory_rest_router = APIRouter(prefix="/{conversation_id}/memory")

@memory_rest_router.post("/")
async def save(memory: Memory, memory_service: MemoryService = Depends(get_memory_service)) -> Memory:
    return memory_service.save(memory)

@memory_rest_router.get("/{memory_id}")
async def get_by_id(memory_id: int, memory_service: MemoryService = Depends(get_memory_service)) -> Memory:
    return memory_service.find_by_id(memory_id)

@memory_rest_router.get("/")
async def get_all(story_id: int, memory_service: MemoryService = Depends(get_memory_service)) -> Memory:
    return memory_service.find_by_story_id(story_id=story_id)

@memory_rest_router.delete("/{memory_id}")
async def delete(memory_id: int, memory_service: MemoryService = Depends(get_memory_service)) -> Memory:
    return memory_service.delete(memory_id)
