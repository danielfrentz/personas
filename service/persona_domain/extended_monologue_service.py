from converter.backstory_converter import BackstoryConverter
from converter.monologue_converter import MonologueConverter
from models.ai.input.extended_monologue_prompt_input import ExtendedMonologuePromptInput
from models.ai.output.extended_monologue_prompt_ai import ExtendedMonologuePromptAI
from models.ai.output.monologue_prompt import MonologuePromptAI
from service.ai.ai_service import AIService
from service.persona_domain.monologue_service import MonologueService
from service.persona_domain.persona_service import PersonaService


class ExtendedMonologueService:
    def __init__(self, ai_service: AIService,
                 monologue_converter: MonologueConverter,
                 backstory_converter: BackstoryConverter,
                 persona_service: PersonaService,
                 monologue_service: MonologueService,):
        self.ai_service = ai_service
        self.monologue_converter = monologue_converter
        self.monologue_service = monologue_service
        self.backstory_converter = backstory_converter
        self.persona_service = persona_service

    def generate(self, monologue_id: int, universe_id: int):
        previous_monologue = self.monologue_service.find_by_id(monologue_id)
        # generated_monologue = self.monologue_service.generate_monologue(prompt=prompt, universe_id=universe_id,
        #                                                                 speaker_id=previous_monologue.speaker_id,
        #                                                                 speaker_backstory=speaker_backstory,
        #                                                                 theme=previous_monologue.theme,
        #                                                                 prompter_id=previous_monologue.prompter_id,
        #                                                                 speaker_name=speaker.name,
        #                                                                 speaker_speech_profile=speaker.speech_profile,
        #                                                                 prompter_name=prompter.name
        #                                                                 )
        # return generated_monologue
        return None

    def get_prompt(self, monologue_id: int, universe_id: int) -> MonologuePromptAI:
        previous_monologue = self.monologue_service.find_by_id(monologue_id)
        extended_monologue_input = ExtendedMonologuePromptInput(
            base_monologue=previous_monologue
        )
        return self.ai_service.call_llm("create_extended_monologue_prompt", ExtendedMonologuePromptAI, extended_monologue_input, universe_id)
