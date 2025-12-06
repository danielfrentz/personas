import logging
from typing import List

from models.conversation import Conversation
from models.conversation_turn import ConversationTurn
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.speech_sample_service import SpeechSampleService


class SpeechDataService:
    def __init__(self, persona_service: PersonaService, speech_sample_service: SpeechSampleService):
        self.persona_service = persona_service
        self.speech_sample_service = speech_sample_service


    def generate(self, persona_id: int) -> List[Conversation]:
        result: List[Conversation] = []
        persona = self.persona_service.find_by_id(persona_id)
        for sample in persona.speech_profile.samples:
            turn = ConversationTurn(
                speaker=persona.backstory.name,
                directed_at=["everyone"],
                tone=sample.tone,
                text=sample.explanation,
                private_thought="I want everyone to know why I speak like this in similar situations.",
                action="Telling everyone about the way in which I speak in different contexts.",
                feeling=sample.feeling
            )
            result.append(Conversation(conversation_turns=[turn]))
        logging.info(f"returning {len(result)} speech samples")
        return result