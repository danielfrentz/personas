from fastapi import APIRouter, Depends

from endpoint import get_universe_location_service
from models.universe_location import UniverseLocation
from service.persona_domain.universe_location_service import UniverseLocationService

universe_location_rest_router = APIRouter(prefix="/{universe_id}/location")

@universe_location_rest_router.post("/")
def create(universe_id: int, universe_location: UniverseLocation, universe_location_service: UniverseLocationService = Depends(get_universe_location_service)):
    return universe_location_service.save(universe_id=universe_id, universe_location=universe_location)


@universe_location_rest_router.get("/")
def get(universe_id: int, universe_location_service: UniverseLocationService=Depends(get_universe_location_service)):
    return universe_location_service.find_by_universe_id(universe_id=universe_id)

@universe_location_rest_router.get("/")
def get(universe_location_id: int, universe_location_service: UniverseLocationService=Depends(get_universe_location_service)):
    return universe_location_service.find_by_id(universe_location_id=universe_location_id)

@universe_location_rest_router.delete("/{universe_location_id}")
def delete(universe_location_id: int, universe_location_service: UniverseLocationService=Depends(get_universe_location_service)):
    return universe_location_service.delete(universe_location_id=universe_location_id)