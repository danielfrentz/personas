from fastapi import APIRouter, Depends

from endpoint import get_introspection_service
from models.http.request.generate.introspection_request import IntrospectionRequest
from models.introspection import Introspection
from service.persona_domain.introspection_service import IntrospectionService

introspection_generate_router = APIRouter(prefix="/{story_id}/introspection")


@introspection_generate_router.post("/")
async def generate(persona_id: int,
                   story_id: int,
                   introspection_request: IntrospectionRequest,
                   introspection_service: IntrospectionService = Depends(get_introspection_service)) -> Introspection:
    return introspection_service.generate(persona_id=persona_id, story_id=story_id, introspection_request=introspection_request)


