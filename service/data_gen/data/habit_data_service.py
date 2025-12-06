import logging
from typing import List

from models.conversation import Conversation
from models.habit import Habit
from service.persona_domain.habit_service import HabitService
from service.persona_domain.persona_service import PersonaService


class HabitDataService:
    def __init__(self, habit_service: HabitService, persona_service: PersonaService):
        self.habit_service = habit_service
        self.persona_service = persona_service

    def generate(self, persona_id: int) -> List[Conversation]:
        persona = self.persona_service.find_by_id(persona_id)
        result: List[Conversation] = [habit.internal_monologue for habit in self.habit_service.find_by_persona_id(persona_id)]
        for habit in result:
            for turn in habit.conversation_turns:
                turn.speaker = persona.backstory.name
                turn.directed_at = [persona.backstory.name]
        logging.info(f"returning {len(result)} habits")
        return result