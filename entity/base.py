from sqlalchemy import Integer, String, create_engine, ForeignKey, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker, relationship

from entity.role import Role

engine = create_engine(f"sqlite:///./database/maths_32b.sqlite")
SessionLocal = sessionmaker(engine)



class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class MemoryEntity(Base):
    __tablename__ = "memory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    memory: Mapped[str] = mapped_column(String())
    core_memory: Mapped[bool] = mapped_column(Boolean())
    feelings_stirred: Mapped[str] = mapped_column(String())
    story_id: Mapped[int] = mapped_column(Integer, ForeignKey("story.id"))
    story = relationship("StoryEntity", back_populates="memories")
    memory_reflex: Mapped[str] = mapped_column(String(), nullable=False)
    memory_reflex_followup: Mapped[str] = mapped_column(String(), nullable=False)


class HairStyleEntity(Base):
    __tablename__ = "hair_styles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    occasion: Mapped[str] = mapped_column(String(), nullable=True)
    description: Mapped[str] = mapped_column(String(), nullable=True)
    physical_description_id: Mapped[int] = mapped_column(Integer, ForeignKey("physical_description.id"))
    physical_description = relationship("PhysicalDescriptionEntity", back_populates="hair_styles")


class ClothingEntity(Base):
    __tablename__ = "clothings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    clothing_category: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    occasion: Mapped[str] = mapped_column(String(), nullable=True)
    purpose: Mapped[str] = mapped_column(String(), nullable=True)
    personal_significance: Mapped[str] = mapped_column(String(), nullable=True)
    physical_description_id: Mapped[int] = mapped_column(Integer, ForeignKey("physical_description.id"))
    physical_description = relationship("PhysicalDescriptionEntity", back_populates="clothing")
    diffusion_model_description: Mapped[str] = mapped_column(String())

class AccessoryEntity(Base):
    __tablename__ = "accessory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_type: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    occasion: Mapped[str] = mapped_column(String(), nullable=True)
    personal_significance: Mapped[str] = mapped_column(String(), nullable=True)
    physical_description_id: Mapped[int] = mapped_column(Integer, ForeignKey('physical_description.id'))
    physical_description = relationship("PhysicalDescriptionEntity", back_populates="accessories")
    name: Mapped[str] = mapped_column(String(), nullable=False)
    diffusion_model_description: Mapped[str] = mapped_column(String())

class PhysicalDescriptionEntity(Base):
    __tablename__ = "physical_description"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    height: Mapped[str] = mapped_column(String())
    weight: Mapped[str] = mapped_column(String())
    hair_color: Mapped[str] = mapped_column(String(), nullable=True)
    hair_styles = relationship("HairStyleEntity", back_populates="physical_description", cascade="all, delete-orphan")
    accessories = relationship("AccessoryEntity", back_populates="physical_description", cascade="all, delete-orphan")
    clothing = relationship("ClothingEntity", back_populates="physical_description", cascade="all, delete-orphan")
    interesting_notes = relationship("PhysicalDescriptionInterestingNoteEntity", back_populates="physical_description", cascade="all, delete-orphan")
    detailed_description: Mapped[str] = mapped_column(String())
    presentation: Mapped[str] = mapped_column(String())
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey("persona.id"))
    persona = relationship("PersonaEntity", back_populates="physical_descriptions")
    diffusion_model_description: Mapped[str] = mapped_column(String())

class PhysicalDescriptionInterestingNoteEntity(Base):
    __tablename__ = "physical_description_interesting_notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String())
    physical_description_id: Mapped[int] = mapped_column(Integer, ForeignKey("physical_description.id"))
    physical_description = relationship("PhysicalDescriptionEntity", back_populates="interesting_notes")


class SpeechProfileEntity(Base):
    __tablename__ = "speech_profile"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String())
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey("persona.id"))
    persona = relationship("PersonaEntity", back_populates="speech_profile")
    samples = relationship("SpeechSampleEntity", back_populates="speech_profile")
    emotional_description: Mapped[str] = mapped_column(String())
    emojis_allowed: Mapped[bool] = mapped_column(Integer())
    verbose: Mapped[bool] = mapped_column(Integer())

class SpeechSampleEntity(Base):
    __tablename__ = "speech_sample"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tone: Mapped[str] = mapped_column(String())
    example: Mapped[str] = mapped_column(String())
    situation: Mapped[str] = mapped_column(String())
    speech_profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("speech_profile.id"))
    speech_profile = relationship("SpeechProfileEntity", back_populates="samples")
    explanation: Mapped[str] = mapped_column(String(), nullable=True)
    feeling: Mapped[str] = mapped_column(String(), nullable=True)

class UniverseDescriptionEntity(Base):
    __tablename__ = "universe_description"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String())
    creatures: Mapped[str] = mapped_column(String())
    universe_id: Mapped[int] = mapped_column(Integer, ForeignKey("universes.id"))
    universe = relationship("UniverseEntity", back_populates="universe_description")

class UniverseMetadataEntity(Base):
    __tablename__ = "universe_metadata"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    universe_id: Mapped[int] = mapped_column(Integer, ForeignKey("universes.id"))
    universe = relationship("UniverseEntity", back_populates="universe_metadata")

class UniverseEntity(Base):
    __tablename__  = "universes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    universe_description = relationship("UniverseDescriptionEntity", back_populates="universe", uselist=False, cascade="all, delete-orphan")
    personas = relationship("PersonaEntity", back_populates="universe")
    universe_metadata = relationship("UniverseMetadataEntity", back_populates="universe")
    locations = relationship("UniverseLocationEntity", back_populates="universe", cascade="all, delete-orphan")
    name: Mapped[str] = mapped_column(String(), unique=True)

class RelationshipThoughtEntity(Base):
    __tablename__ = "relationship_thoughts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    persona_relationship = relationship("PersonaRelationshipEntity", back_populates="thoughts")
    persona_relationship_id: Mapped[int] = mapped_column(Integer, ForeignKey("persona_relationship.id"))
    thought: Mapped[str] = mapped_column(String())

class RelationshipFeelingEntity(Base):
    __tablename__ = "relationships"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    persona_relationship = relationship("PersonaRelationshipEntity", back_populates="feelings")
    persona_relationship_id: Mapped[int] = mapped_column(Integer, ForeignKey("persona_relationship.id"))
    feeling_name: Mapped[str] = mapped_column(String())
    reason: Mapped[str] = mapped_column(String())

class PersonaRelationshipEntity(Base):
    __tablename__ = "persona_relationship"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    source = relationship("PersonaEntity", back_populates="relationships", foreign_keys="PersonaRelationshipEntity.source_id")
    source_id = mapped_column(Integer, ForeignKey("persona.id"))

    target = relationship("PersonaEntity", back_populates="relationships", foreign_keys="PersonaRelationshipEntity.target_id")
    target_id = mapped_column(Integer, ForeignKey("persona.id"))

    thoughts = relationship("RelationshipThoughtEntity", back_populates="persona_relationship")
    feelings = relationship("RelationshipFeelingEntity", back_populates="persona_relationship")
    relationship_type: Mapped[str] = mapped_column(String())
    relationship_subtype: Mapped[str] = mapped_column(String())
    overall_description: Mapped[str] = mapped_column(String())


class PersonaEntity(Base):
    __tablename__ = "persona"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    universe_id: Mapped[int] = mapped_column(Integer(), ForeignKey("universes.id"), nullable=False)
    universe = relationship("UniverseEntity", back_populates="personas")
    backstory = relationship("BackstoryEntity", back_populates="persona", uselist=False, cascade="all, delete-orphan")
    physical_descriptions = relationship("PhysicalDescriptionEntity", back_populates="persona", uselist=False, cascade="all, delete-orphan")
    speech_profile = relationship("SpeechProfileEntity", back_populates="persona", uselist=False)
    life_events = relationship("LifeEventEntity", back_populates="persona")
    reasoning_conversations = relationship("ReasoningConversationEntity", back_populates="persona")
    monologues_prompter = relationship("MonologueEntity", foreign_keys="MonologueEntity.prompter_id", cascade="all, delete-orphan")
    monologues_speaker = relationship("MonologueEntity", foreign_keys="MonologueEntity.speaker_id", cascade="all, delete-orphan")
    relationships = relationship("PersonaRelationshipEntity", back_populates="source", foreign_keys="PersonaRelationshipEntity.source_id")
    group_reasoning_style = relationship("GroupReasoningStyleEntity", back_populates="persona", uselist=False)
    facts = relationship("PersonaFactEntity", back_populates="persona", cascade="all, delete-orphan")
    skills = relationship("PersonaSkillEntity", back_populates="persona", cascade="all, delete-orphan")
    knowledges = relationship("PersonaKnowledgeEntity", back_populates="persona", cascade="all, delete-orphan")


class UniverseLocationEntity(Base):
    __tablename__ = "universe_location"
    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    purpose: Mapped[str] = mapped_column(String())
    visual_description: Mapped[str] = mapped_column(String())
    universe_id: Mapped[int] = mapped_column(Integer, ForeignKey("universes.id"))
    universe = relationship("UniverseEntity", back_populates="locations")



class HabitEntity(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    frequency: Mapped[str] = mapped_column(String())
    backstory_id: Mapped[int] = mapped_column(Integer, ForeignKey('backstory.id'))
    backstory = relationship("BackstoryEntity", back_populates="habits")
    good_habit: Mapped[bool] = mapped_column(Boolean())
    description: Mapped[str] = mapped_column(String(), nullable=False)

class LikesEntity(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    backstory_id: Mapped[int] = mapped_column(Integer, ForeignKey('backstory.id'))
    backstory = relationship("BackstoryEntity", back_populates="likes")
    like_name: Mapped[str] = mapped_column(String(255), nullable=False)
    like_reason: Mapped[str] = mapped_column(String(), nullable=False)
    dislike_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dislike_reason: Mapped[str] = mapped_column(String(), nullable=False)
    contradiction_explanation: Mapped[str] = mapped_column(String(), nullable=False)
    contradiction: Mapped[str] = mapped_column(String(), nullable=False)

class HobbyEntity(Base):
    __tablename__ = "hobby"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=False)
    backstory_id: Mapped[int] = mapped_column(Integer, ForeignKey('backstory.id'))
    backstory = relationship("BackstoryEntity", back_populates="hobbies")


class BackstoryEntity(Base):
    __tablename__ = "backstory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    place_of_birth: Mapped[str] = mapped_column(String(255), nullable=False)
    date_of_birth: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    education_description: Mapped[str] = mapped_column(String(255), nullable=False)
    social_description: Mapped[str] = mapped_column(String(255), nullable=False)
    persona = relationship("PersonaEntity", back_populates="backstory")
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey('persona.id'))
    habits = relationship("HabitEntity", back_populates="backstory", cascade="all, delete-orphan")
    likes = relationship("LikesEntity", back_populates="backstory", cascade="all, delete-orphan")
    hobbies = relationship("HobbyEntity", back_populates="backstory", cascade="all, delete-orphan")
    historical: Mapped[bool] = mapped_column(Boolean())
    gender: Mapped[str] = mapped_column(String())
    aspects = relationship("PersonaAspectEntity", back_populates="backstory", cascade="all, delete-orphan")

class StoryInterestingNoteEntity(Base):
    __tablename__ = "story_interesting_notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(String(255), nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, ForeignKey('story.id'))
    story = relationship("StoryEntity", back_populates="interesting_notes")

class StoryDisagreementEntity(Base):
    __tablename__ = "story_disagreements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(String(255), nullable=False)
    story_id: Mapped[int] = mapped_column(Integer, ForeignKey('story.id'))
    story = relationship("StoryEntity", back_populates="disagreements")

class LifeEventEntity(Base):
    __tablename__ = "life_event"
    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String())
    detail_learned: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    date: Mapped[str] = mapped_column(String())
    persona_id = mapped_column(Integer, ForeignKey("persona.id"))
    persona = relationship("PersonaEntity", back_populates="life_events")
    story = relationship("StoryEntity", back_populates="life_event", cascade="all, delete-orphan", uselist=False)


class StoryEntity(Base):
    __tablename__ = "story"
    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String())
    lead_up: Mapped[str] = mapped_column(String())
    story: Mapped[str] = mapped_column(String())
    outcome: Mapped[str] = mapped_column(String())
    life_event_id: Mapped[int] = mapped_column(Integer, ForeignKey('life_event.id'))
    life_event = relationship("LifeEventEntity", back_populates="story")
    interesting_notes = relationship("StoryInterestingNoteEntity", back_populates="story", cascade="all, delete-orphan")
    disagreements = relationship("StoryDisagreementEntity", back_populates="story", cascade="all, delete-orphan")
    memories = relationship("MemoryEntity", back_populates="story", cascade="all, delete-orphan")
    introspections = relationship("IntrospectionEntity", back_populates="story", cascade="all, delete-orphan")

class ReasoningConversationEntity(Base):
    __tablename__ = "reasoning_conversation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    problem_statement: Mapped[str] = mapped_column(String())
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey('persona.id'))
    persona = relationship("PersonaEntity", back_populates="reasoning_conversations")
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey('conversation.id'))
    conversation = relationship("ConversationEntity", uselist=False)
    theme: Mapped[str] = mapped_column(String(), nullable=True)

class GroupReasoningStyleEntity(Base):
    __tablename__ = "group_reasoning_style"
    id = mapped_column(Integer, primary_key=True)
    assumed_role: Mapped[str] = mapped_column(String())
    tone: Mapped[str] = mapped_column(String())
    devils_advocate: Mapped[bool] = mapped_column(Boolean())
    sarcastic: Mapped[bool] = mapped_column(Boolean())
    reserved: Mapped[bool] = mapped_column(Boolean())
    witty: Mapped[bool] = mapped_column(Boolean())
    subtle: Mapped[bool] = mapped_column(Boolean())
    persona_id = mapped_column(Integer, ForeignKey('persona.id'))
    persona = relationship("PersonaEntity", back_populates="group_reasoning_style")

class ConversationEntity(Base):
    __tablename__ = "conversation"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_turns = relationship("ConversationTurnEntity", back_populates="conversation")
    source: Mapped[str] = mapped_column(String())
    source_id = mapped_column(Integer)

class ConversationTurnEntity(Base):
    __tablename__ = "conversation_turn"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speaker: Mapped[str] = mapped_column(String())
    text: Mapped[str] = mapped_column(String())
    action: Mapped[str] = mapped_column(String(), nullable=True)
    tone: Mapped[str] = mapped_column(String(), nullable=False)
    directed_at = relationship("ConversationTurnDirectedAtEntity", back_populates="conversation_turn", cascade="all, delete-orphan")
    placement: Mapped[int] = mapped_column(Integer())
    conversation_id: Mapped[int] = mapped_column(Integer(), ForeignKey('conversation.id'))
    conversation = relationship("ConversationEntity", back_populates="conversation_turns")
    thought: Mapped[str] = mapped_column(String(), nullable=True)
    feeling: Mapped[str] = mapped_column(String(), nullable=False)
    turn_intent: Mapped[str] = mapped_column(String(), nullable=True)
    private_thought: Mapped[str] = mapped_column(String(), nullable=True)

class ConversationTurnDirectedAtEntity(Base):
    __tablename__ = "conversation_turn_directed_at"
    id = mapped_column(Integer, primary_key=True)
    conversation_turn_id: Mapped[int] = mapped_column(Integer, ForeignKey('conversation_turn.id'))
    conversation_turn = relationship("ConversationTurnEntity", back_populates="directed_at")
    persona_name = mapped_column(String())

class IntrospectionEntity(Base):
    __tablename__ = "introspection"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story_id: Mapped[int] = mapped_column(Integer(), ForeignKey('story.id'))
    story = relationship("StoryEntity", back_populates="introspections")
    aspect_id: Mapped[int] = mapped_column(Integer(), ForeignKey('persona_aspect.id'))
    personality_aspect_role: Mapped[str] = mapped_column(String())
    introspection_topic: Mapped[str] = mapped_column(String())

class MonologueEntity(Base):
    __tablename__ = "monologue"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speaker_id: Mapped[int] = mapped_column(Integer(), ForeignKey('persona.id'), index=True)
    prompter_id: Mapped[int] = mapped_column(Integer(), ForeignKey('persona.id'))
    prompt: Mapped[str] = mapped_column(String(), nullable=True)
    theme: Mapped[str] = mapped_column(String())
    previous_monologue_id: Mapped[int] = mapped_column(Integer(), ForeignKey('monologue.id'), nullable=True)
    previous_monologue = relationship("MonologueEntity")
    conversation_id: Mapped[int] = mapped_column(Integer(), ForeignKey('conversation.id'))
    conversation = relationship("ConversationEntity", lazy=False, uselist=False)
    deliverable: Mapped[str] = mapped_column(String(), nullable=False)
    problem_type: Mapped[str] = mapped_column(String(), nullable=False)
    trigger_word: Mapped[str] = mapped_column(String(), nullable=True)

class PersonaAspectEntity(Base):
    __tablename__ = "persona_aspect"
    aspect_name: Mapped[str] = mapped_column(String(255))
    aspect_description: Mapped[str] = mapped_column(String(2048))
    backstory_id: Mapped[int] = mapped_column(Integer, ForeignKey('backstory.id'))
    backstory = relationship("BackstoryEntity", back_populates="aspects")
    strength_of_aspect_in_personality: Mapped[int] = mapped_column(Integer())


class PersonaAspectConversationEntity(Base):
    __tablename__ = "persona_aspect_conversation"
    aspect_id: Mapped[int] = mapped_column(Integer, ForeignKey('persona_aspect.id'))
    topic: Mapped[str] = mapped_column(String())

class SelfDescriptionConversationEntity(Base):
    __tablename__ = "self_description_conversation"
    persona_id: Mapped[int] = mapped_column(Integer)
    prompter_id: Mapped[int] = mapped_column(Integer)
    topic: Mapped[str] = mapped_column(String())

class PersonaFactEntity(Base):
    __tablename__ = "persona_fact"
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey('persona.id'))
    persona = relationship("PersonaEntity", back_populates="facts")
    fact: Mapped[str] = mapped_column(String())
    fact_explanation: Mapped[str] = mapped_column(String())

class PromptPerformanceEntity(Base):
    __tablename__ = "prompt_performance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt: Mapped[str] = mapped_column(String())
    time_taken: Mapped[float] = mapped_column(Float())
    response: Mapped[str] = mapped_column(String())
    model: Mapped[str] = mapped_column(String())
    template_name: Mapped[str] = mapped_column(String())

class PersonaSkillEntity(Base):
    __tablename__ = "skill"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_name: Mapped[str] = mapped_column(String())
    skill_description: Mapped[str] = mapped_column(String())
    skill_level: Mapped[str] = mapped_column(String())
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey('persona.id'))
    persona = relationship("PersonaEntity", back_populates="skills")

class PersonaKnowledgeEntity(Base):
    __tablename__ = "knowledge"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    knowledge_name: Mapped[str] = mapped_column(String())
    knowledge_description: Mapped[str] = mapped_column(String())
    knowledge_level: Mapped[str] = mapped_column(String())
    persona_id: Mapped[int] = mapped_column(Integer, ForeignKey('persona.id'))
    persona = relationship("PersonaEntity", back_populates="knowledges")

# class TeamEntity(Base):
#     __tablename__ = "team"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String())
#
# class TeamMember(Base):
#     __tablename__ = "team_member"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     team_id: Mapped[int] = mapped_column(Integer, ForeignKey('team.id'))
#     role: Mapped[str] = mapped_column(enum=Role)
#     persona_id: Mapped[int] = mapped_column(Integer, ForeignKey('persona.id'))

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
