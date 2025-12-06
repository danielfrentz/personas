from typing import List

from converter.self_description_conversation_converter import SelfDescriptionConversationConverter
from dao.self_description_conversation_dao import SelfDescriptionConversationDao
from models.ai.input.self_description_conversation_input import SelfDescriptionConversationInput
from models.ai.output.self_description_conversation import SelfDescriptionConversation
from models.ai.output.self_description_conversation_ai import SelfDescriptionConversationAI
from models.http.request.generate.self_description_conversation_request import SelfDescriptionConversationRequest
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.conversation_service import ConversationService
from service.persona_domain.persona_aspect_service import PersonaAspectService
from service.persona_domain.persona_service import PersonaService


class SelfDescriptionConversationService:
    def __init__(self,
                 ai_service: AIService,
                 conversation_service: ConversationService,
                 self_description_conversation_converter: SelfDescriptionConversationConverter,
                 backstory_service: BackstoryService,
                 self_description_conversation_dao: SelfDescriptionConversationDao,
                 persona_service: PersonaService,
                 aspect_service: PersonaAspectService
                 ):
        self.ai_service = ai_service
        self.conversation_service = conversation_service
        self.self_description_conversation_converter = self_description_conversation_converter
        self.backstory_service = backstory_service
        self.self_description_conversation_dao = self_description_conversation_dao
        self.persona_service = persona_service
        self.aspect_service = aspect_service

    def generate(self, universe_id: int, self_description_conversation_request: SelfDescriptionConversationRequest):
        persona_backstory = self.backstory_service.find_by_persona_id(self_description_conversation_request.persona_id)
        persona = self.persona_service.find_by_id(persona_id=self_description_conversation_request.persona_id)
        prompter_backstory = self.backstory_service.find_by_persona_id(self_description_conversation_request.prompter_id)
        aspects = self.aspect_service.find_by_persona(persona_id=persona.id)
        self_description_conversation_input = SelfDescriptionConversationInput(
            persona_id=self_description_conversation_request.persona_id,
            backstory=persona_backstory,
            prompter_backstory=prompter_backstory,
            speech_profile=persona.speech_profile,
            topic=self_description_conversation_request.topic,
            aspects=aspects,
            minimum_turns=10
        )
        generated_conversation = self.ai_service.call_llm(user_data=self_description_conversation_input, system_prompt_name="create_self_description", return_type=SelfDescriptionConversationAI, universe_id=universe_id, validator=self.validate(self_description_conversation_input))
        return self.self_description_conversation_converter.ai_to_model(generated_conversation, persona_id=self_description_conversation_request.persona_id, prompter_id=self_description_conversation_request.prompter_id, topic=self_description_conversation_request.topic)

    def validate(self, self_description_input: SelfDescriptionConversationInput):
        def validation(conversation: SelfDescriptionConversationAI):

            if len(conversation.conversation.conversation_turns) + 2 < self_description_input.minimum_turns:
                raise ValueError(f"Conversation must have at least {self_description_input.minimum_turns} turn but had {len(conversation.conversation.conversation_turns)} turns")
            for turn in conversation.conversation.conversation_turns:
                if turn.speaker.lower() != self_description_input.backstory.name.lower():
                    raise ValueError("Conversation must start with a prompt from the prompter")
                if turn.directed_at != [self_description_input.prompter_backstory.name]:
                    raise ValueError("Conversation must start with a prompt from the prompter")
        return validation

    def save(self, self_description_conversation: SelfDescriptionConversation) -> SelfDescriptionConversation:
        self_description_conversation_entity = self.self_description_conversation_converter.model_to_entity(self_description_conversation)
        self_description_conversation_entity = self.self_description_conversation_dao.save(self_description_conversation_entity)
        conversation = self.conversation_service.save(self_description_conversation.conversation, source_name=SelfDescriptionConversation.__name__, source_id=self_description_conversation_entity.id)
        result = self.self_description_conversation_converter.entity_to_model(self_description_conversation_entity)
        result.conversation = conversation
        return result


    def find_by_persona_id(self, persona_id) -> List[SelfDescriptionConversation]:
        result = []
        self_descriptions = [self.self_description_conversation_converter.entity_to_model(self_description) for self_description in self.self_description_conversation_dao.find_by_persona_id(persona_id)]
        for self_description in self_descriptions:
            conversation = self.conversation_service.find_by_source_id(source_id=self_description.id, source=SelfDescriptionConversation.__name__)
            self_description.conversation = conversation
            result.append(self_description)
        return result
