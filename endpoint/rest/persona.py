from fastapi import APIRouter, Depends

from endpoint import get_persona_service, check_universe_exists
from endpoint.rest.aspect import aspect_rest_router
from endpoint.rest.backstory import backstory_rest_router
from endpoint.rest.group_reasoning import group_reasoning_style_rest_router
from endpoint.rest.life_event import life_event_rest_router
from endpoint.rest.persona_fact import persona_fact_rest_router
from endpoint.rest.physical_description import physical_description_rest_router
from endpoint.rest.reasoning import reasoning_rest_router
from endpoint.rest.relationship import relationship_rest_router
from endpoint.rest.self_description_conversation import self_description_conversation_rest_router
from endpoint.rest.speech import speech_profile_rest_router
from models.persona import Persona
from service.persona_domain.persona_service import PersonaService

persona_rest_router = APIRouter(prefix="/{universe_id}/persona", dependencies=[Depends(check_universe_exists)])
persona_rest_router.include_router(backstory_rest_router)
persona_rest_router.include_router(physical_description_rest_router)
persona_rest_router.include_router(speech_profile_rest_router)
persona_rest_router.include_router(life_event_rest_router)
persona_rest_router.include_router(reasoning_rest_router)
persona_rest_router.include_router(relationship_rest_router)
persona_rest_router.include_router(group_reasoning_style_rest_router)
persona_rest_router.include_router(self_description_conversation_rest_router)
persona_rest_router.include_router(persona_fact_rest_router)

@persona_rest_router.get(path="/{persona_id}/")
async def get_persona(persona_id: int,
                      persona_service: PersonaService = Depends(get_persona_service)):
    return persona_service.find_by_id(persona_id)

@persona_rest_router.post(path="/")
async def create_persona(persona: Persona,
                         persona_service: PersonaService = Depends(get_persona_service)) -> Persona:
    return persona_service.save(persona)

@persona_rest_router.get(path="/")
async def get_all(universe_id: int, persona_service: PersonaService = Depends(get_persona_service)):
    return persona_service.find_by_universe(universe_id=universe_id)

@persona_rest_router.delete(path="/{persona_id}")
async def delete(persona_id: int, persona_service: PersonaService = Depends(get_persona_service)):
    return persona_service.delete(persona_id)