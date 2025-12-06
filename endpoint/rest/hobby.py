from typing import List

from fastapi import APIRouter, Depends

from endpoint import get_hobby_service
from models.hobby import Hobby
from service.persona_domain.hobby_service import HobbyService

hobby_router = APIRouter(prefix="/hobby")

@hobby_router.post("/")
async def save(persona_id, hobby: Hobby, hobby_service: HobbyService = Depends(get_hobby_service)):
    return hobby_service.save(persona_id=persona_id, hobby=hobby)

@hobby_router.delete("/{hobby_id}")
async def delete(hobby_id, hobby_service: HobbyService = Depends(get_hobby_service)):
    return hobby_service.delete(hobby_id)

@hobby_router.get("/")
async def get(persona_id: int, hobby_service: HobbyService = Depends(get_hobby_service)) -> List[Hobby]:
    return hobby_service.find_by_persona_id(persona_id=persona_id)
