from fastapi import APIRouter, Depends

from endpoint import get_clothing_service
from service.persona_domain.clothing_service import ClothingService

clothing_generate_router = APIRouter(prefix="/clothing")

@clothing_generate_router.post("/")
async def generate_clothing(persona_id: int, universe_id:int, clothing_service: ClothingService = Depends(get_clothing_service)):
    return clothing_service.generate(persona_id, universe_id)

@clothing_generate_router.get("/{clothing_id}/")
async def get_clothing(clothing_id: int, clothing_service: ClothingService = Depends(get_clothing_service)):
    return clothing_service.find_by_id(clothing_id=clothing_id)

