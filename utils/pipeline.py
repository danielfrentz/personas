import logging
from json import dumps, loads

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

import json
import random
import time
from typing import List

import requests

from models.persona import Persona
from models.universe import Universe

host = "http://localhost:8000"


def get_life_events(universe_id, persona_id):
    life_events = requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/")
    return life_events.json()

def get_universe_by_name(name: str):
    universes = requests.get(
        f"{host}/rest/universe/").json()
    for universe in universes:
        if name == universe['name']:
            return universe
    return None

def add_story(universe_id: int, persona_id: int, life_event_id: int, memory_count: int):
    generated_story = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/")
    story = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/", generated_story).json()
    logger.info(f"Added story: {story}")
    story_id = story['id']
    add_conversation(story_id=story_id,
                     persona_id=persona_id,
                     life_event_id=life_event_id,
                     universe_id=universe_id,
                     memory_count=memory_count)
    return story

def get_introspections_by_story(universe_id: int, persona_id: int, story_id: int, life_event_id: int):
    introspections = requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/introspection/")
    return introspections

def add_introspections(universe_id: int, persona_id: int, life_event_id: int, story_id: int):
    aspects = get_aspects(universe_id=universe_id, persona_id=persona_id)
    introspections = get_introspections_by_story(story_id=story_id, universe_id=universe_id, persona_id=persona_id, life_event_id=life_event_id)
    for aspect in aspects:
        if aspect['id'] not in [introspection['aspect_id'] for introspection in introspections.json()]:
            generated_introspection = add_introspection(universe_id=universe_id, persona_id=persona_id, life_event_id=life_event_id, story_id=story_id, aspect_id=aspect['id'])
            logger.info(f"generated introspection: {generated_introspection}")

def add_introspection(universe_id: int, persona_id: int, life_event_id: int, story_id: int, aspect_id: int):
    introspection_payload = {
        "aspect_id": aspect_id
    }
    introspection = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/introspection/", json.dumps(introspection_payload))
    logger.info(f"Generated introspection: {json.dumps(introspection.json())}")
    saved_introspection = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/introspection/",
        introspection).json()
    return saved_introspection


def add_conversation(universe_id: int, persona_id: int, life_event_id, story_id: int, memory_count: int) -> int:
    conversation = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/conversation/")
    saved_conversation = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/conversation/",
        conversation)
    logger.info(f"Saved conversation: {dumps(saved_conversation.json())}")
    conversation_id = saved_conversation.json()['id']
    add_memories(universe_id=universe_id, persona_id=persona_id, life_event_id=life_event_id, story_id=story_id,
                 conversation_id=conversation_id, max_memory_count=memory_count)
    add_introspections(universe_id=universe_id, persona_id=persona_id, story_id=story_id, life_event_id=life_event_id)
    return saved_conversation.json()['id']


def add_memory(universe_id: int, persona_id: int, life_event_id, story_id: int, conversation_id: int) -> int:
    memory = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/conversation/{conversation_id}/memory/")
    memory = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/conversation/{conversation_id}/memory/",
        memory)
    logger.info(f"Saved memory: {dumps(memory.json())}")
    return memory.json()['id']


def add_memories(universe_id: int, persona_id: int, life_event_id, story_id: int, conversation_id: int,
                 max_memory_count: int):
    while True:
        story = requests.get(
            f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/").json()
        if len(story['memories']) >= max_memory_count:
            logger.info(f"Memory limit reached for story {story_id}")
            return
        else:
            add_memory(universe_id=universe_id, persona_id=persona_id, life_event_id=life_event_id, story_id=story_id,
                       conversation_id=conversation_id)


def add_life_event(universe_id, persona_id, memory_count, maximum_life_events=0, context:str=None, title: str=None, date: str = None,):
    if maximum_life_events != 0 and len(
            get_life_events(universe_id=universe_id, persona_id=persona_id)) >= maximum_life_events:
        return
    logger.info(
        f"adding life event for persona {persona_id} in universe {universe_id} with memory count {memory_count}")
    start_time = time.time()
    generate_life_event_payload = {
        "context": context,
        "title": title,
        "date": date
    }
    life_event = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/life_events/", json.dumps(generate_life_event_payload))
    life_event = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/", life_event)
    life_event_id = life_event.json()['id']
    logger.info(f"Added life event: {dumps(life_event.json())}")

    add_story(universe_id=universe_id, persona_id=persona_id, life_event_id=life_event_id, memory_count=memory_count)
    logger.info(f"Time taken to add life event: {time.time() - start_time}")


def create_self_description_conversations(personas, universe_id: int, topics: List[str]):
    for persona in personas:
        persona_id = persona['id']
        existing_self_descriptions = requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/self_description_conversation/").json()
        for topic in topics:
            if not topic in [existing_self_description['topic'] for existing_self_description in existing_self_descriptions]:
                prompter_id = random.choice(personas)['id']
                create_self_description_conversation(prompter_id=prompter_id, responder_id=persona_id, topic=topic, universe_id=universe_id)

def create_self_description_conversation(prompter_id: int, responder_id: int, topic: str, universe_id: int):
    generate_payload = {
    "prompter_id":prompter_id,
    "persona_id":responder_id,
    "topic":topic
    }
    response = requests.post(f"{host}/generate/universe/{universe_id}/persona/{responder_id}/self_description_conversation/", json.dumps(generate_payload)).json()
    saved_response = requests.post(f"{host}/rest/universe/{universe_id}/persona/{responder_id}/self_description_conversation/", json.dumps(response)).json()
    logger.info(
    f"created self description conversation {dumps(saved_response)} for persona {responder_id} in universe {universe_id} with topic {topic}")


def create_monologue(universe_id, theme, intent, speaker_ids: List[int],
                     presenter_id,
                     custom_instructions: List[str],
                     custom_prompt_requirements: List[str], prompt=None,
                     include_counter_examples: bool = False,
                     include_examples: bool = False,
                     solution=None,
                     make_mistake: bool = False,
                     disagreement=False,
                     prompt_type: str = "problem",
                     minimum_turns: int = 5,
                     trigger_word: str = None):
    start_time = time.time()
    monologue_input = {
        "theme": theme,
        "intent": intent,
        "prompt": prompt,
        "include_counter_examples": include_counter_examples,
        "include_examples": include_examples,
        "speaker_ids": speaker_ids,
        "prompter_id": presenter_id,
        "custom_instructions": custom_instructions,
        "custom_prompt_requirements": custom_prompt_requirements,
        "make_mistake": make_mistake,
        "solution": solution,
        "disagreement": disagreement,
        "prompt_type": prompt_type,
        "minimum_turns": minimum_turns,
        "trigger_word": trigger_word
    }
    logger.info(f"using request {monologue_input}")
    monologue = requests.post(f"{host}/generate/universe/{universe_id}/monologue/", json.dumps(monologue_input))
    saved_conversation = requests.post(f"{host}/rest/universe/{universe_id}/monologue/", monologue)
    logger.info(f"created monologue {dumps(saved_conversation.json())} in {time.time() - start_time} seconds")


def create_reasoning(universe_id, error_made: bool, answer_expectation: str, theme: str, presenter_id: int,
                     prompt: str = None, solution: str = None):
    logger.info(f"creating a reasoning with presenter {presenter_id} on theme {theme}")
    if prompt is not None:
        logger.info(f"using prompt {prompt}")
    if solution is not None:
        logger.info(f"using solution {solution}")
    reasoning_payload = {
        "theme": theme,
        "prompt": prompt,
        "solution": solution,
        "answer_expectation": answer_expectation,
        "error_made": error_made
    }
    persona_id = presenter_id
    start_time = time.time()
    reasoning_conversation = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/reasoning/",
                                           json.dumps(reasoning_payload))
    logger.info(f"completed reasoning in {time.time() - start_time} seconds")
    logger.info(reasoning_conversation.status_code)
    logger.info(reasoning_conversation.json())
    reasoning_conversation_saved = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/reasoning/",
                                                 reasoning_conversation)
    logger.info("saved reasoning")
    logger.info(reasoning_conversation_saved.json())


def get_personas(universe_id: int):
    personas = requests.get(f"{host}/rest/universe/{universe_id}/persona/").json()
    return personas

def get_persona_by_name(universe_id: int, persona_name: str):
    personas = get_personas(universe_id=universe_id)
    for persona in personas:
        if persona['backstory'] and persona['backstory']['name'] == persona_name:
            return persona
    return None

def create_physical_description(universe_id: int, persona_id: int):
    logger.info(f"creating physical description for persona {persona_id}")
    physical_description = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/physical_description/").json()
    saved_physical_description = requests.put(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/physical_description/", dumps(physical_description)).json()
    logger.info(f"saved physical description {dumps(saved_physical_description)}")
    return saved_physical_description

def create_backstory(universe_id: int, persona_id: int, persona_payload):
    logger.info(f"creating backstory for persona {persona_id}")
    backstory = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/backstory/",
                              json.dumps(persona_payload)).json()
    saved_backstory = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/", dumps(backstory)).json()
    logger.info(f"saved backstory {dumps(saved_backstory)}")
    return backstory

def create_speech_profile(universe_id: int, persona_id: int, speech_profile_payload):
    speech_profile = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/speech_profile/",
                                   json.dumps(speech_profile_payload))
    saved_speech_profile = requests.put(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/speech_profile/",
                                        speech_profile).json()
    logger.info(f"saved speech profile {dumps(saved_speech_profile)}")
    return saved_speech_profile

def create_reasoning_profile(universe_id: int, persona_id: int):
    logger.info(f"creating reasoning profile for persona {persona_id}")
    reasoning_style = requests.post(
        f"http://localhost:8000/generate/universe/{universe_id}/persona/{persona_id}/reasoning_style/")
    saved_reasoning_style = requests.post(
        f"http://localhost:8000/rest/universe/{universe_id}/persona/{persona_id}/reasoning_style/", reasoning_style).json()
    logger.info(f"reasoning style saved {dumps(saved_reasoning_style)}")
    return saved_reasoning_style

def create_persona(universe_id: int, persona_payload):
    logger.info(f"creating persona {persona_payload}")
    persona_response = requests.post(f"{host}/rest/universe/{universe_id}/persona/", json.dumps(persona_payload)).json()
    add_persona_basics(universe_id=universe_id, persona_payload=persona_payload, speech_profile_payload=persona_payload,persona_id=persona_response['id'])
    logger.info(f"created persona {dumps(persona_response)}")

    return persona_response

def add_persona_basics(universe_id: int, persona_payload, speech_profile_payload, persona_id: int):
    logger.info(f"adding persona basics for persona {persona_id}")
    persona_response = requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/").json()
    if persona_response['backstory'] is None:
        persona_response['backstory'] = create_backstory(universe_id=universe_id, persona_id=persona_id, persona_payload=persona_payload)
    if persona_response['physical_description'] is None:
        create_physical_description(universe_id=universe_id, persona_id=persona_id)
    if persona_response['speech_profile'] is None:
        persona_response['speech_profile'] = create_speech_profile(universe_id=universe_id, persona_id=persona_id, speech_profile_payload=speech_profile_payload)
    if persona_response['group_reasoning_profile'] is None:
        create_reasoning_profile(universe_id=universe_id, persona_id=persona_id)
    return requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/").json()


def add_persona_speech_sample(universe_id: int, persona_id: int):
    logger.info(f"adding speech sample for persona {persona_id}")
    speech_sample = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/speech_profile/sample/")
    saved_speech_sample = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/speech_profile/sample/", speech_sample)
    logger.info(f"speech sample saved {saved_speech_sample.json()['id']}")


def add_persona_speech_samples(universe_id: int, persona_id: int, speech_sample_count: int):
    logger.info(f"adding speech samples for persona {persona_id}")
    current_speech_sample_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/speech_profile/sample/").json())
    if current_speech_sample_count < speech_sample_count:
        for i in range(speech_sample_count - current_speech_sample_count):
            add_persona_speech_sample(universe_id, persona_id)
        logger.info(
            f"Finished adding speech samples for persona {persona_id}, added a total of {speech_sample_count - current_speech_sample_count} speech samples")

def delete_persona_speech_samples(universe_id: int, persona_id: int):
    requests.delete(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/speech_profile/sample/").json()

def add_persona_habit(universe_id: int, persona_id: int):
    logger.info(f"adding habit for persona {persona_id}")
    habit = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/backstory/habit/")
    saved_habit = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/habit/", habit)
    logger.info(f"habit saved: {dumps(saved_habit.json())}")


def add_persona_habits(universe_id: int, persona_id: int, habit_count: int):
    logger.info(f"adding habits for persona {persona_id}")
    current_habit_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/habit/").json())
    if current_habit_count < habit_count:
        for i in range(habit_count - current_habit_count):
            add_persona_habit(universe_id, persona_id)
        logger.info(
            f"Finished adding habits for persona {persona_id}, added a total of {habit_count - current_habit_count} habits")


def add_persona_like(universe_id: int, persona_id: int):
    logger.info(f"adding like for persona {persona_id}")
    like = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/backstory/like/")
    saved_like = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/like/", like)
    logger.info(f"like saved: {dumps(saved_like.json())}")


def add_persona_likes(universe_id: int, persona_id: int, like_count: int):
    logger.info(f"adding likes for persona {persona_id}")
    current_like_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/like/").json())
    if current_like_count < like_count:
        for i in range(like_count - current_like_count):
            add_persona_like(universe_id=universe_id, persona_id=persona_id)
        logger.info(
            f"Finished adding likes for persona {persona_id}, added a total of {like_count - current_like_count} likes")


def add_persona_hobby(universe_id: int, persona_id: int):
    logger.info(f"adding hobby for persona {persona_id}")
    hobby = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/backstory/hobby/")
    saved_hobby = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/hobby/", hobby)
    logger.info(f"hobby saved: {dumps(saved_hobby.json())}")

def add_persona_hobbies(universe_id: int, persona_id: int, hobby_count: int):
    logger.info(f"adding hobbies for persona {persona_id}")
    current_hobby_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/hobby/").json())
    if current_hobby_count < hobby_count:
        for i in range(hobby_count - current_hobby_count):
            add_persona_hobby(universe_id=universe_id, persona_id=persona_id)
        logger.info(f"Finished adding hobbies for persona {persona_id}, added a total of {hobby_count - current_hobby_count} hobbies")


def add_accessory(universe_id: int, persona_id: int):
    logger.info(f"adding accessory for persona {persona_id}")
    accessory = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/physical_description/accessory/")
    saved_accessory = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/physical_description/accessory/",
        accessory)
    logger.info(f"accessory saved: {dumps(saved_accessory.json())}")


def add_accessories(universe_id: int, persona_id: int, accessory_count: int):
    logger.info(f"adding accessories for persona {persona_id}")
    current_accessory_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/physical_description/accessory/").json())
    if current_accessory_count < accessory_count:
        for i in range(accessory_count - current_accessory_count):
            add_accessory(universe_id, persona_id)
    logger.info(
        f"Finished adding accessories for persona {persona_id}, added a total of {accessory_count - current_accessory_count} accessories")

def add_hair_style(universe_id: int, persona_id: int):
    logger.info(f"adding hair style for persona {persona_id}")
    hair_style = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/physical_description/hair_style/")
    saved_hair_style = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/physical_description/hair_style/",
        hair_style)
    logger.info(f"hairstyle saved: {dumps(saved_hair_style.json())}")

def add_hair_styles(universe_id: int, persona_id: int, count: int):
    logger.info(f"adding hair styles for persona {persona_id}")
    current_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/physical_description/hair_style/").json())
    if current_count < count:
        for i in range(count - current_count):
            add_hair_style(universe_id, persona_id)
    logger.info(
        f"Finished adding hairstyles for persona {persona_id}, added a total of {count - current_count} accessories")

def add_clothing(universe_id: int, persona_id: int):
    logger.info(f"adding clothing for persona {persona_id}")
    clothing = requests.post(
        f"{host}/generate/universe/{universe_id}/persona/{persona_id}/physical_description/clothing/")
    saved_clothing = requests.post(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/physical_description/clothing/",
        clothing)
    logger.info(f"added clothing {saved_clothing.json()} saved")


def add_hobby(universe_id: int, persona_id: int):
    logger.info(f"adding hobby for persona {persona_id}")
    hobby = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/backstory/hobby/")
    saved_hobby = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/hobby/", hobby)
    logger.info(f"hobby {saved_hobby.json()['id']} saved")


def add_hobbies(universe_id, persona_id, hobby_count):
    logger.info(f"adding hobbies for persona {persona_id}")
    current_hobby_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/hobby/").json())
    if current_hobby_count < hobby_count:
        for i in range(hobby_count - current_hobby_count):
            add_hobby(universe_id, persona_id)
    logger.info(
        f"Finished adding hobbies for persona {persona_id}, added a total of {hobby_count - current_hobby_count} hobbies")


def add_fact(universe_id: int, persona_id: int):
    logger.info(f"adding fact for persona {persona_id}")
    fact = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/fact/")
    saved_fact = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/fact/", fact)
    logger.info(f"fact {saved_fact.json()} saved")


def add_facts(universe_id, persona_id, fact_count):
    logger.info(f"adding fact for persona {persona_id}")
    current_fact_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/fact/").json())
    if current_fact_count < fact_count:
        for i in range(fact_count - current_fact_count):
            add_fact(universe_id, persona_id)
    logger.info(
        f"Finished adding facts for persona {persona_id}, added a total of {fact_count - current_fact_count} hobbies")


def get_aspects(universe_id: int, persona_id: int):
    logger.info(f"getting aspects for persona {persona_id}")
    existing_aspects = requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/aspect/").json()
    return existing_aspects

def add_aspect(universe_id: int, persona_id: int, aspect: str):
    logger.info(f"adding aspect {aspect} for persona id {persona_id}")
    aspect_payload = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/backstory/aspect/",
                                   json.dumps({"aspect_name": aspect}))
    logger.info(f"generated {aspect_payload.json()} for aspect {aspect}")
    saved_aspect = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/aspect/", aspect_payload)
    logger.info(f"aspect {saved_aspect.json()} saved")


def add_aspects(universe_id: int, persona_id: int, aspects: List[str]):
    logger.info(f"adding aspects for persona {persona_id}")
    current_aspects = requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/backstory/aspect/").json()
    current_aspect_types = [aspect['aspect_name'] for aspect in current_aspects]
    for aspect in aspects:
        if aspect not in current_aspect_types:
            add_aspect(universe_id=universe_id, persona_id=persona_id, aspect=aspect)
    logger.info(f"Finished adding aspects for persona {persona_id}")


def add_clothes(universe_id: int, persona_id: int, clothing_count: int):
    logger.info(f"adding clothings for persona {persona_id}")
    current_clothing = requests.get(
        f"{host}/rest/universe/{universe_id}/persona/{persona_id}/physical_description/clothing/").json()
    current_clothing_count = len(current_clothing)
    if current_clothing_count < clothing_count:
        for i in range(clothing_count - current_clothing_count):
            add_clothing(universe_id, persona_id)
    logger.info(
        f"Finished adding clothes for persona {persona_id}, added a total of {clothing_count - current_clothing_count} clothes")


def create_universe(universe_payload: dict, universe_enhance_count: int) -> int:
    logger.info(f"creating universe {universe_payload}")
    universe = requests.post(f"{host}/rest/universe/", json.dumps(universe_payload)).json()
    universe_id = universe['id']
    for i in range(universe_enhance_count):
        enhanced_universe_description = requests.post(
            f"http://localhost:8000/generate/universe/{universe_id}/description/").json()
        universe = requests.put(f"http://localhost:8000/rest/universe/{universe_id}/description/",
                                               dumps(enhanced_universe_description)).json()
        logger.info(f"enhanced universe description saved {dumps(universe)}")
    return universe


def create_universe_location(universe_id: int):
    logger.info(f"creating universe location for persona {universe_id}")
    location = requests.post(f"{host}/generate/universe/{universe_id}/location/")
    saved_location = requests.post(f"{host}/rest/universe/{universe_id}/location/", location)
    logger.info(f"location {saved_location.json()} created")


def create_universe_locations(universe_id: int, location_count: int):
    for i in range(location_count):
        create_universe_location(universe_id)


def add_life_events(universe_id, persona_id, life_event_count, memory_count, context=None, title=None):
    logger.info(f"adding life events for persona {persona_id}")
    current_life_event_count = len(
        requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/").json())
    if current_life_event_count < life_event_count:
        try:
            for i in range(life_event_count - current_life_event_count):
                try:
                    add_life_event(universe_id=universe_id, memory_count=memory_count, persona_id=persona_id, context=context, title=title)
                except Exception as e:
                    logger.error(f"error adding life event {e}")
            logger.info(
            f"finished adding life events for persona {persona_id}, added a total of {life_event_count - current_life_event_count} life events")
        except Exception as e:
            logger.error(f"error adding life events {e}")

def update_relationships(universe_id, persona_id, target_persona_id):
    logger.info(f"updating relationships for id {persona_id}")
    payload = {
        "source_persona_id": persona_id,
        "target_persona_id": target_persona_id
    }
    relationship = requests.post(f"{host}/generate/universe/{universe_id}/persona/{persona_id}/relationship/",
                                 json.dumps(payload))
    logger.info(f"got relationship {relationship.json()}")
    logger.info(f"saving relationship {relationship}")
    relationship_response = requests.post(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/relationship/",
                                          json.dumps(relationship.json()))
    logger.info(relationship_response.json())


def update_relationships_all(universe_id: int):
    personas = get_personas(universe_id=universe_id)
    for source_persona in personas:
        for target_persona in personas:
            source_persona_id = source_persona['id']
            target_persona_id = target_persona['id']
            update_relationships(universe_id=universe_id, persona_id=source_persona_id,
                                 target_persona_id=target_persona_id)


def create_persona_details(universe_id: int,
                           persona_id: int,
                           clothing_count: int,
                           accessory_count: int,
                           like_count: int,
                           hobby_count: int,
                           habit_count: int,
                           speech_sample_count: int,
                           fact_count):
    logger.info(f"creating persona details for persona {persona_id}")
    add_persona_speech_samples(universe_id=universe_id, persona_id=persona_id,
                               speech_sample_count=speech_sample_count)
    add_persona_likes(universe_id=universe_id, persona_id=persona_id, like_count=like_count)
    add_persona_hobbies(universe_id=universe_id, persona_id=persona_id, hobby_count=hobby_count)

    add_clothes(universe_id=universe_id, persona_id=persona_id, clothing_count=clothing_count)
    add_accessories(universe_id=universe_id, persona_id=persona_id, accessory_count=accessory_count)
    add_facts(universe_id=universe_id, persona_id=persona_id, fact_count=fact_count)
    add_persona_habits(universe_id=universe_id, persona_id=persona_id, habit_count=habit_count)

def resume_life_event(life_event_id: int, universe_id: int, persona_id: int, memory_count: int):
    life_event = requests.get(f"{host}/rest/life-event/{life_event_id}/")
    if not 'story' in life_event.json():
        add_story(life_event_id=life_event_id, universe_id=universe_id, persona_id=persona_id,
                  memory_count=memory_count)


def add_universe(name, description, creatures, metadata, location_count: int):
    description = {
        "description": f"{description}",
        "creatures": creatures,
    }
    universe_payload = {'name': name, 'description': description, 'metadata': metadata, 'personas': [], 'locations': []}

    universe_id = create_universe(universe_payload, 5)
    create_universe_locations(universe_id, location_count)
    return universe_id

def add_missing_memories_all_stories(universe_id: int,
                                     persona_id: int,
                                     memory_count: int):
    life_events = requests.get(f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/").json()
    for life_event in life_events:
        logger.info(f"adding missing memories for persona {life_event['title']}")
        life_event_id = life_event['id']
        stories = requests.get(
            f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/").json()
        if len(stories) == 0:
            logger.info(f"no stories found for life event {life_event_id}, adding one")
            add_story(life_event_id=life_event_id, universe_id=universe_id, persona_id=persona_id, memory_count=memory_count)
        else:
            logger.info(f"found {len(stories)} stories for life event {life_event_id}")
        for story in stories:
            life_event_id = story['life_event_id']
            story_id = story['id']
            logger.info(f"resuming story {story_id} for life event {life_event_id}")
            conversation = requests.get(
                f"{host}/rest/universe/{universe_id}/persona/{persona_id}/life_events/{life_event_id}/story/{story_id}/conversation/").json()
            if conversation is None:
                logger.info(f"story {story_id} has no conversation, adding one")
                conversation = add_conversation(universe_id=universe_id, life_event_id=life_event_id, story_id=story_id,
                                 persona_id=persona_id, memory_count=memory_count)
            conversation_id = conversation['id']
            add_memories(universe_id=universe_id, persona_id=persona_id, story_id=story_id,
                         conversation_id=conversation_id, life_event_id=life_event_id,
                         max_memory_count=memory_count)
            add_introspections(universe_id=universe_id, persona_id=persona_id, story_id=story_id,
                              life_event_id=life_event_id)

def create_lectures(personas, universe_id: int, minimum_turns=10, lecture_type: str = ""):
    persona_ids = [persona['id'] for persona in personas]
    selected_personas = random.sample(persona_ids, k=random.randint(2, 2))
    prompter_id = selected_personas[0]
    speaker_ids = selected_personas[1:]

    while True:
        try:
            fields = ["Calculus", "probability", "algebra", "group theory", "ring theory", "integrals",
                      "differential equations", "set theory", "topology"]
            levels = ["beginner", "intermediate", "advanced"]
            theme_template = "indepth and rigorous lecture on a specific definition in {field}."
            intent_template = "To get an indepth private lecture on {field} at a {level} level of education. The conversation should introduce the topic and explain it in detail as if to a university student."
            field = random.choice(fields)
            level = random.choice(levels)
            theme = theme_template.format(field=field)
            intent = intent_template.format(field=field, level=level)
            prompt_type = "lecture"

            trigger_word = f"lecture"
            create_monologue(universe_id=universe_id,
                             theme=theme,
                             presenter_id=prompter_id,
                             speaker_ids=speaker_ids,
                             intent=intent,
                             custom_instructions=[],
                             custom_prompt_requirements=[],
                             make_mistake=random.choice([True, False]),
                             include_examples=True,
                             include_counter_examples=random.choice([True, False]),
                             disagreement=False,
                             prompt_type=prompt_type,
                             minimum_turns=minimum_turns,
                             trigger_word=trigger_word)
        except Exception as e:
            logger.info(f"error {e} occurred, skipping")

def resume_personas(personas, universe_id: int,
                    life_event_count: int,
                    memory_count: int,
                    aspects: List[str],
                    habit_count: int,
                    clothing_count: int,
                    accessory_count: int,
                    speech_sample_count: int ,
                    fact_count: int,
                    like_count: int,
                    hobby_count: int):
    for persona in personas:
        logger.info(f"resuming persona {persona['backstory']['name']}")
        persona_id = persona['id']
        try:
            add_aspects(persona_id=persona_id,
                        aspects=aspects,
                        universe_id=universe_id)
            create_persona_details(universe_id,
                                   persona_id=persona_id,
                                   speech_sample_count=speech_sample_count,
                                   fact_count=fact_count,
                                   habit_count=habit_count,
                                   accessory_count=accessory_count,
                                   clothing_count=clothing_count,
                                   like_count=like_count,
                                   hobby_count=hobby_count)
            # add_missing_memories_all_stories(universe_id=universe_id,
            #                                  persona_id=persona_id,
            #                                  memory_count=memory_count)
            add_life_events(persona_id=persona_id,
                            universe_id=universe_id,
                            memory_count=memory_count,
                            life_event_count=life_event_count)

        except Exception as e:
            logger.info(e)

    # update_relationships_all(universe_id=universe_id)

def create_unique_problem_solving(personas, universe_id):
    fields = ["Calculus", "probability", "algebra", "group theory", "ring theory", "integrals",
              "differential equations", "set theory", "topology"]
    theme = "solving a {field} problem".format(field=random.choice(fields))
    intent = "To solve a maths problem using the approaches reflective of the person solving the problem and delivering a rigorous proof"
    prompt_type = "problem"
    persona_ids = [persona['id'] for persona in personas]
    selected_personas = random.sample(persona_ids, k=random.randint(2, len(personas)))
    prompter_id = selected_personas[0]
    speaker_ids = selected_personas[1:]
    random.seed(time.time_ns())
    create_monologue(universe_id=universe_id,
                     theme=theme,
                     presenter_id=prompter_id,
                     speaker_ids=speaker_ids,
                     intent=intent,
                     custom_instructions=[],
                     custom_prompt_requirements=["Ensure that the question asked is very specific to avoid broad answers."],
                     make_mistake=random.choice([True, False]),
                     include_examples=True,
                     include_counter_examples=random.choice([True, False]),
                     disagreement=random.choice([True, False]) and len(personas) > 2,
                     prompt_type=prompt_type)
def create_problem_solving(personas, universe_id: int, problem_csv):
    persona_ids = [persona['id'] for persona in personas if persona['id'] > 0]

    while True:
        theme = "solving maths problems"
        intent = "To solve a maths problem ensuring that the solution is provided at the end."
        prompt_type = "problem"
        trigger_word = f"solve problem"
        random.seed(time.time_ns())
        try:
            df = pd.read_csv(problem_csv)
            for index, row in df.sample(frac=1, replace=False).iterrows():
                problem = row.loc["problem"]
                solution = row.loc["solution"]
                random.seed(time.time_ns())
                selected_personas = random.sample(persona_ids, k=random.randint(2, len(personas)))
                prompter_id = selected_personas[0]
                speaker_ids = selected_personas[1:]

                create_monologue(universe_id=universe_id,
                                 theme=theme,
                                 presenter_id=prompter_id,
                                 speaker_ids=speaker_ids,
                                 intent=intent,
                                 custom_instructions=[],
                                 custom_prompt_requirements=[],
                                 make_mistake=random.choice([True, False]),
                                 include_examples=True,
                                 include_counter_examples=random.choice([True, False]),
                                 disagreement=random.choice([True, False]) and len(personas) > 2,
                                 prompt_type=prompt_type,
                                 prompt=problem,
                                 solution=solution,
                                 trigger_word=trigger_word,
                                 minimum_turns=10)
        except Exception as e:
            logger.info(e)


def main(config_file):
    with open(config_file) as f:
        config = loads(f.read())
    universe = get_universe_by_name(config["universe"]["name"])
    if not universe:
        universe = create_universe(config["universe"], universe_enhance_count=config['universe']['universe_enhance_count'])
        logger.info(f"Created a new universe {dumps(universe)}")
    else:
        logger.info(f"found existing universe {universe['id']}")

    current_universe_id = universe['id']
    persona_payloads = config["personas"]
    existing_personas = get_personas(universe_id=current_universe_id)
    for persona_payload in persona_payloads:
        existing_persona = [existing for existing in existing_personas if existing['backstory']['name'] == persona_payload['name'].lower()]
        if len(existing_persona) == 0:
            logger.info(f"creating persona {persona_payload['name']}")
            persona_payload["universe_id"] = current_universe_id
            existing_persona = create_persona(universe_id=current_universe_id, persona_payload=persona_payload)
            persona_payload['persona_id'] = existing_persona['id']
        else:
            logger.info(f"persona {persona_payload['name']} already exists")
            existing_persona = existing_persona[0]
        persona_payload['persona_id'] = existing_persona['id']
        speech_profile = config["speech_profile"]
        add_persona_basics(speech_profile_payload=speech_profile, persona_payload=persona_payload, universe_id=current_universe_id, persona_id=existing_persona['id'])
    personas = get_personas(universe_id=current_universe_id)
    print([persona['id'] for persona in personas])
    resume_personas(personas,
                    life_event_count=config["life_event_count"],
                    memory_count=config["memory_count"],
                    aspects=config["persona_aspects"],
                    like_count=config["like_count"],
                    clothing_count=config["clothing_count"],
                    accessory_count=config["accessory_count"],
                    speech_sample_count=config["speech_sample_count"],
                    fact_count=config["fact_count"],
                    universe_id=current_universe_id,
                    habit_count=config["habit_count"],
                    hobby_count=config["hobby_count"])
    create_self_description_conversations(personas=personas, topics=config['self_description_topics'], universe_id=current_universe_id)
    create_problem_solving(problem_csv="math.csv", personas=personas, universe_id=current_universe_id)
    # create_lectures(personas=personas, universe_id=current_universe_id, minimum_turns=20)
    # create_lectures(personas, current_universe_id, minimum_turns=10, lecture_type="indepth lecture")

#
if __name__ == "__main__":
    config_file = "configurations/maths.json"
    main(config_file=config_file)

# delete_persona_speech_samples(universe_id=1, persona_id=1)