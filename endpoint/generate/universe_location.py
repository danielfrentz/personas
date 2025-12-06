from fastapi import APIRouter, Depends

from endpoint import get_universe_location_service
from service.persona_domain.universe_location_service import UniverseLocationService

universe_location_generate_router = APIRouter(prefix="/{universe_id}/location")

@universe_location_generate_router.post("/")
async def generate_universe_location(universe_id: int, universe_location_service: UniverseLocationService = Depends(get_universe_location_service)):
    return universe_location_service.generate(universe_id)

