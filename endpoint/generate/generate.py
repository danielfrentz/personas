from fastapi import APIRouter

from endpoint.generate.universe import universe_generate_router

generate_router = APIRouter(prefix="/generate")

generate_router.include_router(universe_generate_router)
