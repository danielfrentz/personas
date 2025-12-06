from fastapi import APIRouter, Depends

from endpoint import get_relationship_service
from models.relationship import Relationship
from service.persona_domain.relationship_service import RelationshipService

relationship_rest_router = APIRouter(prefix="/{persona_id}/relationship")

@relationship_rest_router.post("/")
async def create_relationship(persona_id: int, relationship: Relationship, relationship_service: RelationshipService = Depends(get_relationship_service)):
    return relationship_service.save(relationship)

@relationship_rest_router.get("/")
async def get_by_persona(persona_id: int, relationship_service: RelationshipService = Depends(get_relationship_service)):
    relationship_service.get_by_persona_id(persona_id=persona_id)

@relationship_rest_router.delete("/{relationship_id}")
async def delete(relationship_id: int, relationship_service: RelationshipService = Depends(get_relationship_service)):
    return relationship_service.delete(relationship_id)