from converter.backstory_converter import BackstoryConverter
from converter.group_reasoning_converter import GroupReasoningConverter
from converter.life_event_converter import LifeEventConverter
from converter.persona_knowledge_converter import PersonaKnowledgeConverter
from converter.persona_skill_converter import PersonaSkillConverter
from converter.physical_description_converter import PhysicalDescriptionConverter
from converter.relationship_converter import RelationshipConverter
from converter.speech_profile_converter import SpeechProfileConverter
from entity.base import PersonaEntity
from models.persona import Persona


class PersonaConverter:
    def __init__(self,
                 backstory_converter: BackstoryConverter,
                 physical_description_converter: PhysicalDescriptionConverter,
                 speech_profile_converter: SpeechProfileConverter,
                 life_event_converter: LifeEventConverter,
                 relationship_converter: RelationshipConverter,
                 group_reasoning_converter: GroupReasoningConverter,
                 persona_skill_converter: PersonaSkillConverter,
                 persona_knowledge_converter: PersonaKnowledgeConverter):
        self.backstory_converter = backstory_converter
        self.physical_description_converter = physical_description_converter
        self.speech_profile_converter = speech_profile_converter
        self.life_event_converter = life_event_converter
        self.relationship_converter = relationship_converter
        self.group_reasoning_converter = group_reasoning_converter
        self.persona_skill_converter = persona_skill_converter
        self.persona_knowledge_converter = persona_knowledge_converter

    def model_to_entity(self, persona: Persona) -> PersonaEntity:
        result = PersonaEntity(
            id=persona.id,
            universe_id=persona.universe_id
        )
        result.backstory = self.backstory_converter.model_to_entity(persona.backstory, persona.id)
        result.physical_description = self.physical_description_converter.model_to_entity(persona.physical_description)
        result.speech = self.speech_profile_converter.model_to_entity(persona.speech_profile)
        result.life_events = [self.life_event_converter.model_to_entity(life_event) for life_event in persona.life_events]
        result.relationships = [self.relationship_converter.model_to_entity(relationship) for relationship in persona.relationships]
        result.group_reasoning_profile = self.group_reasoning_converter.model_to_entity(persona.group_reasoning_profile)
        result.skills = [self.persona_skill_converter.entity_to_model(skill_entity=skill_entity) for skill_entity in persona.skills]
        result.knowledge = [self.persona_knowledge_converter.entity_to_model(persona_knowledge_entity=knowledge_entity) for knowledge_entity in persona.knowledge]
        return result

    def entity_to_model(self, persona_entity: PersonaEntity) -> Persona:
        knowledge = [self.persona_knowledge_converter.entity_to_model(knowledge) for knowledge in persona_entity.knowledges]
        skills = [self.persona_skill_converter.entity_to_model(skill) for skill in persona_entity.skills]
        backstory = self.backstory_converter.entity_to_model(persona_entity.backstory)
        physical_description = self.physical_description_converter.entity_to_model(persona_entity.physical_descriptions)
        speech_profile = self.speech_profile_converter.entity_to_model(persona_entity.speech_profile)
        life_events = [self.life_event_converter.entity_to_model(life_event) for life_event in persona_entity.life_events]
        relationships = [self.relationship_converter.entity_to_model(relationship) for relationship in persona_entity.relationships]
        group_reasoning_profile = self.group_reasoning_converter.entity_to_model(persona_entity.group_reasoning_style)
        persona_model = Persona(
            id=persona_entity.id,
            universe_id=persona_entity.universe_id,
            knowledge=knowledge,
            skills=skills,
            backstory=backstory,
            physical_description=physical_description,
            speech_profile=speech_profile,
            life_events=life_events,
            relationships=relationships,
            group_reasoning_profile=group_reasoning_profile
        )

        return persona_model
