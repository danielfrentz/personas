from fastapi import Depends, APIRouter

from endpoint import get_clothing_service
from models.clothing import Clothing
from service.persona_domain.clothing_service import ClothingService

clothing_rest_router = APIRouter(prefix="/clothing")

@clothing_rest_router.post("/", response_model=Clothing)
async def create_accessory(persona_id: int, clothing: Clothing, clothing_service: ClothingService = Depends(get_clothing_service)):
    return clothing_service.save(persona_id=persona_id, clothing=clothing)

@clothing_rest_router.delete("/{clothing_id}/")
async def delete_accessory(clothing_id: int, clothing_service: ClothingService = Depends(get_clothing_service)):
    return clothing_service.delete(clothing_id)

@clothing_rest_router.get("/")
async def get_clothing(persona_id: int, clothing_service: ClothingService = Depends(get_clothing_service)):
    return clothing_service.find_by_persona_id(persona_id=persona_id)
