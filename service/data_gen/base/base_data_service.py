import random

from service.persona_domain.universe_service import UniverseService


class BaseDataService:
    def __init__(self, universe_service: UniverseService):
        self.universe_service = universe_service

    def generate(self, universe_id: int) -> list[str]:
        result = {}

        return result

