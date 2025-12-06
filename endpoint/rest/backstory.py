from fastapi import APIRouter, Depends

from endpoint import get_backstory_service
from endpoint.rest.aspect import aspect_rest_router
from endpoint.rest.habit import habit_rest_router
from endpoint.rest.hobby import hobby_router
from endpoint.rest.like import like_rest_router
from models.backstory import Backstory
from service.persona_domain.backstory_service import BackstoryService

backstory_rest_router = APIRouter(prefix="/{persona_id}/backstory")
backstory_rest_router.include_router(like_rest_router)
backstory_rest_router.include_router(habit_rest_router)
backstory_rest_router.include_router(hobby_router)
backstory_rest_router.include_router(aspect_rest_router)
@backstory_rest_router.post(path="/")
async def create_backstory(persona_id: int, backstory: Backstory,
                          backstory_service: BackstoryService = Depends(get_backstory_service)) -> Backstory:
    return backstory_service.save(backstory, persona_id)

@backstory_rest_router.get(path="/backstory/")
async def get_backstory(persona_id: int, backstory_service: BackstoryService = Depends(get_backstory_service)):
    return backstory_service.find_by_persona_id(persona_id)

@backstory_rest_router.delete(path="/{backstory_id}/")
async def delete(backstory_id: int, backstory_service: BackstoryService = Depends(get_backstory_service)):
    return backstory_service.delete(backstory_id)

