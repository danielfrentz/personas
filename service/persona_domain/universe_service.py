from converter.universe_converter import UniverseConverter
from converter.universe_metadata_converter import UniverseMetadataConverter
from dao.universe_dao import UniverseDAO
from entity.base import UniverseEntity
from models.ai.input.universe import UniverseInput
from models.ai.output.universe_ai import UniverseDescriptionAI
from models.universe import Universe
from models.universe_description import UniverseDescription
from service.ai.ai_service import AIService


class UniverseService:
    def __init__(self, ai_service: AIService,
                 universe_dao: UniverseDAO,
                 universe_converter: UniverseConverter,
                 universe_metadata_converter: UniverseMetadataConverter):
        self.ai_service = ai_service
        self.universe_dao = universe_dao
        self.universe_converter = universe_converter
        self.universe_metadata_converter = universe_metadata_converter

    def generate_environment(self, universe_id: int) -> UniverseDescription:
        universe: Universe = self.universe_converter.entity_to_model(self.universe_dao.find_by_id(universe_id))
        print(universe.metadata)
        universe_input = UniverseInput(
            description=universe.description.description,
            inhabitants=universe.description.creatures,
            metadata=universe.metadata
        )
        generated_description = self.ai_service.call_llm("enhance_universe",
                                                         return_type=UniverseDescriptionAI,
                                                         user_data=universe_input,
                                                         universe_id=universe_id)
        return self.universe_converter.ai_to_model(generated_description)


    def save(self, universe: Universe) -> Universe:
        universe_entity: UniverseEntity = self.universe_converter.model_to_entity(universe)
        universe_entity = self.universe_dao.save(universe_entity)
        return self.universe_converter.entity_to_model(universe_entity=universe_entity)

    def find_by_id(self, universe_id: int) -> Universe:
        universe_entity = self.universe_dao.find_by_id(universe_id)
        return self.universe_converter.entity_to_model(universe_entity=universe_entity)

    def delete(self, universe_id: int):
        self.universe_dao.delete(universe_id)

    def exists(self, universe_id):
        print(self.universe_dao.exists(universe_id))
        return self.universe_dao.exists(universe_id)

    def find_all(self):
        return self.universe_dao.find_all()

