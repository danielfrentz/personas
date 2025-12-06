from typing import Optional

from converter.habit_converter import HabitConverter
from converter.hobby_converter import HobbyConverter
from converter.like_converter import LikeConverter
from converter.persona_aspect_converter import PersonaAspectConverter
from entity.base import BackstoryEntity
from models.ai.output.backstory_ai import BackstoryAI
from models.backstory import Backstory


class BackstoryConverter:
    def __init__(self, like_converter: LikeConverter,
                 habit_converter: HabitConverter,
                 hobby_converter: HobbyConverter,
                 aspect_converter: PersonaAspectConverter):
        self.like_converter = like_converter
        self.habit_converter = habit_converter
        self.like_converter = like_converter
        self.hobby_converter = hobby_converter
        self.aspect_converter = aspect_converter
        

    def model_to_entity(self, backstory: Backstory, persona_id: int) -> BackstoryEntity | None:
        if backstory is None:
            return None
        likes = [self.like_converter.model_to_entity(like_entity) for like_entity in backstory.likes]
        aspects = [self.aspect_converter.model_to_entity(aspect_entity) for aspect_entity in backstory.aspects]
        result = BackstoryEntity(
            id=backstory.id,
            gender=backstory.gender,
            name=backstory.name.lower(),
            persona_id=persona_id,
            place_of_birth=backstory.place_of_birth.lower(),
            date_of_birth=backstory.date_of_birth,
            description=backstory.description,
            social_description=backstory.social_description,
            education_description=backstory.education_description,
            historical=backstory.historical,

        )
        result.aspects = aspects
        result.likes = likes
        return result

    def entity_to_model(self, backstory_entity: BackstoryEntity) -> Optional[Backstory]:
        if backstory_entity is None:
            return None
        likes = [self.like_converter.entity_to_model(like_entity) for like_entity in backstory_entity.likes]
        habits = [self.habit_converter.entity_to_model(habit) for habit in backstory_entity.habits]
        hobbies = [self.hobby_converter.entity_to_model(hobby) for hobby in backstory_entity.hobbies]
        aspects = [self.aspect_converter.entity_to_model(aspect) for aspect in backstory_entity.aspects]
        return Backstory(
            id=backstory_entity.id,
            gender=backstory_entity.gender,
            persona_id=backstory_entity.persona_id,
            name=backstory_entity.name.lower(),
            place_of_birth=backstory_entity.place_of_birth,
            date_of_birth=backstory_entity.date_of_birth,
            description=backstory_entity.description,
            social_description=backstory_entity.social_description,
            education_description=backstory_entity.education_description,
            likes=likes,
            habits=habits,
            hobbies=hobbies,
            historical=backstory_entity.historical,
            aspects=aspects
        )

    def ai_to_model(self, backstory_ai: BackstoryAI, name: str, historical: bool) -> Backstory:
        habits = []
        return Backstory(
            gender=backstory_ai.gender,
            place_of_birth=backstory_ai.place_of_birth,
            date_of_birth=backstory_ai.date_of_birth,
            description=backstory_ai.indepth_general_description,
            social_description=backstory_ai.social_description,
            education_description=backstory_ai.education_description,
            habits=habits,
            name=name.lower(),
            historical=historical
        )