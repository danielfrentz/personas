from typing import List

from models.conversation import Conversation
from models.conversation_turn import ConversationTurn
from service.persona_domain.persona_service import PersonaService


#[{
#     "speaker": persona_name,
#     "action": "Speaking of how I argue.",
#     "tone": ["Calm"],
#     "text": f"When I am reasoning in a group, do I tend to be sarcastic? i think {group_reasoning['sarcastic']}. as for being a devils advocate? {group_reasoning['devils_advocate']}. when asked if im witty people generally say {group_reasoning['witty']}",
#     "directed_at": ["everyone"]
# }]

class ReasoningStyleDataService:
    conversation_text = "When I am reasoning in a group, do I tend to be sarcastic? i think {sarcastic}. as for being a devils advocate? {devils_advocate}. when asked if im witty people generally say {witty}"
    def __init__(self, persona_service: PersonaService):
        self.persona_service = persona_service

    def generate(self, persona_id: int) -> List[Conversation]:
        persona = self.persona_service.find_by_id(persona_id)
        style = persona.group_reasoning_profile
        turn = ConversationTurn(
            speaker=persona.backstory.name,
            action="Explaining how I behave in a group problem scenario",
            text=ReasoningStyleDataService.conversation_text.format(sarcastic=style.sarcastic, witty=style.witty, devils_advocate=style.devils_advocate),
            directed_at=["everyone"],
            tone=["Calm"]
        )
        return [Conversation(conversation_turns=[turn])]