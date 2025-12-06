from typing import Generator

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from config.settings import Settings
from converter.accessory_converter import AccessoryConverter
from converter.backstory_converter import BackstoryConverter
from converter.clothing_converter import ClothingConverter
from converter.conversation_converter import ConversationConverter
from converter.conversation_turn_converter import ConversationTurnConverter
from converter.group_reasoning_converter import GroupReasoningConverter
from converter.habit_converter import HabitConverter
from converter.hair_style_converter import HairStyleConverter
from converter.hobby_converter import HobbyConverter
from converter.interesting_physical_description_note_converter import InterestingPhysicalDescriptionNoteConverter
from converter.introspection_converter import IntrospectionConverter
from converter.life_event_converter import LifeEventConverter
from converter.like_converter import LikeConverter
from converter.memory_converter import MemoryConverter
from converter.monologue_converter import MonologueConverter
from converter.persona_aspect_converter import PersonaAspectConverter
from converter.persona_converter import PersonaConverter
from converter.persona_fact_converter import PersonaFactConverter
from converter.persona_knowledge_converter import PersonaKnowledgeConverter
from converter.persona_skill_converter import PersonaSkillConverter
from converter.physical_description_converter import PhysicalDescriptionConverter
from converter.prompt_performance_converter import PromptPerformanceConverter
from converter.reasoning_conversation_converter import ReasoningConversationConverter
from converter.relationship_converter import RelationshipConverter
from converter.relationship_feeling_converter import RelationshipFeelingConverter
from converter.relationship_thought_converter import RelationshipThoughtConverter
from converter.self_description_conversation_converter import SelfDescriptionConversationConverter
from converter.speech_profile_converter import SpeechProfileConverter
from converter.speech_sample_converter import SpeechSampleConverter
from converter.story_converter import StoryConverter
from converter.story_disagreement_converter import StoryDisagreementConverter
from converter.story_interesting_note_converter import StoryInterestingNoteConverter
from converter.universe_converter import UniverseConverter
from converter.universe_description_converter import UniverseDescriptionConverter
from converter.universe_location_converter import UniverseLocationConverter
from converter.universe_metadata_converter import UniverseMetadataConverter
from dao.accessory_dao import AccessoryDAO
from dao.backstory_dao import BackstoryDAO
from dao.clothing_dao import ClothingDAO
from dao.conversation_dao import ConversationDAO
from dao.group_reasoning_style_dao import GroupReasoningStyleDAO
from dao.habit_dao import HabitDAO
from dao.hairstyle_dao import HairStyleDAO
from dao.hobby_dao import HobbyDAO
from dao.introspection_dao import IntrospectionDAO
from dao.life_event_dao import LifeEventDAO
from dao.like_dao import LikeDAO
from dao.memory_dao import MemoryDAO
from dao.monologue_dao import MonologueDAO
from dao.persona_aspect_dao import PersonaAspectDao
from dao.persona_dao import PersonaDAO
from dao.persona_fact_dao import PersonaFactDAO
from dao.persona_knowledge_dao import PersonaKnowledgeDAO
from dao.persona_skill_dao import PersonaSkillDAO
from dao.physical_description_dao import PhysicalDescriptionDAO
from dao.prompt_performance_dao import PromptPerformanceDAO
from dao.reasoning_conversation_dao import ReasoningConversationDAO
from dao.relationship_dao import RelationshipDAO
from dao.self_description_conversation_dao import SelfDescriptionConversationDao
from dao.speech_profile_dao import SpeechProfileDAO
from dao.speech_sample_dao import SpeechSampleDAO
from dao.story_dao import StoryDAO
from dao.universe_dao import UniverseDAO
from dao.universe_description_dao import UniverseDescriptionDAO
from dao.universe_location_dao import UniverseLocationDAO
from dao.universe_metadata_dao import UniverseMetadataDAO
from entity.base import SessionLocal
from service.ai.ai_service import AIService
from service.ai.prompt_service import PromptService
from service.analytics.prompt_performance_service import PromptPerformanceService
from service.data_gen.base.base_data_service import BaseDataService
from service.data_gen.base.story_data_service import StoryDataService
from service.data_gen.data.conversation_data_service import ConversationDataService
from service.data_gen.data.fact_data_service import FactDataService
from service.data_gen.data.habit_data_service import HabitDataService
from service.data_gen.data.hobby_data_service import HobbyDataService
from service.data_gen.data.introspection_data_service import IntrospectionDataService
from service.data_gen.data.like_data_service import LikeDataService
from service.data_gen.data.memory_data_service import MemoryDataService
from service.data_gen.data.monologue_data_service import MonologueDataService
from service.data_gen.data.reasoning_style_data_service import ReasoningStyleDataService
from service.data_gen.data.relationship_data_service import RelationshipDataService
from service.data_gen.data.self_description_data_service import SelfDescriptionDataService
from service.data_gen.data.speech_data_service import SpeechDataService
from service.data_gen.data_generation_service import DataGenerationService
from service.persona_domain.accessory_service import AccessoryService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.clothing_service import ClothingService
from service.persona_domain.conversation_service import ConversationService
from service.persona_domain.extended_monologue_service import ExtendedMonologueService
from service.persona_domain.group_reasoning_profile_service import GroupReasoningProfileService
from service.persona_domain.habit_service import HabitService
from service.persona_domain.hair_style_service import HairStyleService
from service.persona_domain.hobby_service import HobbyService
from service.persona_domain.introspection_service import IntrospectionService
from service.persona_domain.life_event_service import LifeEventService
from service.persona_domain.like_service import LikeService
from service.persona_domain.memory_service import MemoryService
from service.persona_domain.monologue_service import MonologueService
from service.persona_domain.persona_aspect_service import PersonaAspectService
from service.persona_domain.persona_fact_service import PersonaFactService
from service.persona_domain.persona_knowledge_service import PersonaKnowledgeService
from service.persona_domain.persona_objective_description_service import PersonaObjectiveDescriptionService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.persona_skill_service import PersonaSkillService
from service.persona_domain.physical_description_service import PhysicalDescriptionService
from service.persona_domain.reasoning_conversation_service import ReasoningConversationService
from service.persona_domain.relationship_service import RelationshipService
from service.persona_domain.self_description_conversation_service import SelfDescriptionConversationService
from service.persona_domain.speech_profile_service import SpeechProfileService
from service.persona_domain.speech_sample_service import SpeechSampleService
from service.persona_domain.story_conversation_service import StoryConversationService
from service.persona_domain.story_service import StoryService
from service.persona_domain.team_service import TeamService
from service.persona_domain.universe_description_service import UniverseDescriptionService
from service.persona_domain.universe_location_service import UniverseLocationService
from service.persona_domain.universe_metadata_service import UniverseMetadataService
from service.persona_domain.universe_service import UniverseService

init_model = None
init_tokenizer = None



def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_settings():
    return Settings()

def get_conversation_turn_converter() -> ConversationTurnConverter:
    return ConversationTurnConverter()


def get_persona_skill_dao(db: Session = Depends(get_db)) -> PersonaSkillDAO:
    return PersonaSkillDAO(db=db)

def get_persona_knowledge_dao(db: Session = Depends(get_db)) -> PersonaKnowledgeDAO:
    return PersonaKnowledgeDAO(db=db)

def get_persona_skill_converter():
    return PersonaSkillConverter()

def get_persona_knowledge_converter():
    return PersonaKnowledgeConverter()

def get_conversation_converter(
        conversation_turn_converter: ConversationTurnConverter = Depends(get_conversation_turn_converter)):
    return ConversationConverter(conversation_turn_converter=conversation_turn_converter)


def get_relationship_thought_converter():
    return RelationshipThoughtConverter()


def get_relationship_feeling_converter():
    return RelationshipFeelingConverter()


def get_relationship_dao(db: Session = Depends(get_db)):
    return RelationshipDAO(db=db)


def get_relationship_converter(
        relationship_feeling_converter: RelationshipFeelingConverter = Depends(get_relationship_feeling_converter),
        relationship_thought_converter: RelationshipThoughtConverter = Depends(get_relationship_thought_converter)):
    return RelationshipConverter(relationship_feeling_converter=relationship_feeling_converter,
                                 relationship_thought_converter=relationship_thought_converter)


def get_model():
    return init_model


def get_tokenizer():
    return init_tokenizer


def get_persona_dao(db=Depends(get_db)) -> PersonaDAO:
    return PersonaDAO(db=db)


def get_hair_style_converter() -> HairStyleConverter:
    return HairStyleConverter()


def get_memory_converter():
    return MemoryConverter()


def get_physical_description_interesting_note_converter() -> InterestingPhysicalDescriptionNoteConverter:
    return InterestingPhysicalDescriptionNoteConverter()


def get_clothing_converter():
    return ClothingConverter()


def get_accessory_converter():
    return AccessoryConverter()


def get_interesting_backstory_note_converter():
    return StoryInterestingNoteConverter()

def get_story_disagreement_converter():
    return StoryDisagreementConverter


def get_story_interesting_note_converter():
    return StoryInterestingNoteConverter()

def get_speech_sample_converter() -> SpeechSampleConverter:
    return SpeechSampleConverter()


def get_speech_profile_converter(speech_sample_converter: SpeechSampleConverter = Depends(
    get_speech_sample_converter)) -> SpeechProfileConverter:
    return SpeechProfileConverter(speech_sample_converter=speech_sample_converter)


def get_hobby_converter() -> HobbyConverter:
    return HobbyConverter()

def get_physical_description_converter(clothing_converter: ClothingConverter = Depends(get_clothing_converter),
                                       interesting_physical_note_converter: InterestingPhysicalDescriptionNoteConverter = Depends(
                                           get_physical_description_interesting_note_converter),
                                       accessory_converter: AccessoryConverter = Depends(get_accessory_converter),
                                       hairstyle_converter: HairStyleConverter = Depends(
                                           get_hair_style_converter)) -> PhysicalDescriptionConverter:
    return PhysicalDescriptionConverter(accessory_converter=accessory_converter,
                                        clothing_converter=clothing_converter,
                                        interesting_notes_converter=interesting_physical_note_converter,
                                        hairstyle_converter=hairstyle_converter
                                        )


def get_physical_description_dao(db=Depends(get_db)) -> PhysicalDescriptionDAO:
    return PhysicalDescriptionDAO(db=db)


def get_like_dao(db: Session = Depends(get_db)):
    return LikeDAO(db=db)


def get_like_converter():
    return LikeConverter()


def get_group_reasoning_converter():
    return GroupReasoningConverter()


def get_habit_converter(conversation_converter: ConversationConverter = Depends(get_conversation_converter)):
    return HabitConverter(conversation_converter=conversation_converter)
def get_persona_aspect_converter() -> PersonaAspectConverter:
    return PersonaAspectConverter()

def get_backstory_converter(like_converter: LikeConverter = Depends(get_like_converter),
                            habit_converter: HabitConverter=Depends(get_habit_converter),
                            hobby_converter:HobbyConverter=Depends(get_hobby_converter),
                            aspect_converter: PersonaAspectConverter = Depends(get_persona_aspect_converter)) -> BackstoryConverter:
    return BackstoryConverter(like_converter=like_converter,
                              habit_converter=habit_converter,
                              hobby_converter=hobby_converter,
                              aspect_converter=aspect_converter)



def get_universe_dao(db: Session = Depends(get_db)) -> UniverseDAO:
    return UniverseDAO(db=db)


def get_universe_location_converter() -> UniverseLocationConverter:
    return UniverseLocationConverter()


def get_universe_description_converter(universe_location_converter: UniverseLocationConverter = Depends(
    get_universe_location_converter)) -> UniverseDescriptionConverter:
    return UniverseDescriptionConverter(universe_location_converter=universe_location_converter)


def get_universe_metadata_converter() -> UniverseMetadataConverter:
    return UniverseMetadataConverter()


def get_introspection_converter(conversation_converter: ConversationConverter = Depends(get_conversation_converter),
                                conversation_turn_converter: ConversationTurnConverter = Depends(
                                    get_conversation_turn_converter)):
    return IntrospectionConverter(conversation_converter=conversation_converter,
                                  conversation_turn_converter=conversation_turn_converter)


def get_story_converter(
        story_disagreement_converter: StoryDisagreementConverter = Depends(get_story_disagreement_converter),
        story_interesting_note_converter: StoryInterestingNoteConverter = Depends(get_story_interesting_note_converter),
        memory_converter: MemoryConverter = Depends(get_memory_converter),
        introspection_converter: IntrospectionConverter = Depends(get_introspection_converter)) -> StoryConverter:
    return StoryConverter(story_disagreement_converter=story_disagreement_converter,
                          story_interesting_note_converter=story_interesting_note_converter,
                          memory_converter=memory_converter,
                          introspection_converter=introspection_converter)


def get_life_event_converter(story_converter: StoryConverter = Depends(get_story_converter)) -> LifeEventConverter:
    return LifeEventConverter(story_converter=story_converter)

def get_persona_converter(backstory_converter=Depends(get_backstory_converter),
                          physical_description_converter=Depends(get_physical_description_converter),
                          life_event_converter: LifeEventConverter = Depends(get_life_event_converter),
                          speech_profile_converter: SpeechProfileConverter = Depends(get_speech_profile_converter),
                          relationship_converter: RelationshipConverter = Depends(get_relationship_converter),
                          group_reasoning_converter: GroupReasoningConverter = Depends(get_group_reasoning_converter),
                          persona_skill_converter: PersonaSkillConverter = Depends(get_persona_skill_converter),
                          knowledge_converter: PersonaKnowledgeConverter = Depends(get_persona_knowledge_converter))\
        -> PersonaConverter:
    return PersonaConverter(backstory_converter=backstory_converter,
                            physical_description_converter=physical_description_converter,
                            life_event_converter=life_event_converter,
                            speech_profile_converter=speech_profile_converter,
                            relationship_converter=relationship_converter,
                            group_reasoning_converter=group_reasoning_converter,
                            persona_skill_converter=persona_skill_converter,
                            persona_knowledge_converter=knowledge_converter,)


def get_persona_service(persona_dao: PersonaDAO = Depends(get_persona_dao),
                        persona_converter: PersonaConverter = Depends(get_persona_converter)):
    return PersonaService(persona_dao, persona_converter)

def get_universe_converter(key_location_converter: UniverseLocationConverter = Depends(get_universe_location_converter),
                           universe_metadata_converter: UniverseMetadataConverter = Depends(
                               get_universe_metadata_converter),
                           universe_description_converter: UniverseDescriptionConverter = Depends(
                               get_universe_description_converter),
                           persona_converter: PersonaConverter = Depends(get_persona_converter),
                           universe_location_converter: UniverseLocationConverter = Depends(
                               get_universe_location_converter),
                           ) -> UniverseConverter:
    return UniverseConverter(key_location_converter=key_location_converter,
                             universe_metadata_converter=universe_metadata_converter,
                             universe_description_converter=universe_description_converter,
                             persona_converter=persona_converter,
                             universe_location_converter=universe_location_converter)


def get_universe_metadata_dao(db: Session = Depends(get_db)) -> UniverseMetadataDAO:
    return UniverseMetadataDAO(db=db)


def get_universe_metadata_service(metadata_dao: UniverseMetadataDAO = Depends(get_universe_metadata_dao),
                                  metadata_converter: UniverseMetadataConverter = Depends(
                                      get_universe_metadata_converter)):
    return UniverseMetadataService(universe_metadata_dao=metadata_dao,
                                   metadata_converter=metadata_converter)


def get_prompt_service(
        universe_metadata_service: UniverseMetadataService = Depends(get_universe_metadata_service)) -> PromptService:
    return PromptService(universe_metadata_service=universe_metadata_service)


def get_prompt_performance_dao(db: Session = Depends(get_db)) -> PromptPerformanceDAO:
    return PromptPerformanceDAO(db=db)

def get_prompt_performance_converter():
    return PromptPerformanceConverter()

def get_prompt_performance_service(prompt_performance_dao: PromptPerformanceDAO = Depends(get_prompt_performance_dao),
                                   prompt_performance_converter: PromptPerformanceConverter = Depends(
                                      get_prompt_performance_converter)):
    return PromptPerformanceService(prompt_performance_dao=prompt_performance_dao,
                                      prompt_performance_converter=prompt_performance_converter)

def get_ai_service(prompt_service: PromptService = Depends(get_prompt_service),
                   model=Depends(get_model),
                   tokenizer=Depends(get_tokenizer),
                   prompt_performance_service: PromptPerformanceService = Depends(get_prompt_performance_service),
                   settings: Settings = Depends(get_settings),):
    return AIService(prompts_service=prompt_service,
                     model=model,
                     tokenizer=tokenizer,
                     prompt_performance_service=prompt_performance_service,
                     settings=settings)


def get_hair_style_dao(db: Session = Depends(get_db)) -> HairStyleDAO:
    return HairStyleDAO(db_session=db)


def get_universe_service(universe_dao: UniverseDAO = Depends(get_universe_dao),
                         ai_service: AIService = Depends(get_ai_service),
                         universe_converter: UniverseConverter = Depends(get_universe_converter),
                         universe_metadata_converter: UniverseMetadataConverter = Depends(
                             get_universe_metadata_converter)) -> UniverseService:
    return UniverseService(universe_dao=universe_dao, ai_service=ai_service, universe_converter=universe_converter,
                           universe_metadata_converter=universe_metadata_converter)


def get_universe_description_dao(db: Session = Depends(get_db)) -> UniverseDescriptionDAO:
    return UniverseDescriptionDAO(db=db)


def get_universe_description_service(universe_description_dao=Depends(get_universe_description_dao),
                                     universe_description_converter=Depends(get_universe_description_converter)):
    return UniverseDescriptionService(universe_description_dao=universe_description_dao,
                                      universe_description_converter=universe_description_converter)


def get_physical_description_service(ai_service=Depends(get_ai_service),
                                     persona_service: PersonaService = Depends(get_persona_service),
                                     physical_description_converter=Depends(get_physical_description_converter),
                                     physical_description_dao=Depends(get_physical_description_dao),
                                     universe_description_service=Depends(
                                         get_universe_description_service)) -> PhysicalDescriptionService:
    return PhysicalDescriptionService(ai_service=ai_service,
                                      persona_service=persona_service,
                                      physical_description_converter=physical_description_converter,
                                      physical_description_dao=physical_description_dao,
                                      universe_description_service=universe_description_service)


def get_backstory_dao(db=Depends(get_db)) -> BackstoryDAO:
    return BackstoryDAO(db=db)


def get_universe_dao(db=Depends(get_db)) -> UniverseDAO:
    return UniverseDAO(db=db)


def get_life_event_dao(db=Depends(get_db)) -> LifeEventDAO:
    return LifeEventDAO(db=db)


def get_speech_profile_dao(db: Session = Depends(get_db)) -> SpeechProfileDAO:
    return SpeechProfileDAO(db=db)


def get_backstory_service(backstory_dao: BackstoryDAO = Depends(get_backstory_dao),
                          ai_service: AIService = Depends(get_ai_service),
                          backstory_converter: BackstoryConverter = Depends(get_backstory_converter),
                          universe_description_service: UniverseDescriptionService = Depends(
                              get_universe_description_service),
                          persona_service=Depends(get_persona_service)) -> BackstoryService:
    return BackstoryService(backstory_dao=backstory_dao,
                            ai_service=ai_service,
                            backstory_converter=backstory_converter,
                            universe_description_service=universe_description_service,
                            persona_service=persona_service)


def get_hair_style_service(ai_service: AIService = Depends(get_ai_service),
                           hair_style_dao: HairStyleDAO = Depends(get_hair_style_dao),
                           hair_style_converter: HairStyleConverter = Depends(get_hair_style_converter),
                           backstory_service: BackstoryService = Depends(get_backstory_service)) -> HairStyleService:
    return HairStyleService(ai_service=ai_service,
                            hair_style_dao=hair_style_dao,
                            hairstyle_converter=hair_style_converter,
                            backstory_service=backstory_service,
                            )


def get_speech_profile_service(ai_service: AIService = Depends(get_ai_service),
                               speech_dao: SpeechProfileDAO = Depends(get_speech_profile_dao),
                               speech_converter: SpeechProfileConverter = Depends(get_speech_profile_converter),
                               persona_service: PersonaService = Depends(get_persona_service)) -> SpeechProfileService:
    return SpeechProfileService(ai_service=ai_service,
                                speech_dao=speech_dao,
                                speech_profile_converter=speech_converter,
                                persona_service=persona_service)


def get_life_events_service(
        ai_service: AIService = Depends(get_ai_service),
        life_event_converter: LifeEventConverter = Depends(get_life_event_converter),
        life_event_dao: LifeEventDAO = Depends(get_life_event_dao),
        persona_service: PersonaService = Depends(get_persona_service),
        backstory_converter: BackstoryConverter = Depends(get_backstory_converter),
) -> LifeEventService:
    return LifeEventService(
        ai_service=ai_service,
        life_event_converter=life_event_converter,
        life_event_dao=life_event_dao,
        persona_service=persona_service,
        backstory_converter=backstory_converter,
    )


def get_like_service(like_dao: LikeDAO = Depends(get_like_dao),
                     like_converter: LikeConverter = Depends(get_like_converter),
                     ai_service: AIService = Depends(get_ai_service),
                     backstory_service: BackstoryService = Depends(get_backstory_service), ) -> LikeService:
    return LikeService(ai_service=ai_service, like_converter=like_converter, backstory_service=backstory_service,
                       like_dao=like_dao)


def get_story_disagreement_converter():
    return StoryDisagreementConverter()


def get_story_dao(db: Session = Depends(get_db)) -> StoryDAO:
    return StoryDAO(db=db)


def get_story_converter(story_disagreement_converter=Depends(get_story_disagreement_converter),
                        story_interesting_note_converter=Depends(get_story_interesting_note_converter),
                        memory_converter: MemoryConverter = Depends(get_memory_converter),
                        introspection_converter: IntrospectionConverter = Depends(get_introspection_converter)) -> StoryConverter:
    return StoryConverter(story_disagreement_converter=story_disagreement_converter,
                          story_interesting_note_converter=story_interesting_note_converter,
                          memory_converter=memory_converter,
                          introspection_converter=introspection_converter)


def get_story_service(story_dao: StoryDAO = Depends(get_story_dao),
                      persona_service: PersonaService = Depends(get_persona_service),
                      story_converter: StoryConverter = Depends(get_story_converter),
                      ai_service: AIService = Depends(get_ai_service),
                      universe_description_service: UniverseDescriptionService = Depends(
                          get_universe_description_service),
                      life_event_service: LifeEventService = Depends(get_life_events_service),
                      backstory_converter: BackstoryConverter = Depends(get_backstory_converter),
                      ) -> StoryService:
    return StoryService(
        story_dao=story_dao,
        persona_service=persona_service,
        story_converter=story_converter,
        ai_service=ai_service,
        universe_description_service=universe_description_service,
        life_event_service=life_event_service,
        backstory_converter=backstory_converter,
    )


def get_conversation_dao(db: Session = Depends(get_db)):
    return ConversationDAO(
        db=db,
    )


def get_conversation_service(conversation_dao: ConversationDAO = Depends(get_conversation_dao),
                             conversation_converter: ConversationConverter = Depends(
                                 get_conversation_converter)) -> ConversationService:
    return ConversationService(conversation_dao=conversation_dao,
                               conversation_converter=conversation_converter, )


def get_story_conversation_service(
        ai_service: AIService = Depends(get_ai_service),
        conversation_converter: ConversationConverter = Depends(get_conversation_converter),
        conversation_dao: ConversationDAO = Depends(get_conversation_dao),
        persona_service: PersonaService = Depends(get_persona_service),
        universe_service: UniverseService = Depends(get_universe_service),
        story_service: StoryService = Depends(get_story_service),
        background_converter: BackstoryConverter = Depends(get_backstory_converter),
):
    return StoryConversationService(ai_service=ai_service,
                                    conversation_converter=conversation_converter,
                                    conversation_dao=conversation_dao,
                                    persona_service=persona_service,
                                    universe_service=universe_service,
                                    story_service=story_service,
                                    backstory_converter=background_converter, )


def get_memory_dao(db: Session = Depends(get_db)):
    return MemoryDAO(db=db)


def get_universe_location_dao(db: Session = Depends(get_db)):
    return UniverseLocationDAO(db=db)


def get_universe_location_service(universe_location_dao: UniverseLocationDAO = Depends(get_universe_location_dao),
                                  universe_location_converter: UniverseLocationConverter = Depends(
                                      get_universe_location_converter),
                                  ai_service: AIService = Depends(get_ai_service),
                                  universe_description_service: UniverseDescriptionService = Depends(
                                      get_universe_description_service),
                                  universe_description_converter: UniverseDescriptionConverter = Depends(
                                      get_universe_description_converter)) -> UniverseLocationService:
    return UniverseLocationService(universe_location_dao=universe_location_dao,
                                   universe_location_converter=universe_location_converter,
                                   ai_service=ai_service,
                                   universe_description_service=universe_description_service,
                                   universe_description_converter=universe_description_converter)


def get_memory_service(memory_dao: MemoryDAO = Depends(get_memory_dao),
                       ai_service: AIService = Depends(get_ai_service),
                       memory_converter: MemoryConverter = Depends(get_memory_converter),
                       persona_service: PersonaService = Depends(get_persona_service),
                       story_service: StoryService = Depends(get_story_service),
                       story_conversation_service: StoryConversationService = Depends(get_conversation_service)):
    return MemoryService(memory_dao=memory_dao,
                         ai_service=ai_service,
                         memory_converter=memory_converter,
                         persona_service=persona_service,
                         story_service=story_service,
                         story_conversation_service=story_conversation_service)


def get_story_disagreement_converter():
    return StoryDisagreementConverter()


def get_story_interesting_note_converter():
    return StoryInterestingNoteConverter()


def get_introspection_dao(db: Session = Depends(get_db)):
    return IntrospectionDAO(db=db)

def get_persona_aspect_dao(db: Session = Depends(get_db)) -> PersonaAspectDao:
    return PersonaAspectDao(db=db)




def get_persona_aspect_service(ai_service: AIService = Depends(get_ai_service),
                               persona_aspect_dao: PersonaAspectDao = Depends(get_persona_aspect_dao),
                               persona_aspect_converter: PersonaAspectConverter = Depends(get_persona_aspect_converter),
                               backstory_service: BackstoryService = Depends(get_backstory_service),
                               persona_service: PersonaService = Depends(get_persona_service)) -> PersonaAspectService:
    return PersonaAspectService(ai_service=ai_service,
                                persona_aspect_dao=persona_aspect_dao,
                                persona_aspect_converter=persona_aspect_converter,
                                backstory_service=backstory_service,
                                persona_service=persona_service
                                )



def get_introspection_service(ai_service: AIService = Depends(get_ai_service),
                              introspection_dao: IntrospectionDAO = Depends(get_introspection_dao),
                              persona_service: PersonaService = Depends(get_persona_service),
                              introspection_converter: IntrospectionConverter = Depends(get_introspection_converter),
                              speech_profile_service: SpeechProfileService = Depends(get_speech_profile_service),
                              conversation_service: ConversationService = Depends(get_conversation_service),
                              memory_service: MemoryService = Depends(get_memory_service),
                              conversation_converter: ConversationConverter = Depends(get_conversation_converter),
                              conversation_dao: ConversationDAO = Depends(get_conversation_dao),
                              backstory_converter: BackstoryConverter = Depends(get_backstory_converter),
                              aspect_service: PersonaAspectService = Depends(get_persona_aspect_service),
                              ):
    return IntrospectionService(ai_service=ai_service,
                                persona_service=persona_service,
                                introspection_converter=introspection_converter,
                                introspection_dao=introspection_dao,
                                speech_profile_service=speech_profile_service,
                                conversation_service=conversation_service,
                                memory_service=memory_service,
                                conversation_converter=conversation_converter,
                                conversation_dao=conversation_dao,
                                backstory_converter=backstory_converter,
                                aspect_service=aspect_service
                                )


def get_accessory_dao(db: Session = Depends(get_db)):
    return AccessoryDAO(db=db)


def get_accessory_service(ai_service: AIService = Depends(get_ai_service),
                          accessory_converter: AccessoryConverter = Depends(get_accessory_converter),
                          backstory_service: BackstoryService = Depends(get_backstory_service),
                          accessory_dao: AccessoryDAO = Depends(get_accessory_dao),
                          physical_description_service: PhysicalDescriptionService = Depends(
                              get_physical_description_service),
                          persona_service: PersonaService = Depends(get_persona_service),
                          universe_description_service: UniverseDescriptionService = Depends(get_universe_description_service)) -> AccessoryService:
    return AccessoryService(
        ai_service=ai_service,
        accessory_converter=accessory_converter,
        backstory_service=backstory_service,
        accessory_dao=accessory_dao,
        persona_service=persona_service,
        physical_description_service=physical_description_service,
        universe_description_service=universe_description_service,

    )


def get_clothing_dao(db: Session = Depends(get_db)):
    return ClothingDAO(db=db)


def get_clothing_service(ai_service: AIService = Depends(get_ai_service),
                         clothing_dao: ClothingDAO = Depends(get_clothing_dao),
                         clothing_converter: ClothingConverter = Depends(get_clothing_converter),
                         physical_description_service: PhysicalDescriptionService = Depends(
                            get_physical_description_service),
                        universe_service: UniverseService = Depends(get_universe_service),
                         persona_backstory_service: BackstoryService = Depends(
                             get_backstory_service)) -> ClothingService:
    return ClothingService(
        ai_service=ai_service,
        clothing_converter=clothing_converter,
        clothing_dao=clothing_dao,
        persona_background_service=persona_backstory_service,
        physical_description_service=physical_description_service,
        universe_service=universe_service
    )


def get_speech_sample_dao(db: Session = Depends(get_db)):
    return SpeechSampleDAO(db=db)


def get_speech_sample_service(ai_service: AIService = Depends(get_ai_service),
                              speech_sample_converter: SpeechSampleConverter = Depends(get_speech_sample_converter),
                              speech_sample_dao: SpeechSampleDAO = Depends(get_speech_sample_dao),
                              persona_service: PersonaService = Depends(get_persona_service)) -> SpeechSampleService:
    return SpeechSampleService(
        ai_service=ai_service,
        speech_sample_dao=speech_sample_dao,
        speech_sample_converter=speech_sample_converter,
        persona_service=persona_service)


def get_reasoning_conversation_dao(db: Session = Depends(get_db)):
    return ReasoningConversationDAO(db=db)


def get_reasoning_converter(conversation_converter: ConversationConverter = Depends(get_conversation_converter)):
    return ReasoningConversationConverter(conversation_converter=conversation_converter)


def get_reasoning_conversation_service(
        reasoning_dao: ReasoningConversationDAO = Depends(get_reasoning_conversation_dao),
        reasoning_converter: ReasoningConversationConverter = Depends(get_reasoning_converter),
        persona_service: PersonaService = Depends(get_persona_service),
        ai_service: AIService = Depends(get_ai_service),
        backstory_service: BackstoryService = Depends(get_backstory_service),
        conversation_dao: ConversationDAO = Depends(get_conversation_dao),
        conversation_converter: ConversationConverter = Depends(get_conversation_converter),
        universe_service=Depends(get_universe_service),
        conversation_service=Depends(get_conversation_service),
        ):
    return ReasoningConversationService(ai_service=ai_service,
                                        reasoning_converter=reasoning_converter,
                                        reasoning_dao=reasoning_dao,
                                        persona_service=persona_service,
                                        backstory_service=backstory_service,
                                        conversation_dao=conversation_dao,
                                        conversation_converter=conversation_converter,
                                        universe_service=universe_service,
                                        conversation_service=conversation_service
                                        )



def get_monologue_dao(db: Session = Depends(get_db)):
    return MonologueDAO(db=db)


def get_monologue_converter_ai(conversation_converter: ConversationConverter = Depends(get_conversation_converter)):
    return MonologueConverter(conversation_converter=conversation_converter)


def get_monologue_service(ai_service: AIService = Depends(get_ai_service),
                          monologue_dao: MonologueDAO = Depends(get_monologue_dao),
                          monologue_converter: MonologueConverter = Depends(get_monologue_converter_ai),
                          backstory_service: BackstoryService = Depends(get_backstory_service),
                          speech_profile_service: SpeechProfileService = Depends(get_speech_profile_service),
                          conversation_converter: ConversationConverter = Depends(get_conversation_converter),
                          conversation_dao: ConversationDAO = Depends(get_conversation_dao),
                          persona_service: PersonaService = Depends(get_persona_service),
                          ):
    return MonologueService(
        ai_service=ai_service,
        backstory_service=backstory_service,
        monologue_dao=monologue_dao,
        monologue_converter=monologue_converter,
        speech_profile_service=speech_profile_service,
        conversation_converter=conversation_converter,
        conversation_dao=conversation_dao,
        persona_service=persona_service,
    )


def get_relationship_service(relationship_converter: RelationshipConverter = Depends(get_relationship_converter),
                             ai_service: AIService = Depends(get_ai_service),
                             backstory_service: BackstoryService = Depends(get_backstory_service),
                             persona_service: PersonaService = Depends(get_persona_service),
                             relationship_dao: RelationshipDAO = Depends(get_relationship_dao)):
    return RelationshipService(relationship_converter=relationship_converter, persona_service=persona_service,
                               backstory_service=backstory_service, ai_service=ai_service,
                               relationship_dao=relationship_dao)


def get_group_reasoning_dao(db: Session = Depends(get_db)):
    return GroupReasoningStyleDAO(db=db)


def get_group_reasoning_converter():
    return GroupReasoningConverter()


def get_group_reasoning_style_service(ai_service: AIService = Depends(get_ai_service),
                                      group_reasoning_converter_service: GroupReasoningConverter = Depends(
                                          get_group_reasoning_converter),
                                      group_reasoning_dao: GroupReasoningStyleDAO = Depends(get_group_reasoning_dao),
                                      persona_service: PersonaService = Depends(get_persona_service)):
    return GroupReasoningProfileService(ai_service=ai_service,
                                        group_reasoning_dao=group_reasoning_dao,
                                        group_reasoning_converter=group_reasoning_converter_service,
                                        persona_service=persona_service)


def get_conversation_data_service(conversation_converter: ConversationConverter = Depends(get_conversation_converter),
                                  conversation_dao: ConversationDAO = Depends(get_conversation_dao),
                                  persona_service: PersonaService = Depends(get_persona_service),
                                  introspection_service: IntrospectionService = Depends(get_introspection_service),
                                  story_conversation_service: StoryConversationService = Depends(
                                      get_story_conversation_service),
                                  monologue_service: MonologueService = Depends(get_monologue_service),
                                  reasoning_service: ReasoningConversationService = Depends(
                                      get_reasoning_conversation_service)):
    return ConversationDataService(conversation_converter=conversation_converter,
                                   conversation_dao=conversation_dao,
                                   persona_service=persona_service,
                                   introspection_service=introspection_service,
                                   story_conversation_service=story_conversation_service,
                                   monologue_service=monologue_service,
                                   reasoning_service=reasoning_service,
                                   )


def get_like_data_service(like_service: LikeService = Depends(get_like_service),
                          persona_service: PersonaService = Depends(get_persona_service), ):
    return LikeDataService(like_service=like_service,
                           persona_service=persona_service)


def get_memory_data_service(story_service: StoryService = Depends(get_story_service),
                            memory_service: MemoryService = Depends(get_memory_service),
                            persona_service: PersonaService = Depends(get_persona_service), ):
    return MemoryDataService(story_service=story_service,
                             memory_service=memory_service,
                             persona_service=persona_service)


def get_reasoning_style_data_service(persona_service: PersonaService = Depends(get_persona_service), ):
    return ReasoningStyleDataService(persona_service=persona_service)


def get_relationship_data_service(persona_service: PersonaService = Depends(get_persona_service), ):
    return RelationshipDataService(persona_service=persona_service)


def get_speech_data_service(persona_service: PersonaService = Depends(get_persona_service),
                            speech_service: SpeechSampleService = Depends(get_speech_sample_service)):
    return SpeechDataService(persona_service=persona_service,
                             speech_sample_service=speech_service)

def get_self_description_conversation_converter(conversation_converter: ConversationConverter = Depends(get_conversation_converter)):
    return SelfDescriptionConversationConverter(conversation_converter=conversation_converter)

def get_self_description_conversation_dao(db: Session = Depends(get_db)):
    return SelfDescriptionConversationDao(db=db)

def get_self_description_conversation_service(ai_service: AIService = Depends(get_ai_service),
                                      conversation_service: ConversationService = Depends(get_conversation_service),
                                      self_description_conversation_dao: SelfDescriptionConversationDao = Depends(get_self_description_conversation_dao),
                                      backstory_service: BackstoryService = Depends(get_backstory_service),
                                      self_description_conversation_converter: SelfDescriptionConversationConverter = Depends(get_self_description_conversation_converter),
                                              aspect_service: PersonaAspectService = Depends(get_persona_aspect_service),
                                              persona_service: PersonaService = Depends(get_persona_service)):
    return SelfDescriptionConversationService(
        ai_service=ai_service,
        conversation_service=conversation_service,
        self_description_conversation_dao=self_description_conversation_dao,
        backstory_service=backstory_service,
        self_description_conversation_converter=self_description_conversation_converter,
        persona_service=persona_service,
        aspect_service=aspect_service,
    )

def get_story_data_service(persona_service: PersonaService = Depends(get_persona_service),
                           story_service: StoryService = Depends(get_story_service), ):
    return StoryDataService(persona_service=persona_service,
                            story_service=story_service)



def get_introspection_data_service(persona_service: PersonaService = Depends(get_persona_service),
                                   introspection_service: IntrospectionService = Depends(get_introspection_service), ):
    return IntrospectionDataService(persona_service=persona_service, introspection_service=introspection_service)


def get_base_data_generator(universe_service: UniverseService = Depends(get_universe_service), ):
    return BaseDataService(universe_service=universe_service)


def get_habit_dao(db: Session = Depends(get_db)):
    return HabitDAO(db_session=db)


def get_habit_service(ai_service: AIService = Depends(get_ai_service),
                      backstory_converter: BackstoryConverter = Depends(get_backstory_converter),
                      conversation_service: ConversationService = Depends(get_conversation_service),
                      habit_dao: HabitDAO = Depends(get_habit_dao),
                      persona_service: PersonaService = Depends(get_persona_service),
                      backstory_service: BackstoryService = Depends(get_backstory_service),
                      habit_converter: HabitConverter = Depends(get_habit_converter)) -> HabitService:
    return HabitService(
        ai_service=ai_service,
        backstory_converter=backstory_converter,
        habit_dao=habit_dao,
        habit_converter=habit_converter,
        persona_service=persona_service,
        conversation_service=conversation_service,
        backstory_service=backstory_service,
    )


def get_habit_data_service(habit_service: HabitService = Depends(get_habit_service), persona_service: PersonaService = Depends(get_persona_service),):
    return HabitDataService(habit_service=habit_service, persona_service=persona_service)


def get_hobby_dao(db: Session = Depends(get_db)) -> HobbyDAO:
    return HobbyDAO(db=db)

def get_hobby_service(ai_service: AIService = Depends(get_ai_service),
                      backstory_service: BackstoryService = Depends(get_backstory_service),
                      hobby_converter: HobbyConverter = Depends(get_hobby_converter),
                      hobby_dao: HobbyDAO = Depends(get_hobby_dao)) -> HobbyService:
    return HobbyService(
        ai_service=ai_service,
        backstory_service=backstory_service,
        hobby_converter=hobby_converter,
        hobby_dao=hobby_dao)

def get_hobby_data_service(hobby_service: HobbyService = Depends(get_hobby_service),
                           person_service: PersonaService = Depends(get_persona_service)):
    return HobbyDataService(hobby_service=hobby_service,
                            persona_service=person_service)


def get_monologue_data_service(monologue_service: MonologueService = Depends(get_monologue_service)):
    return MonologueDataService(monologue_service=monologue_service)

def get_persona_fact_dao(db: Session = Depends(get_db)):
    return PersonaFactDAO(db=db)

def get_persona_fact_converter():
    return PersonaFactConverter()

def get_persona_fact_service(ai_service: AIService = Depends(get_ai_service),
                             persona_fact_dao: PersonaFactDAO = Depends(get_persona_fact_dao),
                             backstory_service: BackstoryService = Depends(get_backstory_service),
                             persona_fact_converter: PersonaFactConverter = Depends(get_persona_fact_converter)
                             ):
    return PersonaFactService(ai_service=ai_service,
                              persona_fact_dao=persona_fact_dao,
                              persona_fact_converter=persona_fact_converter,
                              backstory_service=backstory_service)

def get_fact_data_service(fact_service: PersonaFactService = Depends(get_persona_fact_service),
                          persona_service: PersonaService = Depends(get_persona_service)):
    return FactDataService(fact_service=fact_service,
                           persona_service=persona_service)

def get_self_description_conversation_data_service(persona_service: PersonaService = Depends(get_persona_service),
                                                   self_description_conversation_service: SelfDescriptionConversationService = Depends(get_self_description_conversation_service)):
    return SelfDescriptionDataService(
        persona_service=persona_service,
        self_description_conversation_service=self_description_conversation_service
    )
def get_data_generation_service(persona_service: PersonaService = Depends(get_persona_service),
                                story_service: StoryService = Depends(get_story_service),
                                story_data_service: StoryDataService = Depends(get_story_data_service),
                                conversation_data_service: ConversationDataService = Depends(
                                    get_conversation_data_service),
                                speech_data_service: SpeechDataService = Depends(get_speech_data_service),
                                memory_data_service: MemoryDataService = Depends(get_memory_data_service),
                                relationship_data_service: RelationshipDataService = Depends(
                                    get_relationship_data_service),
                                like_data_service: LikeDataService = Depends(get_like_data_service),
                                introspection_data_service: IntrospectionDataService = Depends(
                                    get_introspection_data_service),
                                base_data_service: BaseDataService = Depends(get_base_data_generator),
                                reasoning_service: ReasoningConversationService = Depends(
                                    get_reasoning_conversation_service),
                                habit_data_service: HabitDataService = Depends(get_habit_data_service),
                                monologue_data_service: MonologueDataService = Depends(get_monologue_data_service),
                                hobby_data_service: HobbyDataService = Depends(get_hobby_data_service),
                                self_description_conversation_data_service: SelfDescriptionDataService = Depends(get_self_description_conversation_data_service),
                                fact_data_service: FactDataService = Depends(get_fact_data_service),
                                ):
    return DataGenerationService(
        persona_service=persona_service,
        story_service=story_service,
        conversation_data_service=conversation_data_service,
        speech_data_service=speech_data_service,
        relationship_data_service=relationship_data_service,
        like_data_service=like_data_service,
        story_data_service=story_data_service,
        memory_data_service=memory_data_service,
        introspection_data_service=introspection_data_service,
        base_data_service=base_data_service,
        reasoning_service=reasoning_service,
        habit_data_service=habit_data_service,
        monologue_data_service=monologue_data_service,
        hobby_data_service=hobby_data_service,
        self_description_conversation_data_service=self_description_conversation_data_service,
        fact_data_service=fact_data_service
    )

def get_extended_monologue_service(ai_service: AIService = Depends(get_ai_service),
                                   monologue_converter: MonologueConverter = Depends(get_monologue_converter_ai),
                                   backstory_converter: BackstoryConverter = Depends(get_backstory_converter),
                                   persona_service: PersonaService = Depends(get_persona_service),
                                   monologue_service: MonologueService = Depends(get_monologue_service)):
    return ExtendedMonologueService(ai_service=ai_service,
                                    monologue_converter=monologue_converter,
                                    monologue_service=monologue_service,
                                    backstory_converter=backstory_converter,
                                    persona_service=persona_service)


def get_objective_persona_description_service(ai_service: AIService = Depends(get_ai_service)):
    return PersonaObjectiveDescriptionService(ai_service=ai_service)


def check_universe_exists(universe_id: int, universe_service: UniverseService = Depends(get_universe_service)):
    if not universe_service.exists(universe_id):
        raise HTTPException(status_code=404, detail="Universe not found")


def get_team_service(ai_service: AIService = Depends(get_ai_service),):
    return TeamService(ai_service=ai_service)

def get_persona_knowledge_service(ai_service: AIService = Depends(get_ai_service),
                                  persona_knowledge_dao: PersonaKnowledgeDAO = Depends(get_persona_knowledge_dao),
                                  persona_knowledge_converter: PersonaKnowledgeConverter = Depends(get_persona_knowledge_converter),
                                  ):
    return PersonaKnowledgeService(ai_service=ai_service,
                                    persona_knowledge_converter=persona_knowledge_converter,
                                    persona_knowledge_dao=persona_knowledge_dao)

def get_persona_skill_service(ai_service: AIService = Depends(get_ai_service),
                              persona_skill_dao: PersonaSkillDAO = Depends(get_persona_skill_dao),
                              persona_skill_converter: PersonaSkillConverter = Depends(get_persona_skill_converter),
                              ):
    return PersonaSkillService(ai_service=ai_service,
                                persona_skill_converter=persona_skill_converter,
                                persona_skill_dao=persona_skill_dao)