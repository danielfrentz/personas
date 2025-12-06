from typing import List, Callable

from converter.memory_converter import MemoryConverter
from dao.memory_dao import MemoryDAO
from models.ai.input.memory_input import MemoryInput
from models.ai.output.memory_ai import MemoryAI
from models.memory import Memory
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.story_conversation_service import StoryConversationService
from service.persona_domain.story_service import StoryService


class MemoryService:
    def __init__(self, memory_dao: MemoryDAO,
                 memory_converter: MemoryConverter,
                 ai_service: AIService,
                 persona_service: PersonaService,
                 story_service: StoryService,
                 story_conversation_service: StoryConversationService):
        self.memory_dao = memory_dao
        self.memory_converter = memory_converter
        self.ai_service = ai_service
        self.persona_service = persona_service
        self.story_service = story_service
        self.conversation_service = story_conversation_service


    def save(self, memory: Memory) -> Memory:
        memory_entity = self.memory_converter.model_to_entity(memory)
        memory_entity = self.memory_dao.save(memory_entity)
        return self.memory_converter.entity_to_model(memory_entity)

    def generate(self, persona_id: int, story_id: int, universe_id: int, conversation_id: int) -> Memory:
        persona = self.persona_service.find_by_id(persona_id)
        story = self.story_service.find_by_id(story_id)
        conversation = self.conversation_service.find_by_id(conversation_id)
        recent_memories = self.get_memories_by_story_id(story.id)
        memory_input = MemoryInput(
            backstory=persona.backstory,
            story=story,
            conversation=conversation,
            recent_memories=recent_memories
        )
        memories: MemoryAI = self.ai_service.call_llm("create_story_memories", MemoryAI, memory_input, universe_id=universe_id, validator=self.create_validator(recent_memories))
        return self.memory_converter.ai_to_model(memories, story.title, story_id)

    def get_memories_by_story_id(self, story_id) -> List[Memory]:
        entities = self.memory_dao.find_by_story_id(story_id)
        return [self.memory_converter.entity_to_model(memory) for memory in entities]

    def find_by_id(self, memory_id) -> Memory:
        memory_entity = self.memory_dao.find_by_id(memory_id)
        return self.memory_converter.entity_to_model(memory_entity)

    def find_by_story_id(self, story_id):
        memory_entities = self.memory_dao.find_by_story_id(story_id)
        return [self.memory_converter.entity_to_model(memory_entity) for memory_entity in memory_entities]

    def create_validator(self, recent_memories: List[Memory]) -> Callable:
        def validator(memory: MemoryAI):
            for recent_memory in recent_memories:
                if recent_memory.memory_text == memory.memory_text:
                    raise ValueError(f"The text must not be the same as another memory and yet it is the same as memory {recent_memory.memory_text}. Please ensure you check the previous memories and create a new one.")
        return validator

    def delete(self, memory_id: int):
        self.memory_dao.delete(memory_id)