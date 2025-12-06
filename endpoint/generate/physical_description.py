from fastapi import APIRouter, Depends

from endpoint import get_physical_description_service
from endpoint.generate.accessory import accessory_generate_router
from endpoint.generate.clothing import clothing_generate_router
from models.physical_description import PhysicalDescription
from service.persona_domain.physical_description_service import PhysicalDescriptionService

physical_description_generate_router = APIRouter(prefix="/{persona_id}/physical_description")

physical_description_generate_router.include_router(clothing_generate_router)
physical_description_generate_router.include_router(accessory_generate_router)

@physical_description_generate_router.post(path="/")
async def generate_physical_description(persona_id: int,
                                        universe_id: int,
                                        physical_description_service: PhysicalDescriptionService = Depends(get_physical_description_service),
                                        ) -> PhysicalDescription:
    return physical_description_service.generate(persona_id=persona_id, universe_id=universe_id)

