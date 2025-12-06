from fastapi import APIRouter, Depends

from endpoint import get_persona_fact_service
from service.persona_domain.persona_fact_service import PersonaFactService

persona_fact_generate_router = APIRouter(prefix="/{persona_id}/fact")

@persona_fact_generate_router.post("/")
async def generate_persona_fact(persona_id: int, universe_id: int, persona_fact_service: PersonaFactService=Depends(get_persona_fact_service)):
    return persona_fact_service.generate(persona_id, universe_id)