from fastapi import APIRouter, Depends

from endpoint import get_data_generation_service
from models.http.request.data.data_generation_request import DataGenerationRequest
from service.data_gen.data_generation_service import DataGenerationService

data_generation_router = APIRouter(prefix="/data_generation", tags=["data_generation"])


@data_generation_router.get("/universe/{universe_id}")
async def data_generation(universe_id: int,  request: DataGenerationRequest,  data_generation_service: DataGenerationService = Depends(get_data_generation_service)) -> dict:
    return data_generation_service.generate(universe_id=universe_id, data_gen_request=request)