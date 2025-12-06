import logging
from typing import List

from converter.conversation_converter import ConversationConverter
from converter.monologue_converter import MonologueConverter
from dao.conversation_dao import ConversationDAO
from dao.monologue_dao import MonologueDAO
from models.ai.input.monologue import MonologueInput
from models.ai.input.monologue_plan_input import MonologuePlanInput
from models.ai.input.monologue_prompt_input import MonologuePromptInput
from models.ai.output.monologue_ai import MonologueAI
from models.ai.output.monologue_plan_ai import MonologuePlanAI
from models.ai.output.monologue_prompt import MonologuePromptAI
from models.backstory import Backstory
from models.conversation import ConversationTurn
from models.http.request.generate.monologue import MonologuePromptRequest
from models.monologue import Monologue
from models.persona import Persona
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.speech_profile_service import SpeechProfileService


class MonologueService:
    def __init__(self,
                 ai_service: AIService,
                 backstory_service: BackstoryService,
                 speech_profile_service: SpeechProfileService,
                 monologue_converter: MonologueConverter,
                 conversation_converter: ConversationConverter,
                 conversation_dao: ConversationDAO,
                 monologue_dao: MonologueDAO,
                 persona_service: PersonaService,):
        self.ai_service = ai_service
        self.backstory_service = backstory_service
        self.speech_profile_service = speech_profile_service
        self.monologue_converter = monologue_converter
        self.conversation_converter = conversation_converter
        self.conversation_dao = conversation_dao
        self.monologue_dao = monologue_dao
        self.persona_service = persona_service
        self.logger = logging.getLogger(__name__)

    def generate(self, universe_id: int, monologue_request: MonologuePromptRequest) -> Monologue:
        speakers = [self.persona_service.find_by_id(speaker_id) for speaker_id in monologue_request.speaker_ids]
        prompter = self.persona_service.find_by_id(monologue_request.prompter_id)
        self.logger.info(f"prompt is given as {monologue_request.prompt}")
        if monologue_request.prompt is None:
            generated_monologue_prompt = self.generate_monologue_prompt(theme=monologue_request.theme,
                                                                    universe_id=universe_id, prompter_backstory=prompter.backstory,
                                                                    custom_prompt_requirements=monologue_request.custom_prompt_requirements,
                                                                        intent=monologue_request.intent, prompt_type=monologue_request.prompt_type)
        else:
            generated_monologue_prompt = MonologuePromptAI(
                prompt_text=monologue_request.prompt
            )
        generated_monologue_plan = self.generate_monologue_plan(prompt=generated_monologue_prompt, speakers=speakers, prompter=prompter, universe_id=universe_id, make_mistake=monologue_request.make_mistake, custom_instructions=monologue_request.custom_instructions, intent=monologue_request.intent, include_examples=monologue_request.include_examples, include_counter_examples=monologue_request.include_counter_examples, solution=monologue_request.solution, disagreement=monologue_request.disagreement, problem_type=monologue_request.prompt_type, minimum_turns=monologue_request.minimum_turns)

        generated_monologue = self.generate_monologue(prompt=generated_monologue_prompt, monologue_plan=generated_monologue_plan, universe_id=universe_id, speakers=speakers, theme=monologue_request.theme, custom_instructions=monologue_request.custom_instructions, problem_type=monologue_request.prompt_type, minimum_turns=monologue_request.minimum_turns)
        for idx, turn in enumerate(generated_monologue.conversation.conversation_turns):
            turn.placement = idx
            turn.directed_at = [prompter.backstory.name]
        generated_monologue.speaker_id = monologue_request.speaker_ids[0]
        generated_monologue.prompter_id = prompter.id
        first_prompt = ConversationTurn(
            speaker=prompter.backstory.name,
            action="asking a question",
            tone="Curious",
            directed_at=[speaker.backstory.name for speaker in speakers],
            text=generated_monologue_prompt.prompt_text,
            feeling="Curious"
        )
        generated_monologue.conversation.conversation_turns.insert(0, first_prompt)
        generated_monologue.trigger_word = monologue_request.trigger_word
        return generated_monologue

    def generate_monologue_prompt(self,
                                  theme: str,
                                  prompter_backstory: Backstory,
                                  universe_id, custom_prompt_requirements: List[str],
                                  intent: str,
                                  prompt_type: str):

        previous_prompts = self.find_by_theme(theme)
        monologue_prompt_input = MonologuePromptInput(
            theme = theme,
            previous_prompts=previous_prompts,
            backstory=prompter_backstory,
            custom_prompt_requirements=custom_prompt_requirements,
            intent=intent,
            prompt_type=prompt_type
        )

        generated_monologue_prompt: MonologuePromptAI = self.ai_service.call_llm("create_monologue_prompt",
                                                                                 MonologuePromptAI,
                                                                                 monologue_prompt_input,
                                                                                 universe_id = universe_id,
                                                                                 validator=self.validate_prompt(previous_prompts=previous_prompts))
        return generated_monologue_prompt

    def generate_monologue_plan(self, prompt: MonologuePromptAI,
                                custom_instructions: List[str],
                                speakers: List[Persona],
                                prompter: Persona,
                                make_mistake: bool,
                                universe_id: int,
                                intent: str,
                                include_examples: bool,
                                include_counter_examples: bool,
                                solution=None,
                                disagreement=False,
                                problem_type=None,
                                minimum_turns=5):
        user_data = MonologuePlanInput(prompt=prompt,
                                       solution=solution,
                                       responders=speakers,
                                       prompter=prompter,
                                       intent=intent,
                                       custom_instructions=custom_instructions,
                                       make_mistake=make_mistake,
                                       include_examples=include_examples,
                                       include_counter_examples=include_counter_examples,
                                       disagreement=disagreement,
                                       problem_type=problem_type,
                                       minimum_turns=minimum_turns
                                       )
        generated_plan =  self.ai_service.call_llm(system_prompt_name="create_monologue_plan",
                                                   return_type=MonologuePlanAI,
                                                   user_data=user_data,
                                                   universe_id=universe_id,
                                                   validator=self.validate_plan(plan_input=user_data))
        return generated_plan

    def validate_prompt(self, previous_prompts: List[str]):
        def validate(prompt_ai: MonologuePromptAI):
            if prompt_ai.prompt_text in previous_prompts:
                raise ValueError(f"Prompt must be unique")
        return validate

    def validate_plan(self, plan_input: MonologuePlanInput):
        def validate(plan_ai: MonologuePlanAI):
            if len(plan_ai.conversation_steps) < plan_input.minimum_turns - 2:
                raise ValueError(f"Plan must have at least {plan_input.minimum_turns} steps but has {len(plan_ai.conversation_steps)}")
        return validate

    def generate_monologue(self, prompt: MonologuePromptAI,
                           monologue_plan: MonologuePlanAI,
                           speakers: List[Persona],
                           theme: str, universe_id: int,
                           custom_instructions: List[str],
                           problem_type: str,
                           minimum_turns: int) -> Monologue:
        monologue_input = MonologueInput(
            prompt=prompt.prompt_text,
            monologue_plan=monologue_plan,
            speakers=speakers,
            custom_instructions=custom_instructions,
            problem_type=problem_type,
            minimum_turns=minimum_turns
        )

        generated_monologue = self.ai_service.call_llm(system_prompt_name="create_monologue", return_type=MonologueAI, user_data=monologue_input, universe_id=universe_id, validator=self.validate_monologue(monologue_input, minimum_turns))
        result = self.monologue_converter.ai_to_model(generated_monologue=generated_monologue, monologue_input=monologue_input, theme=theme)
        return result

    def save(self, monologue: Monologue) -> Monologue:
        monologue_entity = self.monologue_converter.model_to_entity(monologue)
        monologue_entity.conversation.source_id = 1
        monologue_entity = self.monologue_dao.save(monologue_entity)
        return self.monologue_converter.entity_to_model(monologue_entity)

    def validate_monologue(self, monologue_input: MonologueInput, minimum_turns: int = 5):
        def validate(monologue: MonologueAI):
            for conversation_turn in monologue.conversation.conversation_turns:
                if len([speaker for speaker in monologue_input.speakers if speaker.backstory.name == conversation_turn.speaker.lower()]) == 0:
                    raise ValueError(
                        f"The speakers name must always be one of {[s.backstory.name for s in monologue_input.speakers]} as these are the people speaking.")
            if len(monologue.conversation.conversation_turns) < minimum_turns - 2:
                raise ValueError(f"Monologue must have at least {minimum_turns} turns but has {len(monologue.conversation.conversation_turns)}")

        return validate

    def find_by_id(self, initial_monologue_id) -> Monologue:
        monologue_entity = self.monologue_dao.find_by_id(entity_id=initial_monologue_id)
        return self.monologue_converter.entity_to_model(monologue_entity=monologue_entity)

    def find_by_theme(self, theme) -> List[str]:
        monologue_entities = self.monologue_dao.find_by_theme(theme=theme)
        return [monologue.prompt for monologue in monologue_entities]

    def find_by_speaker_id(self, speaker_id: int) -> List[Monologue]:
        result = []
        monologue_entities = self.monologue_dao.find_by_speaker_id(speaker_id)
        for monologue in monologue_entities:
            result.append(self.find_by_id(monologue.id))
        return result

    def delete(self, monologue_id: int):
        self.monologue_dao.delete(monologue_id)

    def search(self, persona_id, themes):
        monologue_entities = self.monologue_dao.search(persona_id=persona_id, themes=themes)
        return [self.monologue_converter.entity_to_model(monologue_entity) for monologue_entity in monologue_entities]
