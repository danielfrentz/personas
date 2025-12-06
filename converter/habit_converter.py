from converter.conversation_converter import ConversationConverter
from entity.base import HabitEntity
from models.ai.output.habit_ai import HabitAI
from models.habit import Habit


class HabitConverter:
    def __init__(self, conversation_converter: ConversationConverter):
        self.conversation_converter = conversation_converter

    def model_to_entity(self, habit: Habit) -> HabitEntity:
        return HabitEntity(
            id=habit.id,
            backstory_id=habit.backstory_id,
            name=habit.name,
            frequency=habit.frequency,
            good_habit=habit.good_habit,
            description=habit.description,
        )

    def entity_to_model(self, habit_entity: HabitEntity) -> Habit:
        return Habit(
            id=habit_entity.id,
            name=habit_entity.name,
            frequency=habit_entity.frequency,
            backstory_id=habit_entity.backstory_id,
            description=habit_entity.description,
            good_habit=habit_entity.good_habit
        )

    def ai_to_model(self, habit: HabitAI, backstory_id: int) -> Habit:
        internal_monologue = self.conversation_converter.ai_to_model(habit.internal_monologue)
        return Habit(
            name=habit.habit_name.lower(),
            frequency=habit.frequency,
            backstory_id=backstory_id,
            internal_monologue=internal_monologue,
            good_habit=habit.good_habit,
            description=habit.description
        )