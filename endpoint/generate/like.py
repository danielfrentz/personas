from fastapi import APIRouter, Depends

from endpoint import get_like_service
from service.persona_domain.like_service import LikeService

like_generate_router = APIRouter(prefix="/like")
@like_generate_router.post("/")
async def generate(persona_id: int, universe_id: int, like_service: LikeService = Depends(get_like_service)):
    return like_service.generate(persona_id, universe_id)
