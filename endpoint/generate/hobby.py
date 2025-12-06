from fastapi import APIRouter, Depends

from endpoint import get_hobby_service
from service.persona_domain.hobby_service import HobbyService

hobby_router = APIRouter(prefix="/hobby")

@hobby_router.post("/")
async def generate(persona_id: int, universe_id: int, hobby_service: HobbyService = Depends(get_hobby_service)):
    return hobby_service.generate(persona_id, universe_id)