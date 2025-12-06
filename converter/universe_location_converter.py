from entity.base import UniverseLocationEntity
from models.ai.output.universe_location_ai import UniverseLocationAI
from models.universe_location import UniverseLocation


class UniverseLocationConverter:
    def __init__(self):
        pass
    def entity_to_model(self, entity: UniverseLocationEntity) -> UniverseLocation:
        return UniverseLocation(
            id=entity.id,
            universe_id=entity.universe_id,
            name=entity.name,
            visual_description=entity.visual_description,
            purpose=entity.purpose
        )

    def model_to_entity(self, model: UniverseLocation) -> UniverseLocationEntity:
        return UniverseLocationEntity(
            id=model.id,
            universe_id=model.universe_id,
            name=model.name,
            visual_description=model.visual_description,
            purpose=model.purpose
        )

    def ai_to_model(self, model: UniverseLocationAI) -> UniverseLocation:
        return UniverseLocation(
            name=model.name,
            purpose=model.purpose,
            visual_description=model.visual_description
        )

    def model_to_ai(self, model: UniverseLocation) -> UniverseLocationAI:
        return UniverseLocationAI(
            name=model.name,
            purpose=model.purpose,
            visual_description=model.visual_description
        )

