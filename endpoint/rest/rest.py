from fastapi import APIRouter

from endpoint.rest.universe import universe_rest_router

rest_router = APIRouter(prefix="/rest")
rest_router.include_router(universe_rest_router)