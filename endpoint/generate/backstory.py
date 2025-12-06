from typing import List

from fastapi import APIRouter, Depends

from endpoint import get_backstory_service
from endpoint.generate.aspect import aspect_generate_router
from endpoint.generate.habit import habit_generate_router
from endpoint.generate.hobby import hobby_router
from endpoint.generate.like import like_generate_router
from models.backstory import Backstory
from models.http.request.generate.backstory_generate_request import BackstoryGenerateRequest
from service.persona_domain.backstory_service import BackstoryService

backstory_generate_router = APIRouter(prefix="/{persona_id}/backstory")
backstory_generate_router.include_router(like_generate_router)
backstory_generate_router.include_router(habit_generate_router)
backstory_generate_router.include_router(hobby_router)
backstory_generate_router.include_router(aspect_generate_router)
@backstory_generate_router.post("/")
async def generate(universe_id: int,
                    backstory_generate_request: BackstoryGenerateRequest,
                           backstory_service: BackstoryService = Depends(get_backstory_service),
                           ) -> Backstory:
    return backstory_service.generate(universe_id=universe_id, request=backstory_generate_request)

@backstory_generate_router.get("/")
async def get(backstory_service: BackstoryService = Depends(get_backstory_service)) -> List[Backstory]:
    return backstory_service.find_all()

@backstory_generate_router.delete("/{backstory_id}")
async def delete(backstory_id: int, backstory_service: BackstoryService = Depends(get_backstory_service)) -> Backstory:
    return backstory_service.delete(backstory_id)

@backstory_generate_router.get("/")
async def get_all(persona_id: int, backstory_service: BackstoryService = Depends(get_backstory_service)) -> Backstory:
    return backstory_service.find_by_persona_id(persona_id)
