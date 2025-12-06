import random
from typing import List

from converter.backstory_converter import BackstoryConverter
from converter.conversation_converter import ConversationConverter
from converter.introspection_converter import IntrospectionConverter
from dao.conversation_dao import ConversationDAO
from dao.introspection_dao import IntrospectionDAO
from models.ai.input.introspection_input import IntrospectionInput
from models.ai.output.introspection_ai import IntrospectionAI
from models.http.request.generate.introspection_request import IntrospectionRequest
from models.introspection import Introspection
from models.story import Story
from service.ai.ai_service import AIService
from service.persona_domain.conversation_service import ConversationService
from service.persona_domain.memory_service import MemoryService
from service.persona_domain.persona_aspect_service import PersonaAspectService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.speech_profile_service import SpeechProfileService


class IntrospectionService:
    def __init__(self, introspection_dao: IntrospectionDAO,
                 introspection_converter: IntrospectionConverter,
                 ai_service: AIService,
                 persona_service: PersonaService,
                 conversation_service: ConversationService,
                 speech_profile_service: SpeechProfileService,
                 memory_service: MemoryService,
                 conversation_converter: ConversationConverter,
                 conversation_dao: ConversationDAO,
                 backstory_converter: BackstoryConverter,
                 aspect_service: PersonaAspectService):
        self.introspection_dao = introspection_dao
        self.introspection_converter = introspection_converter
        self.ai_service = ai_service
        self.persona_service = persona_service
        self.conversation_service = conversation_service
        self.speech_profile_service = speech_profile_service
        self.memory_service = memory_service
        self.conversation_converter = conversation_converter
        self.conversation_dao = conversation_dao
        self.backstory_converter = backstory_converter
        self.aspect_service = aspect_service

    def generate(self, persona_id: int, story_id: int, introspection_request: IntrospectionRequest) -> Introspection:
        persona = self.persona_service.find_by_id(persona_id)
        speech_profile = self.persona_service.find_by_id(persona_id).speech_profile
        memories = self.memory_service.find_by_story_id(story_id=story_id)
        conversation = self.conversation_service.find_by_source_id(source_id=story_id, source=Story.__name__)
        random.shuffle(speech_profile.samples)
        speech_profile.samples = speech_profile.samples[:20]
        aspect = self.aspect_service.find_by_id(introspection_request.aspect_id)
        introspection_input = IntrospectionInput(
            backstory=persona.backstory,
            speech_pattern=speech_profile,
            relationships=persona.relationships,
            memories=[memory.memory_text for memory in memories],
            conversation=conversation,
            aspect=aspect,

        )
        introspection: IntrospectionAI = self.ai_service.call_llm("create_introspection",
                                                                  IntrospectionAI,
                                                                  introspection_input,
                                                                  universe_id=persona.universe_id,
                                                                  validator=self.validate(introspection_input))
        result = self.introspection_converter.ai_to_model(introspection, persona, story_id)
        result.aspect_id = aspect.id
        return result

    def validate(self, input_data: IntrospectionInput):
        def validation(introspection: Introspection):
            if len(introspection.internal_monologue.conversation_turns) == 0:
                raise ValueError("Conversation must have at least one turn")
            for conversation_turn in introspection.internal_monologue.conversation_turns:
                if len(conversation_turn.directed_at) != 1:
                    raise ValueError("The speaker must be the same as the persona background as it is an internal monologue.")
                if not conversation_turn.directed_at[0].lower() in [input_data.backstory.name.lower(), f"{input_data.backstory.name}'s {input_data.aspect.aspect_name}".lower()]:
                    raise ValueError("The speaker must be the same as the persona background as it is an internal monologue.")
        return validation

    def save(self, introspection: Introspection):
        introspection_entity = self.introspection_converter.model_to_entity(introspection)
        introspection_entity = self.introspection_dao.save(introspection_entity)
        conversation_entity = self.conversation_converter.model_to_entity(introspection.monologue)
        conversation_entity.source = Introspection.__name__
        conversation_entity.source_id = introspection_entity.id
        conversation_entity = self.conversation_dao.save(conversation_entity)

        result: Introspection = self.introspection_converter.entity_to_model(introspection_entity)
        result.monologue = self.conversation_converter.entity_to_model(conversation_entity)
        return result

    def find_by_id(self, introspection_id: int) -> Introspection:
        introspection_entity = self.introspection_dao.find_by_id(introspection_id)
        introspection_model = self.introspection_converter.entity_to_model(introspection_entity)
        conversation_entity = self.conversation_dao.find_by_id_and_source(introspection_id, Introspection.__name__)
        conversation_model = self.conversation_converter.entity_to_model(conversation_entity)
        introspection_model.monologue = conversation_model
        return introspection_model

    def find_by_story_id(self, story_id: int) -> List[Introspection]:
        introspection_entities = self.introspection_dao.find_by_story_id(story_id)
        introspections = [self.introspection_converter.entity_to_model(introspection_entity) for introspection_entity in introspection_entities]
        for introspection in introspections:
            conversation = self.conversation_service.find_by_source_id(source_id=introspection.id, source=Introspection.__name__)
            introspection.monologue = conversation
        return introspections

    def delete(self, introspection_id: int):
        self.introspection_dao.delete(introspection_id)
