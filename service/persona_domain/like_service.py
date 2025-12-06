from typing import List

from converter.like_converter import LikeConverter
from dao.like_dao import LikeDAO
from models.ai.input.like_input import LikeInput
from models.ai.output.like_ai import LikeAI
from models.like import Like
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService


class LikeService:
    def __init__(self,
                 ai_service: AIService,
                 backstory_service: BackstoryService,
                 like_converter: LikeConverter,
                 like_dao: LikeDAO):

        self.ai_service = ai_service
        self.backstory_service = backstory_service
        self.like_converter = like_converter
        self.like_dao = like_dao

    def generate(self, persona_id, universe_id: int) -> Like:
        backstory = self.backstory_service.find_by_persona_id(persona_id=persona_id)
        like_input = LikeInput(
            current_likes=[
                {"like":like.like_name,
                 "dislike":like.dislike_name}
                for like in backstory.likes],
            backstory=backstory,
        )
        generated_like: LikeAI = self.ai_service.call_llm("create_like",
                                        return_type=LikeAI,
                                        user_data=like_input,
                                        universe_id=universe_id,
                                        validator=self.create_validator(current_likes=backstory.likes))
        generated_like.like_name = generated_like.like_name.replace("_", " ")
        generated_like.dislike_name = generated_like.dislike_name.replace("_", " ")
        return self.like_converter.ai_to_model(generated_like, persona_id)

    def create_validator(self, current_likes):
        def validator(result: LikeAI):
            for like in current_likes:
                if like.like_name == result.like_name:
                    raise ValueError(f"The like {result.like_name} has already been used, choose another one that has not been used.")
                elif like.dislike_name == result.dislike_name:
                    raise ValueError(f"The dislike {result.dislike_name} matches an existing dislike, choose another one that does not match an existing dislike.")
                elif like.like_name == result.dislike_name:
                    raise ValueError(f"The like {result.like_name} matches the dislike {result.dislike_name}, they cannot like and dislike the same thing at the same time.")
                elif like.dislike_name == result.like_name:
                    raise ValueError(f"The dislike {result.dislike_name} matches the like {result.like_name}, they cannot like and dislike the same thing at the same time.")
        return validator

    def save(self, persona_id, like: Like):
        like_entity = self.like_converter.model_to_entity(like)
        like_entity.backstory_id = self.backstory_service.find_by_persona_id(persona_id).id
        like_entity = self.like_dao.save(like_entity)
        return self.like_converter.entity_to_model(like_entity)

    def find_by_persona_id(self, persona_id: int) -> List[Like]:
        backstory_id: int = self.backstory_service.find_by_persona_id(persona_id).id
        like_entities = self.like_dao.find_by_persona_id(backstory_id=backstory_id)
        return [self.like_converter.entity_to_model(like_entity) for like_entity in like_entities]

    def delete(self, like_id):
        self.like_dao.delete(like_id)
