from fastapi import APIRouter, Depends

from endpoint import get_universe_service
from endpoint.rest.monologue import monologue_rest_router
from endpoint.rest.persona import persona_rest_router
from endpoint.rest.self_description_conversation import self_description_conversation_rest_router
from endpoint.rest.universe_description import universe_description_rest_router
from endpoint.rest.universe_location import universe_location_rest_router
from models.universe import Universe
from service.persona_domain.universe_service import UniverseService

universe_rest_router = APIRouter(prefix="/universe")
universe_rest_router.include_router(persona_rest_router)
universe_rest_router.include_router(universe_description_rest_router)
universe_rest_router.include_router(universe_location_rest_router)
universe_rest_router.include_router(monologue_rest_router)
universe_rest_router.include_router(self_description_conversation_rest_router)
@universe_rest_router.post(path="/")
async def create_universe(universe: Universe,
                          universe_service: UniverseService = Depends(get_universe_service)) -> Universe:
    return universe_service.save(universe)

@universe_rest_router.get(path="/{universe_id}")
async def get_universe(universe_id: int, universe_service: UniverseService = Depends(get_universe_service)):
    return universe_service.find_by_id(universe_id)

@universe_rest_router.get(path="/")
async def get_universes(universe_service: UniverseService = Depends(get_universe_service)):
    return universe_service.find_all()
@universe_rest_router.delete(path="/{universe_id}")
async def delete(universe_id: int, universe_service: UniverseService = Depends(get_universe_service)):
    return universe_service.delete(universe_id)