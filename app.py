import logging

from starlette.middleware.cors import CORSMiddleware

from endpoint.data.data import data_generation_router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"

)

logger = logging.getLogger(__name__)

logger.info("App is starting up!")
from fastapi import FastAPI


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from endpoint.generate.generate import generate_router
from endpoint.rest.rest import rest_router
app.include_router(rest_router)
app.include_router(generate_router)
app.include_router(data_generation_router)