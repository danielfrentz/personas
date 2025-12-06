import logging
from typing import List

from models.conversation import Conversation
from models.conversation_turn import ConversationTurn
from service.persona_domain.like_service import LikeService
from service.persona_domain.persona_service import PersonaService


class LikeDataService:
    conversation_text_like = "One of the things I like is {like} because {reason}."
    conversation_text_not_like = "But I also dislike {dislike} because {reason}."


    def __init__(self, like_service: LikeService, persona_service: PersonaService):
        self.like_service = like_service
        self.persona_service = persona_service

    def generate(self, persona_id: int) -> List[Conversation]:
        result: List[Conversation] = []
        persona = self.persona_service.find_by_id(persona_id)
        for like in persona.backstory.likes:
            like_turn = ConversationTurn(
                speaker=persona.backstory.name,
                action="Reminding myself of what I like",
                turn_intent="Establish why I like something",
                text=LikeDataService.conversation_text_like.format(like=like.like_name, reason=like.like_reason),
                tone="Pensive",
                directed_at=[persona.backstory.name],
                feeling="contentment"
            )
            dislike_turn = ConversationTurn(
                speaker=persona.backstory.name,
                action="Explaining something I dislike",
                turn_intent="Establish why I dislike something",
                text=LikeDataService.conversation_text_not_like.format(dislike=like.dislike_name, reason=like.dislike_reason),
                tone="Reflective",
                directed_at=[persona.backstory.name],
                feeling="sad"
            )
            contradiction_turn = ConversationTurn(
                speaker=persona.backstory.name,
                action="Resolving self contradiction",
                turn_intent="determine the contradiction",
                text=like.contradiction,
                tone="Contemplative",
                directed_at=[persona.backstory.name],
                feeling="confused"
            )
            contradiction_resolution_turn = ConversationTurn(
                speaker=persona.backstory.name,
                action="Resolving self contradiction",
                turn_intent="resolve the contradiction",
                text=like.contradiction_explanation,
                tone="Confident",
                directed_at=[persona.backstory.name],
                feeling="cognitive closure"
            )
            result.append(Conversation(conversation_turns=[like_turn, dislike_turn, contradiction_turn, contradiction_resolution_turn]))
        logging.info(f"returning {len(result)} likes")
        return result

