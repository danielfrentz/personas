import logging
import random
from typing import Dict, List

from converter.conversation_converter import ConversationConverter
from converter.reasoning_conversation_converter import ReasoningConversationConverter
from dao.conversation_dao import ConversationDAO
from dao.reasoning_conversation_dao import ReasoningConversationDAO
from entity.base import ReasoningConversationEntity
from models.ai.input.reasoning_conversation_input import ReasoningConversationInput, ReasoningProblemInput
from models.ai.input.reasoning_participant import ReasoningParticipant
from models.ai.output.conversation_ai import ConversationAI
from models.ai.output.reasoning_flow_ai import ReasoningFlowAI
from models.ai.output.reasoning_problem_ai import ReasoningProblemStatementAI
from models.backstory import Backstory
from models.http.request.reasoning import ReasoningRequest
from models.reasoning_conversation import ReasoningFlowInput, ReasoningConversation
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.conversation_service import ConversationService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.universe_service import UniverseService

logger = logging.getLogger(__name__)

class ReasoningConversationService:
    def __init__(self, reasoning_dao: ReasoningConversationDAO,
                 reasoning_converter: ReasoningConversationConverter,
                 ai_service: AIService,
                 persona_service: PersonaService,
                 backstory_service: BackstoryService,
                 conversation_dao: ConversationDAO,
                 conversation_converter: ConversationConverter,
                 universe_service: UniverseService,
                 conversation_service: ConversationService,):
        self.reasoning_dao = reasoning_dao
        self.reasoning_converter = reasoning_converter
        self.ai_service = ai_service
        self.persona_service = persona_service
        self.backstory_service = backstory_service
        self.conversation_dao = conversation_dao
        self.conversation_converter = conversation_converter
        self.universe_service = universe_service
        self.conversation_service = conversation_service

    def generate(self, persona_id: int, universe_id: int, reasoning_request: ReasoningRequest) -> ReasoningConversation:
        presenter_backstory = self.backstory_service.find_by_persona_id(persona_id)
        previous_problems = [statement.problem_statement for statement in self.find_previous(theme=reasoning_request.theme)]
        logger.info(f"Passing in {len(previous_problems)} previous problems")
        if reasoning_request.prompt is None:
            problem_statement = self.get_reasoning_problem_statement(presenter_backstory=presenter_backstory, universe_id=universe_id, previous_problems=previous_problems, theme=reasoning_request.theme)
        else:
            problem_statement = ReasoningProblemStatementAI(
                problem_statement=reasoning_request.prompt,
                problem_solution=reasoning_request.solution
            )

        personas = self.persona_service.find_by_universe(universe_id)
        random.shuffle(personas)
        possible_participants: Dict[str, ReasoningParticipant] = {}
        for possible_participant in personas[:5]:
            if not possible_participant.id == persona_id:
                possible_participants[possible_participant.name] = ReasoningParticipant(
                    name=possible_participant.name,
                    group_reasoning_style=possible_participant.group_reasoning_profile,
                    description=possible_participant.backstory.description,
                    speech_profile=possible_participant.speech_profile
                )
                print(f"got the following possible {possible_participant}")

        problem_flow = self.get_problem_flow(presenter_backstory=presenter_backstory, problem=problem_statement,
                                             possible_participants=possible_participants, universe_id=universe_id,
                                             answer_expectation=reasoning_request.answer_expectation, error_made=reasoning_request.error_made)


        participants = {}
        for participant_name in problem_flow.persona_roles:
            persona = self.persona_service.find_by_name(participant_name.name)
            participants[persona.name] = ReasoningParticipant(
                name=persona.name,
                group_reasoning_style=persona.group_reasoning_profile,
                description=persona.backstory.description,
                speech_profile=persona.speech_profile
            )
        generated_dialogue = self.get_reasoning_conversation(problem_flow=problem_flow, participants=participants, universe_id=universe_id, problem=problem_statement)
        dialogue = self.conversation_converter.ai_to_model(generated_dialogue)
        return self.reasoning_converter.ai_to_model(dialogue, problem_statement=problem_statement.problem_statement, persona_id=persona_id, theme=reasoning_request.theme)

    def get_reasoning_problem_statement(self, presenter_backstory: Backstory, universe_id: int, previous_problems: List[str], theme: str) -> ReasoningProblemStatementAI:
        universe_description = self.universe_service.find_by_id(universe_id).description.description
        reasoning_problem_input = ReasoningProblemInput(
            problem_presenter=presenter_backstory,
            previous_problems=previous_problems,
            theme=theme,
            universe_description=universe_description
        )
        return self.ai_service.call_llm(system_prompt_name="create_reasoning_problem_statement", return_type=ReasoningProblemStatementAI, user_data=reasoning_problem_input,
                                        universe_id=universe_id, validator=self.validate_problem_statement(reasoning_problem_input))

    def validate_problem_statement(self, problem_statement_input: ReasoningProblemInput):
        def validate(problem_statement: ReasoningProblemStatementAI):
            if problem_statement.problem_statement in problem_statement_input.previous_problems:
                raise ValueError(f"The problem statement {problem_statement.problem_statement} has already been used, choose another one that has not been used.")
        return validate

    def get_problem_flow(self, presenter_backstory: Backstory, error_made: bool, problem: ReasoningProblemStatementAI, possible_participants: Dict[str, ReasoningParticipant], universe_id: int, answer_expectation: str) -> ReasoningFlowAI:
        problem_flow_input: ReasoningFlowInput = ReasoningFlowInput(
            problem_presenter=presenter_backstory,
            topic=problem.problem_statement,
            possible_participants=possible_participants,
            answer_expectation=answer_expectation,
            error_made=error_made,
            problem_statement=problem.problem_statement,
            solution=problem.problem_solution
        )
        return self.ai_service.call_llm(system_prompt_name="create_reasoning_flow", return_type=ReasoningFlowAI,
                                        user_data=problem_flow_input, universe_id=universe_id)


    def get_reasoning_conversation(self, problem_flow: ReasoningFlowAI, participants: Dict[str, ReasoningParticipant],
                                   universe_id: int, problem: ReasoningProblemStatementAI) -> ConversationAI:
        reasoning_dialogue_input = ReasoningConversationInput(
            conversation_flow=problem_flow,
            participants=participants,
            problem_statement=problem
        )
        return self.ai_service.call_llm("create_reasoning_conversation", return_type=ConversationAI,
                                        user_data=reasoning_dialogue_input, universe_id=universe_id)

    def save(self, reasoning_conversation: ReasoningConversation) -> ReasoningConversation:
        reasoning_entity: ReasoningConversationEntity = self.reasoning_converter.model_to_entity(reasoning_conversation)
        reasoning_entity = self.reasoning_dao.save(reasoning_entity)
        return self.reasoning_converter.entity_to_model(reasoning_entity)

    def find_by_id(self, reasoning_conversation_id: int) -> ReasoningConversation:
        reasoning_entity: ReasoningConversationEntity = self.reasoning_dao.find_by_id(entity_id=reasoning_conversation_id)
        return self.reasoning_converter.entity_to_model(reasoning_entity=reasoning_entity)

    def find_previous(self, theme) -> List[ReasoningConversation]:
        previous_entities = self.reasoning_dao.find_previous(theme)
        return [self.reasoning_converter.entity_to_model_without_conversation(previous_entity) for previous_entity in previous_entities]

    def find_all(self) -> List[ReasoningConversation]:
        reasoning_entities = self.reasoning_dao.find_all()
        return [self.reasoning_converter.entity_to_model(reasoning_entity) for reasoning_entity in reasoning_entities]

    def find_by_persona(self, persona_id):
        reasoning_entities = self.reasoning_dao.find_by_persona(persona_id=persona_id)
        return [self.reasoning_converter.entity_to_model(reasoning_entity) for reasoning_entity in reasoning_entities]

    def delete_by_id(self, reasoning_id: int):
        self.reasoning_dao.delete(reasoning_id)


