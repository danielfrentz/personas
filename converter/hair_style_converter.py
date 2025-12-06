from entity.base import HairStyleEntity
from models.hair_style import HairStyle


class HairStyleConverter:
    def __init__(self):
        pass

    def model_to_entity(self, hairstyle: HairStyle) -> HairStyleEntity:
        return HairStyleEntity(
            name=hairstyle.name,
            description=hairstyle.description,
            occasion=hairstyle.occasion,
        )
    def entity_to_model(self, hairstyle_entity: HairStyleEntity) -> HairStyle:
        return HairStyle(
            id=hairstyle_entity.id,
            physical_description_id=hairstyle_entity.physical_description_id,
            name=hairstyle_entity.name,
            description=hairstyle_entity.description,
            occasion=hairstyle_entity.occasion,
        )

    def ai_to_model(self, hair_ai):
        return HairStyle(
            name=hair_ai.habit_name,
            description=hair_ai.description,
            occasion=hair_ai.occasion,
        )
