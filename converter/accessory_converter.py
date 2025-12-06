from entity.base import AccessoryEntity
from models.accessory import Accessory
from models.ai.output.accessory_ai import AccessoryAI


class AccessoryConverter:
    def model_to_entity(self, accessory: Accessory) -> AccessoryEntity:
        return AccessoryEntity(
            item_type=accessory.item_type,
            description=accessory.description,
            occasion=accessory.occasion,
            personal_significance=accessory.personal_significance,
            name=accessory.name,
            physical_description_id=accessory.physical_description_id,
            diffusion_model_description=accessory.diffusion_model_description
        )

    def entity_to_model(self, accessory: AccessoryEntity) -> Accessory:
        result = Accessory(
            physical_description_id=accessory.physical_description_id,
            name=accessory.name,
            item_type=accessory.item_type,
            description=accessory.description,
            occasion=accessory.occasion,
            personal_significance=accessory.personal_significance,
            diffusion_model_description=accessory.diffusion_model_description
        )
        result.id = accessory.id
        return result

    def ai_to_model(self, model: AccessoryAI, physical_description_id: int) -> Accessory:
        return Accessory(
            physical_description_id=physical_description_id,
            name=model.accessory_name,
            occasion=model.wearing_occasion,
            item_type=model.accessory_type,
            description=model.detailed_accessory_description,
            personal_significance=model.personal_significance,
            diffusion_model_description=model.diffusion_model_description
        )