from entity.base import HobbyEntity
from models.ai.output.hobby_ai import HobbyAI
from models.hobby import Hobby


class HobbyConverter:
    def model_to_entity(self, hobby: Hobby) -> HobbyEntity:
        return HobbyEntity(
            id=hobby.id,
            name=hobby.name,
            description=hobby.description,
            backstory_id=hobby.backstory_id,
        )

    def entity_to_model(self, hobby_entity: HobbyEntity) -> Hobby:
        return Hobby(
            id=hobby_entity.id,
            name=hobby_entity.name,
            description=hobby_entity.description,
            backstory_id=hobby_entity.backstory_id,
        )

    def ai_to_model(self, hobby: HobbyAI) -> Hobby:
        return Hobby(
            name=hobby.name,
            description=hobby.description,
        )