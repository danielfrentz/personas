from entity.base import MemoryEntity
from models.ai.output.memory_ai import MemoryAI
from models.memory import Memory


class MemoryConverter:
    def entity_to_model(self, memory_entity: MemoryEntity) -> Memory:
        return Memory(
            id=memory_entity.id,
            memory_text=memory_entity.memory.lower(),
            core_memory=memory_entity.core_memory,
            feelings_stirred=memory_entity.feelings_stirred,
            story_id=memory_entity.story_id,
            memory_reflex=memory_entity.memory_reflex,
            memory_reflex_followup=memory_entity.memory_reflex_followup,
        )

    def model_to_entity(self, model: Memory) -> MemoryEntity:
        return MemoryEntity(
            memory=model.memory_text.lower(),
            core_memory=model.core_memory,
            feelings_stirred=model.feelings_stirred,
            story_id=model.story_id,
            memory_reflex=model.memory_reflex,
            memory_reflex_followup=model.memory_reflex_followup
        )


    def ai_to_model(self, model: MemoryAI, story_title: str, story_id:int) -> Memory:
        return Memory(
            feelings_stirred=model.feelings_stirred,
            story_title=story_title,
            memory_text=model.memory_text.lower(),
            core_memory=model.is_core_memory,
            story_id=story_id,
            memory_reflex=model.memory_reflex,
            memory_reflex_followup=model.memory_reflex_followup,
        )