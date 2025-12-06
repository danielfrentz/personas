from fastapi import APIRouter, Depends

from endpoint import get_universe_description_service
from models.universe_description import UniverseDescription
from service.persona_domain.universe_description_service import UniverseDescriptionService

universe_description_rest_router = APIRouter(prefix="/{universe_id}/description")


@universe_description_rest_router.put("/")
async def create_universe_description(universe_description: UniverseDescription,
                                      universe_id: int,
                                      universe_description_service: UniverseDescriptionService = Depends(
                                          get_universe_description_service)):
    universe_description.universe_id = universe_id
    return universe_description_service.update(universe_description, universe_id)


@universe_description_rest_router.get("/")
async def get_universe_description(universe_id: int,
                                   universe_description_service: UniverseDescriptionService = Depends(get_universe_description_service)):
    return universe_description_service.get(universe_id)
