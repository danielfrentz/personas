from typing import List

from converter.backstory_converter import BackstoryConverter
from converter.habit_converter import HabitConverter
from dao.habit_dao import HabitDAO
from entity.base import HabitEntity
from models.ai.input.habits_input import HabitsInput
from models.ai.output.habit_ai import HabitAI
from models.backstory import Backstory
from models.habit import Habit
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.conversation_service import ConversationService
from service.persona_domain.persona_service import PersonaService


class HabitService:
    def __init__(self, ai_service: AIService,
                 backstory_converter: BackstoryConverter,
                 persona_service: PersonaService,
                 habit_converter: HabitConverter,
                 habit_dao: HabitDAO,
                 backstory_service: BackstoryService,
                 conversation_service: ConversationService):
        self.ai_service = ai_service
        self.backstory_converter = backstory_converter
        self.persona_service = persona_service
        self.habit_converter = habit_converter
        self.habit_dao = habit_dao
        self.conversation_service = conversation_service
        self.backstory_service = backstory_service

    def generate(self, universe_id, persona_id: int) -> Habit:
        backstory = self.backstory_service.find_by_persona_id(persona_id)
        habit_input = HabitsInput(
            backstory=backstory
        )
        generated_habit: HabitAI = self.ai_service.call_llm(system_prompt_name="create_habit", return_type=HabitAI, user_data=habit_input, universe_id=universe_id, validator=self.create_validation(habit_input, backstory=backstory))
        return self.habit_converter.ai_to_model(generated_habit, persona_id)

    def create_validation(self, habit_input: HabitsInput, backstory: Backstory):
        def validation(habit_ai: HabitAI):
            if habit_ai.habit_name.lower() in [habit.name.lower() for habit in backstory.habits]:
                raise ValueError(f"Habit must be unique, but has the same name as {habit_ai.habit_name}")
            for conversation_turn in habit_ai.internal_monologue.conversation_turns:
                if conversation_turn.speaker.lower() != backstory.name:
                    raise ValueError("The speaker must be the same as the persona backstory as it is an internal monologue.")
        return validation


    def save(self, persona_id: int, habit: Habit) -> Habit:
        backstory_id = self.persona_service.find_by_id(persona_id).backstory.id
        habit_entity = self.habit_converter.model_to_entity(habit)
        habit_entity.backstory_id = backstory_id
        habit_entity = self.habit_dao.save(habit_entity)
        habit_conversation = self.conversation_service.save(habit.internal_monologue, source_id=habit_entity.id, source_name=Habit.__name__)
        habit_model = self.habit_converter.entity_to_model(habit_entity)
        habit_model.internal_monologue = habit_conversation
        return habit_model

    def find_by_persona_id(self, persona_id: int) -> List[Habit]:
        backstory_id = self.persona_service.find_by_id(persona_id).backstory.id
        habit_entities: List[HabitEntity] = self.habit_dao.find_by_persona(backstory_id=backstory_id)
        result: List[Habit] = []
        for habit_entity in habit_entities:
            habit_conversation = self.conversation_service.find_by_source_id(source_id=habit_entity.id, source=Habit.__name__)
            habit = self.habit_converter.entity_to_model(habit_entity)
            habit.internal_monologue = habit_conversation
            result.append(habit)
        return result

    def delete_by_id(self, habit_id: int):
        self.habit_dao.delete(habit_id)