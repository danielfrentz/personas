from fastapi import APIRouter, Depends

from endpoint import get_objective_persona_description_service
from models.http.request.generate.raw_persona_request import ObjectivePersonaRequest
from service.persona_domain.persona_objective_description_service import PersonaObjectiveDescriptionService

persona_objective_description_generate_router = APIRouter(prefix="/objective_description")

@persona_objective_description_generate_router.post("/")
async def generate_objective_description(request: ObjectivePersonaRequest, universe_id: int, objective_persona_description_service: PersonaObjectiveDescriptionService=Depends(get_objective_persona_description_service)):
    return objective_persona_description_service.generate(universe_id=universe_id, raw_persona_request=request)
