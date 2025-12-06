from fastapi import APIRouter, Depends

from endpoint import get_introspection_service
from models.introspection import Introspection
from service.persona_domain.introspection_service import IntrospectionService

introspection_rest_router = APIRouter(prefix="/{story_id}/introspection")

@introspection_rest_router.post("/")
async def save(introspection: Introspection, introspection_service: IntrospectionService = Depends(get_introspection_service)):
    return introspection_service.save(introspection)

@introspection_rest_router.get("/")
async def get_all(story_id: int, introspection_service: IntrospectionService = Depends(get_introspection_service)):
    return introspection_service.find_by_story_id(story_id)

@introspection_rest_router.get("/{introspection_id}")
async def get_by_id(introspection_id: int, introspection_service: IntrospectionService = Depends(get_introspection_service)):
    return introspection_service.find_by_id(introspection_id)

@introspection_rest_router.delete("/{introspection_id}")
async def delete(introspection_id: int, introspection_service: IntrospectionService = Depends(get_introspection_service)):
    return introspection_service.delete(introspection_id)