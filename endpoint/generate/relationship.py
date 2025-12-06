from fastapi import APIRouter, Depends

from endpoint import get_relationship_service
from models.http.relationship_request import RelationshipRequest
from models.relationship import Relationship
from service.persona_domain.relationship_service import RelationshipService

relationship_generate_router = APIRouter(prefix="/{persona_id}/relationship")

@relationship_generate_router.post("/")
async def generate_relationship(relationship_request: RelationshipRequest, universe_id: int, relationship_service: RelationshipService = Depends(get_relationship_service)) -> Relationship:
    return relationship_service.generate(relationship_request=relationship_request, universe_id=universe_id)
