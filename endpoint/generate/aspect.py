from fastapi import APIRouter, Depends

from endpoint import get_persona_aspect_service
from models.http.request.generate.persona_aspect_request import PersonaAspectRequest
from models.persona_aspect import PersonaAspect
from service.persona_domain.persona_aspect_service import PersonaAspectService

aspect_generate_router = APIRouter(prefix="/aspect")

@aspect_generate_router.post("/")
async def generate_aspect(persona_id: int,
                          universe_id: int,
                          aspect_request: PersonaAspectRequest,
                          persona_aspect_service: PersonaAspectService = Depends(get_persona_aspect_service)) -> PersonaAspect:
    return persona_aspect_service.generate(persona_id=persona_id, universe_id=universe_id, persona_aspect_request=aspect_request)