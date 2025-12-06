from fastapi import APIRouter, Depends

from endpoint import get_accessory_service
from service.persona_domain.accessory_service import AccessoryService

accessory_generate_router = APIRouter(prefix="/accessory")

@accessory_generate_router.post("/")
async def generate_clothing(persona_id: int, universe_id: int, accessory_service: AccessoryService = Depends(get_accessory_service)):
    return accessory_service.generate(persona_id, universe_id)
