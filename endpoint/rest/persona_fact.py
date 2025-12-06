from fastapi import APIRouter, Depends

from endpoint import get_persona_fact_service
from models.persona_fact import PersonaFact
from service.persona_domain.persona_fact_service import PersonaFactService

persona_fact_rest_router = APIRouter(prefix="/{persona_id}/fact")

@persona_fact_rest_router.post("/")
async def save(persona_fact: PersonaFact, persona_id: int, persona_fact_service: PersonaFactService = Depends(get_persona_fact_service)):
    return persona_fact_service.save(persona_fact=persona_fact, persona_id=persona_id)

@persona_fact_rest_router.get("/")
async def get(persona_id: int, persona_fact_service: PersonaFactService = Depends(get_persona_fact_service)):
    return persona_fact_service.find_by_persona_id(persona_id=persona_id)