import random

from converter.backstory_converter import BackstoryConverter
from converter.conversation_converter import ConversationConverter
from dao.conversation_dao import ConversationDAO
from entity.base import ConversationEntity
from models.ai.input.story_conversation_input import ConversationInput
from models.ai.output.conversation_ai import ConversationAI
from models.conversation import Conversation
from models.story import Story
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.story_service import StoryService
from service.persona_domain.universe_service import UniverseService


class StoryConversationService:
    def __init__(self, conversation_converter: ConversationConverter,
                 conversation_dao: ConversationDAO,
                 persona_service: PersonaService,
                 ai_service: AIService,
                 universe_service: UniverseService,
                 story_service: StoryService,
                 backstory_converter: BackstoryConverter,):
        self.conversation_converter = conversation_converter
        self.conversation_dao = conversation_dao
        self.ai_service = ai_service
        self.story_service = story_service
        self.persona_service = persona_service
        self.universe_service = universe_service
        self.backstory_converter = backstory_converter

    def generate(self, story_id: int, universe_id, persona_id) -> Conversation:
        story = self.story_service.find_by_id(story_id)
        persona = self.persona_service.find_by_id(persona_id)
        speech_profiles = {}
        for character in story.characters:
            character = self.persona_service.find_by_name(character)
            if character is not None:
                profile = character.speech_profile.model_copy()
                random.shuffle(profile.samples)
                profile.samples = profile.samples
                speech_profiles[character.name] = profile
        conversation_input = ConversationInput(
            story=story.story,
            backstory=persona.backstory,
            relationships=persona.relationships,
            speech_profiles=speech_profiles
        )
        generated_conversation = self.ai_service.call_llm(system_prompt_name="create_story_conversation", return_type=ConversationAI, user_data=conversation_input, universe_id=universe_id, validator=self.validate())
        return self.conversation_converter.ai_to_model(generated_conversation)

    def validate(self):
        def validation(conversation: ConversationAI):
            if len(conversation.conversation_turns) == 0:
                raise ValueError("Conversation must have at least one turn")
        return validation
    def find_by_id(self, conversation_id):
        conversation_entity: ConversationEntity = self.conversation_dao.find_by_id(conversation_id)
        return self.conversation_converter.entity_to_model(conversation_entity)

    def save(self, conversation: Conversation, story_id: int) -> Conversation:
        conversation.source_id = story_id
        conversation_entity: ConversationEntity = self.conversation_converter.model_to_entity(conversation)
        conversation_entity.source = Story.__name__
        conversation_entity.source_id = story_id
        self.conversation_dao.save(conversation_entity)
        result = self.conversation_converter.entity_to_model(conversation_entity)
        result.source_id = story_id
        return result

    def find_by_story_id(self, story_id: int) -> Conversation | None:
        conversation = self.conversation_dao.find_by_id_and_source(story_id, Story.__name__)
        return self.conversation_converter.entity_to_model(conversation_entity=conversation)

    def delete_by_id(self, conversation_id: int):
        self.conversation_dao.delete(conversation_id)

