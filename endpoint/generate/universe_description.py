from fastapi import APIRouter, Depends

from endpoint import get_universe_service
from models.universe_description import UniverseDescription
from service.persona_domain.universe_service import UniverseService

universe_description_generate_router = APIRouter(prefix="/{universe_id}/description")

@universe_description_generate_router.post("/")
async def generate_universe(universe_id: int, environment_service: UniverseService = Depends(get_universe_service)) -> UniverseDescription:
    return environment_service.generate_environment(universe_id=universe_id)