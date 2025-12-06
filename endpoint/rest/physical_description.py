from fastapi import APIRouter, Depends

from endpoint import get_physical_description_service
from endpoint.rest.accessory import accessory_rest_router
from endpoint.rest.clothing import clothing_rest_router
from models.physical_description import PhysicalDescription
from service.persona_domain.physical_description_service import PhysicalDescriptionService

physical_description_rest_router = APIRouter(prefix="/{persona_id}/physical_description")
physical_description_rest_router.include_router(clothing_rest_router)
physical_description_rest_router.include_router(accessory_rest_router)


@physical_description_rest_router.put(path="/")
async def create_physical_description(persona_id: int,
                                      physical_description: PhysicalDescription,
                                      physical_description_service: PhysicalDescriptionService = Depends(
                                          get_physical_description_service)) -> PhysicalDescription:
    return physical_description_service.save(persona_id=persona_id, physical_description=physical_description)

@physical_description_rest_router.get(path="/")
async def get_physical_description(persona_id: int, physical_description_service: PhysicalDescriptionService = Depends(get_physical_description_service)) -> PhysicalDescription:
    return physical_description_service.find_by_persona_id(persona_id)

@physical_description_rest_router.delete(path="/{physical_description_id}")
async def delete_physical_description(physical_description_id: int, physical_description_service: PhysicalDescriptionService = Depends(get_physical_description_service)) -> PhysicalDescription:
    return physical_description_service.delete(physical_description_id)
