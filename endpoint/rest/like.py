from fastapi import APIRouter, Depends

from endpoint import get_like_service
from models.like import Like
from service.persona_domain.like_service import LikeService

like_rest_router = APIRouter(prefix="/like")
@like_rest_router.post("/")
async def save(persona_id: int, like: Like, like_service: LikeService = Depends(get_like_service)):
    return like_service.save(persona_id, like)

@like_rest_router.delete("/{like_id}")
async def delete(like_id: int, like_service: LikeService = Depends(get_like_service)):
    return like_service.delete(like_id)

@like_rest_router.get("/")
async def get_likes(persona_id: int, like_service: LikeService = Depends(get_like_service)):
    return like_service.find_by_persona_id(persona_id)
