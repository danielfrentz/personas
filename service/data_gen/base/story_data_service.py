from typing import List

import pandas as pd

from service.persona_domain.persona_service import PersonaService
from service.persona_domain.story_service import StoryService


class StoryDataService:
    conversation_text = "This is a story in which I was the main character {story_text}"
    def __init__(self, persona_service: PersonaService, story_service: StoryService):
        self.persona_service = persona_service
        self.story_service = story_service

    def generate(self, persona_id: int) -> List:
        result = pd.DataFrame(columns=["story_id", "title", "description"])
        persona = self.persona_service.find_by_id(persona_id)
        for event in persona.life_events:
            story = event.story
            if story is not None:
                row = pd.Series()
                row['story_id'] = story.id
                row['title'] = story.title
                row['lead_up'] = story.lead_up
                row['story text'] = story.story
                row['outcome'] = story.outcome
                row['life event'] = event.title
                result = result.append(row, ignore_index=True)
        return result
