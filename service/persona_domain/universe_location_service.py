from typing import List

from converter.universe_description_converter import UniverseDescriptionConverter
from converter.universe_location_converter import UniverseLocationConverter
from dao.universe_location_dao import UniverseLocationDAO
from models.ai.input.universe_location_input import UniverseLocationInput
from models.ai.output.universe_location_ai import UniverseLocationAI
from models.universe_location import UniverseLocation
from service.ai.ai_service import AIService
from service.persona_domain.universe_description_service import UniverseDescriptionService


class UniverseLocationService:
    def __init__(self, universe_location_dao: UniverseLocationDAO,
                 universe_location_converter: UniverseLocationConverter,
                 ai_service: AIService,
                 universe_description_service: UniverseDescriptionService,
                 universe_description_converter: UniverseDescriptionConverter):
        self.universe_location_dao = universe_location_dao
        self.universe_location_converter = universe_location_converter
        self.ai_service = ai_service
        self.universe_description_service = universe_description_service
        self.universe_description_converter = universe_description_converter

    def generate(self, universe_id) -> UniverseLocation:
        universe_locations = self.find_by_universe_id(universe_id)
        universe_locations_ai = [self.universe_location_converter.model_to_ai(location) for location in universe_locations]
        universe_description = self.universe_description_service.find_by_universe_id(universe_id)
        universe_description_ai = self.universe_description_converter.model_to_ai(universe_description)
        universe_location_input = UniverseLocationInput(
            existing_locations=universe_locations_ai,
            universe_description=universe_description_ai
        )
        generated = self.ai_service.call_llm("create_universe_location", return_type=UniverseLocationAI, user_data=universe_location_input, universe_id=universe_id, validator=self.create_validation(universe_location_input))
        return self.universe_location_converter.ai_to_model(generated)

    def create_validation(self, universe_location_input: UniverseLocationInput):
        def validation(result: UniverseLocationAI):
            for location in universe_location_input.existing_locations:
                if location.name == result.name:
                    raise ValueError(f"The location {result.name} has already been used, choose another one that has not been used.")
                elif location.purpose == result.purpose:
                    raise ValueError(f"The description {result.description} matches an existing description, choose another one that does not match an existing description.")
        return validation
    def find_by_universe_id(self, universe_id: int) -> List[UniverseLocation]:
        universe_location_entities = self.universe_location_dao.get_by_universe(universe_id)
        return [self.universe_location_converter.entity_to_model(location) for location in universe_location_entities]

    def save(self, universe_id: int, universe_location: UniverseLocation):
        universe_location.universe_id = universe_id
        universe_location_entity = self.universe_location_converter.model_to_entity(universe_location)
        universe_location_entity = self.universe_location_dao.save(universe_location_entity)
        return self.universe_location_converter.entity_to_model(universe_location_entity)

    def find_by_id(self, universe_location_id):
        return self.universe_location_dao.find_by_id(universe_location_id)

    def delete(self, universe_location_id):
        self.universe_location_dao.delete(universe_location_id)

