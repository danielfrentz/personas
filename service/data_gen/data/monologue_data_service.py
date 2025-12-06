import logging
from typing import List

from models.conversation import Conversation
from service.persona_domain.monologue_service import MonologueService


class MonologueDataService:
    def __init__(self, monologue_service: MonologueService):
        self.monologue_service = monologue_service

    def generate(self, persona_id: int) -> List[Conversation]:
        result = []
        for monologue in self.monologue_service.find_by_speaker_id(persona_id):
            if monologue.conversation is not None:
                original_speaker = monologue.conversation.conversation_turns[0].speaker
                for i, conversation_turn in enumerate(monologue.conversation.conversation_turns):
                    if i == 0:
                        conversation_turn.speaker = "User"
                        conversation_turn.turn_intent = monologue.trigger_word
                    else:
                        if conversation_turn.directed_at == [original_speaker]:
                            conversation_turn.directed_at = [conversation_turn.speaker]
                        if i == len(monologue.conversation.conversation_turns) - 1:
                            conversation_turn.directed_at = ["User"]

                result.append(monologue.conversation)
        logging.info(f"returning {len(result)} monologues")
        return result