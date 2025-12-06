from typing import List

from fastapi import APIRouter, Depends

from endpoint import get_accessory_service
from models.accessory import Accessory
from service.persona_domain.accessory_service import AccessoryService

accessory_rest_router = APIRouter(prefix="/accessory")

@accessory_rest_router.post("/", response_model=Accessory)
async def create_accessory(persona_id: int, accessory: Accessory, accessory_service: AccessoryService = Depends(get_accessory_service)):
    return accessory_service.save(accessory, persona_id)

@accessory_rest_router.get("/", response_model=List[Accessory])
async def get_accessories(persona_id: int, accessory_service: AccessoryService = Depends(get_accessory_service)) -> List[Accessory]:
    return accessory_service.get_by_persona_id(persona_id)

@accessory_rest_router.get("/{accessory_id}/")
async def get_accessory(accessory_id: int, accessory_service: AccessoryService = Depends(get_accessory_service)) -> Accessory:
    return accessory_service.find_by_id(accessory_id)

@accessory_rest_router.delete("/{accessory_id}/")
async def delete_accessory(accessory_id: int, accessory_service: AccessoryService = Depends(get_accessory_service)):
    return accessory_service.delete(accessory_id)