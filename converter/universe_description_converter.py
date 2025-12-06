from converter.universe_location_converter import UniverseLocationConverter
from entity.base import UniverseDescriptionEntity
from models.ai.output.universe_ai import UniverseDescriptionAI
from models.universe_description import UniverseDescription


class UniverseDescriptionConverter(object):
    def __init__(self, universe_location_converter: UniverseLocationConverter):
        self.universe_location_converter = universe_location_converter

    def model_to_entity(self, model: UniverseDescription) -> UniverseDescriptionEntity | None:
        if model is None:
            return None
        result = UniverseDescriptionEntity(
            description=model.description,
            creatures=model.creatures,
            universe_id=model.universe_id
        )
        return result


    def entity_to_model(self, entity: UniverseDescriptionEntity) -> UniverseDescription | None:
        if entity is None:
            return None
        return UniverseDescription(
            id=entity.id,
            universe_id=entity.universe_id,
            description=entity.description,
            creatures=entity.creatures,
        )

    def model_to_ai(self, model: UniverseDescription) -> UniverseDescriptionAI:
        return UniverseDescriptionAI(
            description=model.description,
            inhabitants=model.creatures

        )

    def ai_to_model(self, model:UniverseDescriptionAI) -> UniverseDescription:
        return UniverseDescription(
            description=model.description,
            creatures=model.creatures
        )
