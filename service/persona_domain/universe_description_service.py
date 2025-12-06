from converter.universe_description_converter import UniverseDescriptionConverter
from dao.universe_description_dao import UniverseDescriptionDAO
from models.universe_description import UniverseDescription


class UniverseDescriptionService:
    def __init__(self, universe_description_dao: UniverseDescriptionDAO,
                 universe_description_converter: UniverseDescriptionConverter):
        self.universe_description_dao = universe_description_dao
        self.universe_description_converter = universe_description_converter


    def update(self, universe_description: UniverseDescription, universe_id: int) -> UniverseDescription:
        universe_description_entity = self.universe_description_converter.model_to_entity(universe_description)
        universe_description_entity = self.universe_description_dao.update(universe_description_entity, universe_id)
        return self.universe_description_converter.entity_to_model(universe_description_entity)


    def find_by_id(self, universe_description_id: int) -> UniverseDescription:
        universe_description_entity = self.universe_description_dao.find_by_universe_id(universe_description_id)
        return self.universe_description_converter.entity_to_model(universe_description_entity)

    def find_by_universe_id(self, universe_description_id: int) -> UniverseDescription:
        universe_description_entity = self.universe_description_dao.find_by_universe_id(universe_description_id)
        return self.universe_description_converter.entity_to_model(universe_description_entity)

    def get(self, universe_id):
        universe_description_entity = self.universe_description_dao.find_by_universe_id(universe_id)
        return self.universe_description_converter.entity_to_model(universe_description_entity)

    def delete(self, universe_description_id):
        self.universe_description_dao.delete(universe_description_id)

