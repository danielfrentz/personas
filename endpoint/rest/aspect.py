from typing import List

from fastapi import APIRouter, Depends

from endpoint import get_persona_aspect_service
from models.persona_aspect import PersonaAspect
from service.persona_domain.persona_aspect_service import PersonaAspectService

aspect_rest_router = APIRouter(prefix="/aspect")

@aspect_rest_router.post("/")
async def create_aspect(persona_id: int, aspect: PersonaAspect, persona_aspect_service: PersonaAspectService = Depends(get_persona_aspect_service)) -> PersonaAspect:
    return persona_aspect_service.save(persona_id=persona_id, persona_aspect=aspect)

@aspect_rest_router.get("/")
async def get_aspects(persona_id: int, persona_aspect_service: PersonaAspectService = Depends(get_persona_aspect_service)) -> List[PersonaAspect]:
    return persona_aspect_service.find_by_persona(persona_id=persona_id)

@aspect_rest_router.get("/{aspect_id}/")
async def get_aspect(aspect_id: int, persona_aspect_service: PersonaAspectService = Depends(get_persona_aspect_service)) -> PersonaAspect:
    return persona_aspect_service.find_by_id(aspect_id)
