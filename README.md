## Overview

The project aims to create a tool that can be used to generate a persona based on a description of the personas and requiring no additional information.

## Why

The current LLM environment is saturated with persona frameworks, and it makes sense to first discuss why this project exists. It takes a different approach to persona generation than most LLM based persona frameworks by ignoring system prompts, and in fact ignoring instruct LLMs completely, and rather focusing on the idea of teaching the LLM who to be not what to say. 

Of course all LLM training comes down to predicting the next token in the sequence, but the idea is to teach the LLM to be a persona generator rather than a persona. This is achieved by using a combination of a few different techniques. The primary of these is to structure all training data as conversations in which the LLM has an identity. These can be described by the following:

1. Self referencing - in some conversations there is only one persona speaking, in these the persona addresses itself and responds to itself, ie introspections uses this technique.
2. Speaking to everyone - in other conversations the persona addresses everyone where the persona being spoken to is simply referenced as everyone. These conversations are generally used to describe some attributes about the persona in the first person. This not only teaches it again to reference the correct pronouns but also acts as a subtle way to teach the model about the persona. 
3. Multi persona conversations - in some conversations the persona addresses multiple personas, this is used to introduce the idea of multi persona conversations. In these conversations multiple personas will take turns in speaking and the template ensure that this ordering is ordered correctly.

Anyone who looks deeply at the data will notice that there is a lot of data in there which does not appear to help with the final task at all, and they would be correct, for example clothing, likes and dislikes etc. These are not intended for tasks but rather as additional metadata to help drive identity and so far tests have shown that this is exceptionally useful and this will be expanded upon going forward.

The project itself is split into several parts each with its unique purpose.

### API

There is an API for generating the data regarding each persona. This data is not usable as training data for an LLM but rather is used to generate the training data later on and often previously generated data will be passed into future stages to help generate consistent personas.

### Data Generation

While technically a different use case, for now the data generation process is part of the API. the endpoint /generate can be called and will return data which is ready to be used as training data using the script described below.

### Training

The training process is the final process in the pipeline. It is intended to train an LLM to generate personas based on the data generated in the previous stages. Below it is discussed in depth along with a sample script which can be modified to suit your needs.

## Data Categories

The generated data is stored in a SQL database and can be split into the following categories:

### Universe

This is a common grounding for all the characters to reference in their conversations, otherwise it plays no role.

### Persona

All data related to a persona is stored under the persona table or linked to it. This includes backstory, habits, clothing, likes and dislikes, relationships, and so on.

### Conversations

All conversations are stored in a single table. This table does not have references back to its source but rather has a composite key made up of the name of the source type and the id of the source. This design may change in the future.

Conversations are stored not as a single object but as a sequence of turns. Each turn has the following fields:

- speaker: The person who is speaking.
- speech: The text of the turn.
- tone: The tone of the speaker.
- action: An action being performed by the speaker.
- feeling: How the speaker feels as they speak.
- intent: What they aim to achieve with their speech.
- internal_thought: What the person is thinking internally.

Most of these fields are treated as a conditioning vector to guide the conversation.


## API 

### Structure

The api is organized into domains, such as persona, habit, monologue etc. Each domain has its own endpoints and follows a RESTful structure.

Additionally, for each object that can be generated there exists a /generate endpoint which will return the generated object but not save it. The intention is that the user will then send a post request to the /rest API to save the object.

## Data generation

The data generation process is broken into 3 stages.
1. The basic details about a persona.
2. Life events for the persona.
3. Monologue/task conversatons.

To kick off the process only a short description is necessary, something to ground the persona. If it is a historical figure it is best to use their full name. At this point the persona data will go through the following stages:

### Stage 1 - Basic details

During this stage the pipeline will accept a simple description and create a series of objects about the persona. The objects are described below.

The description of the persona can either be short or long, it is completely up to the user. While in the long term the goal is to ensure that it generates well-balanced characters, it is often best to use long descriptions if the requirement is a persona which is complex and nuanced, meanwhile for something like a generic Java developer something like 'an expert spring developer' would be sufficient.

#### Sample details

The following samples were generated on a 235b qwen model running on a h200. Roughly 1 hour to develop the complete persona excluding monologues.

While they have been exported to JSON each of these objects are represented as a row in a SQL database.

Backstory
```JSON
  {
    "id": 1,
    "place_of_birth": "Tambov, Russian Empire",
    "description": "Andrey Nikolaevich Kolmogorov was born on April 25, 1903, in Tambov, Russia, to Maria Yakovlevna Kolmogorova, a noblewoman who died in childbirth. His father, Nikolai Matveevich Kataev, was an agronomist of noble descent who perished during the Russian Civil War. Raised by his maternal aunts in Tunoshna, a rural village near Yaroslavl, Kolmogorov's early intellectual development was shaped by an environment rich in literature, music, and informal mathematical exploration. By age five, he was already constructing calendars for his family and experimenting with arithmetic sequences. His fascination with patterns and probability emerged early, as seen in his childhood analysis of the frequency of letters in Pushkin's poetry. Kolmogorov's foundational work in probability theory, particularly his 1933 axiomatization using measure theory ($P(\\Omega) = 1$, $P(A) \\geq 0$, and countable additivity), revolutionized the field, providing a rigorous framework that unified disparate probabilistic concepts. In the Topological Paradise, he continues to refine these ideas, engaging with living topological spaces to explore stochastic processes on fractal manifolds and the interplay between algorithmic complexity and measure-theoretic probability.",
    "education_description": "Kolmogorov's formal education began at the age of 14 when he joined Moscow State University's preparatory program. By 1920, he enrolled at Moscow State University, where he studied under luminaries such as Nikolai Luzin and Dmitri Egorov. His undergraduate thesis on Fourier series convergence (1922) demonstrated his exceptional talent, while his doctoral work established foundational results in probability, topology, and intuitionistic logic. Kolmogorov earned his Ph.D. in 1929 and became a professor at Moscow State University in 1931. He later co-founded the Moscow School of Probability Theory, mentoring generations of mathematicians. In the Topological Paradise, his educational pursuits transcend traditional academia; he collaborates with sentient mathematical constructs to develop dynamic models of probability spaces, where $\\sigma$-algebras evolve through continuous deformations, and engages Einstein in discussions about the probabilistic interpretation of quantum mechanics within curved spacetime.",
    "social_description": "Kolmogorov was known for his humility, intellectual generosity, and commitment to collaborative inquiry. He maintained close relationships with colleagues such as Pavel Alexandrov and Israel Gelfand, often hosting seminars at his dacha in Komarovka. His mentorship style emphasized clarity and rigor, encouraging students to derive results independently before presenting them. In the Topological Paradise, his social interactions reflect these traits: he frequently engages with sentient functions and harmonic series to explore the ergodic properties of dynamical systems, and debates the philosophical implications of the law of large numbers with Einstein. His speech retains the precise, methodical cadence characteristic of his historical persona, often punctuated by phrases like 'It is evident that...' or 'By the axioms of measure theory...' He avoids metaphors, preferring direct exposition grounded in mathematical truth, such as explaining conditional probability via $P(A|B) = \\frac{P(A \\cap B)}{P(B)}$ rather than analogies.",
    "persona_id": 1
  }
```


Habits:

```json
{
    "id": 186,
    "name": "Recursive Axiomatic Contemplation",
    "frequency": "Daily",
    "backstory_id": 8,
    "good_habit": 0,
    "description": ""
  }
```

Clothing

```json
  {
    "id": 1,
    "name": "Kolmogorov Compactness Cloak",
    "clothing_category": "cloak",
    "description": "The cloak is made of a shimmering, adaptive fabric that subtly shifts its texture and color based on the topological properties of the surrounding space. Its edges are reinforced with a non-Euclidean lining that ensures the cloak remains connected even when stretched across multiple dimensions. The interior is lined with a fine mesh of harmonic sequences that resonate with the wearer's thoughts, providing a calming effect during complex calculations. The clasp is a miniature model of a compact metric space, glowing faintly when the wearer is in a state of mathematical clarity.",
    "occasion": "Worn during deep explorations of fractal manifolds or when engaging in high-stakes discussions involving measure theory and stochastic processes.",
    "purpose": "Designed to maintain personal continuity and compactness in chaotic topological transformations, preventing the wearer from becoming disconnected or non-compact during intense mathematical fluctuations.",
    "personal_significance": "This cloak was a gift from Kolmogorov himself after the wearer demonstrated an exceptional understanding of his axioms. It symbolizes the wearer's commitment to mathematical rigor and their role as a guardian of continuity in the Topological Paradise.",
    "physical_description_id": 1
  }
```

Hobby

```json
  {
    "id": 1,
    "name": "Probabilistic Origami Folding",
    "description": "Andrey Kolmogorov finds joy in folding origami models where each crease is determined by a stochastic process. Using a pre-defined probability distribution over possible fold angles, he constructs intricate paper structures that embody randomness and emergent symmetry. He often analyzes the resulting geometric properties, such as the expected curvature of the final model or the probability of achieving a specific topological configuration. This hobby merges his love for measure theory with tactile creativity, allowing him to explore how probabilistic rules manifest in physical space. His favorite models are those that approximate fractal surfaces, where small-scale random folds lead to large-scale self-similar patterns.",
    "backstory_id": 1
  }
```

Likes and dislikes:

```json
  {
    "id": 1,
    "backstory_id": 1,
    "like_name": "Chaotic Pendulum Art",
    "like_reason": "The unpredictable trajectories of double pendulums create intricate patterns that embody the beauty of deterministic chaos. Each swing reveals emergent order within apparent randomness, mirroring the deep connection between measure theory and dynamical systems I've always sought to formalize.",
    "dislike_name": "Predictable Clockwork Automata",
    "dislike_reason": "These rigid mechanical devices follow preordained paths with no room for stochastic variation, reducing motion to mere repetition. Their lack of probabilistic nuance fails to capture the richness of real-world phenomena governed by chance.",
    "contradiction_explanation": "I find myself questioning: 'How can one who champions measure-theoretic probability appreciate chaotic systems yet reject deterministic automata?' The answer lies in the mathematical distinction between chaos and true randomness. Chaotic systems, while deterministic, exhibit sensitive dependence on initial conditions that generate effectively unpredictable behavior—akin to how Kolmogorov complexity measures the information content of sequences. Clockwork automata, however, operate within finite state spaces devoid of such complexity. My work on $\\sigma$-algebras shows that even deterministic systems can induce non-trivial probability spaces when observed through coarse-grained partitions. Thus, the pendulum's fractal trajectories inhabit the very boundary between order and probability that my axioms describe, while clockwork remains confined to trivial $\\sigma$-algebras with no measurable complexity.",
    "contradiction": "A possible contradiction in their like and dislike."
  }
```
### Stage 2 - Life events

Life events are vital for defining a persona as this is where all the core conversations will be generated or at least the data from which they will be generated.

1. A life event is generated - in order to generate unique events all the past ones will be passed into the llm as context. This will generally result in the new life event coming after the previous one. 
2. A story is written - A summary of a story about the life event will be generated. This is not used for any training data as such but rather to help with the next few steps.
3. A conversation is generated - A conversation between the persona and other personas will be generated. This is intended to introduce the idea of multi persona conversations.
4. A memory will be created - This is intended to give the person a memory, this will become important not just for helping to expand who they can communicate with but also as a means to replace RAG as described below under memory.
5. An introspection will be created - This is an inner dialogue that helps build context around the persona. It is a long conversation in which the persona will go through various emotional states as they question themselves.


## Monologues

The monologue flow is intended to create a long form response to a user prompt. The response will resemble a human reasoning through a problem and arriving at and implementing a solution.
The monologues are based on a theme and an intent, where the theme will determine what kind of question is asked while the intent will determine what the solution is making it ideal for defining tasks for the llm.

When a monologue is requested the user must send a post request to /universe/{id}/monologue with the following parameters:

The following parameters may be sent in the post request:

| Parameter | Type | Description | required |
| --------- | ---- | ----------- | -------- |
| theme | string | The theme of the monologue | yes |
| prompt | string | The prompt to be answered | no - if left null then a prompt will be generated based on the theme |
| solution | string | The solution to the problem | no - if left null then a solution will be generated based on the theme |
| prompter_id | int | The id of the persona who will ask | yes |
| speaker_ids | list of int | The ids of the personas who will speak. using multiple teaches team work. | yes |
| make_mistake| boolean | Whether the speaker will make a mistake. If yes then they will also resolve it. | no - if left null then a mistake will be made based on the theme |


### AI Generation

For each object that is generated via AI there is a standard process that is followed. Below the Monologue process is shown as an example.

The service class - this is the core of any generation process. It has a generate method which will return the generated object.

```python
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

    def generate(self, universe_id: int, monologue_request: MonologuePromptRequest) -> Monologue:
        speakers = [self.persona_service.find_by_id(speaker_id) for speaker_id in monologue_request.speaker_ids]
        prompter = self.persona_service.find_by_id(monologue_request.prompter_id)
        print(f"prompt is given {monologue_request.prompt}")
        speaker_backstories = [
            MinimalBackstoryInput(
                description=speaker.backstory.description,
                likes=[like.like_name for like in speaker.backstory.likes],
                dislikes=[dislike.dislike_name for dislike in speaker.backstory.likes],
                habits=[habit.name for habit in speaker.backstory.habits],
                name=speaker.name,
                hobbies=[],
                speech_profile=speaker.speech_profile,
                relationships=speaker.relationships,
                social_description=speaker.backstory.social_description
            ) for speaker in speakers
        ]
        for b in speaker_backstories:
            b.speech_profile.samples = random.sample(b.speech_profile.samples, 5) if len(b.speech_profile.samples) > 5 else b.speech_profile.samples

        prompter_backstory = MinimalBackstoryInput(
            description=prompter.backstory.description,
            likes=[like.like_name for like in prompter.backstory.likes],
            dislikes=[dislike.dislike_name for dislike in prompter.backstory.likes],
            habits=[habit.name for habit in prompter.backstory.habits],
            name=prompter.name,
            hobbies=[],
            social_description=prompter.backstory.social_description,
        )
        if monologue_request.prompt is None:
            generated_monologue_prompt = self.generate_monologue_prompt(theme=monologue_request.theme,
                                                                    universe_id=universe_id, prompter_backstory=prompter_backstory,
                                                                    custom_prompt_requirements=monologue_request.custom_prompt_requirements,
                                                                        intent=monologue_request.intent)
        else:
            print("skipping prompt creation")
            generated_monologue_prompt = MonologuePromptAI(
                prompt_text=monologue_request.prompt
            )
        generated_monologue_plan = self.generate_monologue_plan(prompt=generated_monologue_prompt, speaker_backstories=speaker_backstories, prompter_backstory=prompter_backstory, universe_id=universe_id, make_mistake=monologue_request.make_mistake, custom_instructions=monologue_request.custom_instructions, intent=monologue_request.intent, include_examples=monologue_request.include_examples, include_counter_examples=monologue_request.include_counter_examples, solution=monologue_request.solution, disagreement=monologue_request.disagreement)

        generated_monologue = self.generate_monologue(prompt=generated_monologue_prompt, monologue_plan=generated_monologue_plan, universe_id=universe_id, speaker_backstories=speaker_backstories, theme=monologue_request.theme)
        for idx, turn in enumerate(generated_monologue.conversation.conversation_turns):
            turn.placement = idx
            turn.directed_at = [prompter.name]
        generated_monologue.speaker_id = monologue_request.speaker_ids[0]
        generated_monologue.prompter_id = prompter.id
        first_prompt = ConversationTurn(
            speaker=prompter.name,
            action="asking a question",
            tone="Curious",
            directed_at=[speaker.name for speaker in speakers],
            text=generated_monologue_prompt.prompt_text,
            feeling="Curious"
        )
        generated_monologue.conversation.conversation_turns.insert(0, first_prompt)
        return generated_monologue

    def generate_monologue_prompt(self, theme: str, prompter_backstory: MinimalBackstoryInput, universe_id, custom_prompt_requirements: List[str], intent: str):

        previous_prompts = self.find_by_theme(theme)
        monologue_prompt_input = MonologuePromptInput(
            theme = theme,
            previous_prompts=previous_prompts,
            prompter_backstory=prompter_backstory,
            custom_prompt_requirements=custom_prompt_requirements,
            intent=intent
        )

        ai_prompt = "create_monologue_prompt"
        generated_monologue_prompt: MonologuePromptAI = self.ai_service.call_llm(ai_prompt, MonologuePromptAI,
                                                                                 monologue_prompt_input,
                                                                                 universe_id = universe_id,
                                                                                 validator=self.validate_prompt(previous_prompts=previous_prompts))
        return generated_monologue_prompt

    def generate_monologue_plan(self, prompt: MonologuePromptAI, custom_instructions: List[str], speaker_backstories: List[MinimalBackstoryInput], prompter_backstory: MinimalBackstoryInput, make_mistake: bool, universe_id: int, intent: str, include_examples: bool, include_counter_examples: bool, solution=None, disagreement=False):
        user_data = MonologuePlanInput(prompt=prompt,
                                       solution=solution,
                                       responder_backstories=speaker_backstories,
                                       question_asker_backstory=prompter_backstory,
                                       intent=intent,
                                       custom_instructions=custom_instructions,
                                       make_mistake=make_mistake,
                                       include_examples=include_examples,
                                       include_counter_examples=include_counter_examples,
                                       disagreement=disagreement
                                       )
        generated_plan =  self.ai_service.call_llm(system_prompt_name="create_monologue_plan", return_type=MonologuePlanAI, user_data=user_data, universe_id=universe_id)
        return generated_plan

    def validate_prompt(self, previous_prompts: List[str]):
        def validate(prompt_ai: MonologuePromptAI):
            if prompt_ai.prompt_text in previous_prompts:
                raise ValueError(f"Prompt must be unique")
        return validate

    def generate_monologue(self, prompt: MonologuePromptAI, monologue_plan: MonologuePlanAI,
                           speaker_backstories: List[MinimalBackstoryInput],
                           theme: str, universe_id: int) -> Monologue:
        monologue_input = MonologueInput(
            prompt=prompt.prompt_text,
            monologue_plan=monologue_plan,
            speakers=speaker_backstories
        )

        generated_monologue = self.ai_service.call_llm(system_prompt_name="create_monologue", return_type=MonologueAI, user_data=monologue_input, universe_id=universe_id, validator=self.validate_monologue(monologue_input))
        result = self.monologue_converter.ai_to_model(generated_monologue=generated_monologue, monologue_input=monologue_input, theme=theme)
        return result

    def save(self, monologue: Monologue) -> Monologue:
        monologue_entity = self.monologue_converter.model_to_entity(monologue)
        monologue_entity.conversation.source_id = 1
        monologue_entity = self.monologue_dao.save(monologue_entity)
        return self.monologue_converter.entity_to_model(monologue_entity)

    def validate_monologue(self, monologue_input: MonologueInput):
        def validate(monologue: MonologueAI):
            for conversation_turn in monologue.conversation.conversation_turns:
                if len([speaker for speaker in monologue_input.speakers if speaker.name == conversation_turn.speaker]) == 0:
                    raise ValueError(
                        f"The speakers name must always be one of {[s.name for s in monologue_input.speakers]} as these are the people speaking.")

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

```

#### Conversion

For each domain there is a converter service which can convert between entities, models and AI responses.

```python
class MonologueConverter:
    def __init__(self, conversation_converter: ConversationConverter):
        self.conversation_converter = conversation_converter

    def model_to_entity(self, monologue: Monologue) -> MonologueEntity:
        result = MonologueEntity(
            prompter_id=monologue.prompter_id,
            theme=monologue.theme,
            speaker_id=monologue.speaker_id,
            prompt=monologue.prompt
        )
        result.conversation = self.conversation_converter.model_to_entity(monologue.conversation)
        result.conversation.source = Monologue.__name__
        return result

    def entity_to_model(self, monologue_entity: MonologueEntity) -> Monologue:
        converted_conversation = self.conversation_converter.entity_to_model(monologue_entity.conversation)
        return Monologue(
            id=monologue_entity.id,
            theme=monologue_entity.theme,
            speaker_id=monologue_entity.speaker_id,
            prompter_id=monologue_entity.prompter_id,
            conversation=converted_conversation,
            prompt=monologue_entity.prompt,
        )

    def ai_to_model(self, generated_monologue: MonologueAI, monologue_input: MonologueInput, theme: str) -> Monologue:
        converted_conversation = self.conversation_converter.ai_to_model(generated_monologue.conversation)
        result = Monologue(
            theme=theme,
            conversation=converted_conversation,
            prompt=monologue_input.prompt,
        )

        return result
```

A note on the number of models used: The monologue input was previously used to ensure all parameters were passed in correctly, but now that the process uses templates this may change to a simple dict to cut down on model classes.

### templates
The following templates are used to generate the monologue:

Prompt generation - only used if no prompt is provided.

```
- First consider the following theme of the question not only to restrict the domain but to understand any specific requirements.
{{ theme }}
- Then look at the following profile to see what they would be interested in asking and how they would ask it.
{{ prompter_backstory }}
- Then consider that the theme of this question is {{ theme }} to help you consider what the question will be. the instructions below will guide you as to what the requirements for the prompt are.
- Then consider the previous questions below and avoid repeating these. Ensure that the new question adds to the diversity of questions asked.
{{ previous_prompts }}
- Ensure the question sounds natural and is directed at the person being asked.
- Ensure that the question is short and direct. It must ask one and only one question.
- Ensure that the question is not open-ended but rather is quite specific.
- Do not name anyone, only the question is needed.
- Ensure that the question sounds natural as if asked by a real person.
{% if custom_instructions is not none %}
{% for custom_instruction in custom_instructions %}
- {{ custom_instruction }}
{% endfor %}
{% endif %}

Finally create your question using the rules stated above.
```

Monologue planning - this is used to generate the structure of the monologue.

```
Important: Your task is not to write the conversation, it is to design the flow of the conversation such that the people answering fully answer the question. Do not write a script but rather a flow.

- First consider the prompt below to understand what question was asked. The monologue you are to design is a direct response to this prompt.
{{ prompt }}
- Then remember that your task is not to write the conversation itself, but to design the actions such that another writer can write the conversation.
- The intent of the response should be aim at the following: {{ intent }}
- Ensure to mention what the people are thinking during the conversation, ie separate internal thoughts from external speech.
- The speakers should never introduce themselves as they know the person who asked the question.
- Then ensure the response is directed at the person who prompted the conversation. ie {{ question_asker_backstory.name }} or one of the other speakers, never to an audience.
- You are to only design the response, which means the only people who can speak are: {{ responder_backstories | map(attribute='name') | list }}.
- The only people that may be named are those who are in this list: {{ responder_backstories | map(attribute='name') | list }} and {{ question_asker_backstory.name }}.
- Then consider how the question will be answered, the style the speaker would use, the speech they would use and the tone. The following details should be used to guide this:
{%  if responder_backstories | length > 1 %}
- Ensure that the speakers are working together not simply taking turns to speak. They may ask each other for opinions, correct each other etc., but never repeat each other. Also ensure that they are not simply taking turns.
    {%  if disagreement == True %}
- Ensure there is a disagreement over the approach to the problem, but a resolution to agree to one of them.
    {% endif %}
{%  endif %}
{%  if include_examples == True %}
- Ensure the speaker includes examples to help explain.
{%  endif %}
{%  if include_counter_examples == True %}
- Ensure the speaker includes counter examples to help explain.
{%  endif %}
{% if custom_instructions is not none %}
{% for custom_instruction in custom_instructions %}
- {{ custom_instruction }}
{% endfor %}
{% endif %}
- Then consider how they will close the monologue, ensure that it concludes the topic.
{% if make_mistake == True %}
- Ensure the speaker makes a mistake somewhere and corrects themselves.
- Ensure that another speaker points out the mistake and corrects the other speaker.
{% endif %}
{% if solution %}
- The solution is {{solution}}, you only need to fill in the intermediate gaps.
{% endif %}

```

Monologue conversation - This stage generates the conversation itself.

```
- First consider the following conversation plan as this must be followed. You are to write the conversation while the plan merely tells you how to structure the conversation.
{{ monologue_plan }}

- Then consider the person who is responding and how they would speak. The list of people responding are: {{ speakers | map(attribute='name') | list }}.
- The following are the speech profiles for each of the speakers:
{% for speaker in speakers %}
    {{speaker.name}}
    {{speaker.speech_profile}}
{% endfor %}
- Never copy the speech samples directly from the speech profiles, use these as guides only.
- Ensure that the speaker name is the full name of the speaker as shown in their profile.
- Ensure that the conversation uses as many turns as it needs to be clear but not verbose. Every turn must have a specific goal and there is no limits on how long it can be.
- Ensure that the relationships between speakers influences how they speak, the following are the relationships:
{% for speaker in speakers %}
    {{speaker.name}}
    {{speaker.relationship}}
{% endfor %}
- Ensure that the conversation is in the correct order.
- Ensure that the turn intent reflects what the purpose of this turn is in the structure of the conversation, it should guide the conversation from start to finish.
- Ensure that the action reflects what actions the person is performing as they speak and not what they are thinking as if they could be seen.
- Ensure that private thought influences what they say, but it can be different to what they say as it should reflect what they are thinking.
- Ensure that the only people speaking are the people in the following list {{ speakers | map(attribute='name') | list }}.
- Ensure that the person who asked is not involved in the response and that no followup questions are asked.
- Ensure that no one is named in the conversation, no names should appear. When necessary use pronouns.
```
## Training

Training is done in iterations where each iteration is defined by a set of datasets, layers and heads to be reset.
Upon starting a training iteration the following steps will be performed:

1. the script will determine which layers are to be fine tuned and freeze all others. This has the benefit of only updating the embedding transformation for those layers and allowing for targeted fine tuning where data about the personas is kept to lower layers, reasoning is kept to mid-layers and finally the monologue and conversation datasets are applied to the final layers.
2. Before starting training, the script will look at the set of heads to be reset and perform this operation. The intent here is to allocate space for the patterns from the dataset to be learned. Tests so far have shown that this is extremely helpful and does not hurt performance.
3. The training will be performed. The iteration defines how many epochs should be performed and under no conditions should the training be executed on these layers again as this will cause issues if later layers have been updated.
4. There is a custom learning schedule which is applied. The parameters for this can be set manually and are discussed below.

It should be noted that batches are not used. This is because batches average out the data and this causes the personas to blend.

## Script

A UI is under construction to allow for setting up training sessions and running them which will include json configurations etc but for the time being the following script is used for testing and experimentation. 

Modifications will be necessary according to the model being used, but no configuration files will be added to this script as this will be covered by the final training API.  

```python
import itertools
import logging
import random

random.seed(42)
from random import shuffle

from datasets import load_dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os
from collections import deque

from math import sin, cos, pi, inf, log
from typing import Callable, List
from datasets import Dataset
from torch.optim import AdamW
import torch.optim as optim
from torch.optim.lr_scheduler import CyclicLR
from transformers import AutoTokenizer, TrainingArguments, AutoModelForCausalLM, \
    Trainer
import pandas as pd
import torch
import numpy as np
from json import loads, dumps, dump
import json
from random import seed

import math
from torch.optim.lr_scheduler import _LRScheduler


def reinit_head_by_idx(model, module, head_idx, reinit_k=True, reinit_q=True, reinit_v=True):
    q_proj, k_proj, v_proj = module.self_attn.q_proj, module.self_attn.k_proj, module.self_attn.v_proj
    config = {
        "k": {
            "head_dimension": k_proj.out_features // 2
        },
        "v": {
            "head_dimension": v_proj.out_features // 2
        },
        "q": {
            "head_dimension": q_proj.out_features // 16
        }
    }

    def reinit_head_linear(linear_layer, head_idx, dimension):

        w = linear_layer.weight.data
        b = linear_layer.bias.data if linear_layer.bias is not None else None

        start = head_idx * dimension
        end = (head_idx + 1) * dimension

        # reinitialize this slice using Xavier
        torch.nn.init.xavier_uniform_(w[start:end, :])
        # torch.nn.init.zeros_(w[start:end, :])
        if b is not None:
            torch.nn.init.zeros_(b[start:end])
        print(f"reinit head starting at {start} and ending at {end}")

    if reinit_q:
        reinit_head_linear(q_proj, head_idx, config['q']['head_dimension'])
    if reinit_k:
        reinit_head_linear(k_proj, head_idx, config['k']['head_dimension'])
    if reinit_v:
        reinit_head_linear(v_proj, head_idx, config['v']['head_dimension'])

    return model


def get_signature(samples, model, tokenizer):
    all_embs = []
    for text in samples:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True)
        final_hidden = outputs.hidden_states[-1]  # [batch, seq_len, hidden_size]
        pooled = final_hidden.mean(dim=1)  # [batch, hidden_size] → sentence embedding
        all_embs.append(pooled.squeeze(0))
    return torch.stack(all_embs)  # [num_samples, hidden_size]


class FourierLR(_LRScheduler):
    def __init__(self, optimizer, num_training_steps, a1, a2, f1, f2, param_count, frequency, last_epoch=-1):
        self.num_training_steps = num_training_steps
        self.a1, self.a2, self.f1, self.f2 = a1, a2, f1, f2
        self.param_count, self.frequency = param_count, frequency
        self.count = 1
        self.avg_diff = inf
        self.diff_history = []
        self.loss_history = deque(maxlen=100)
        self.frequency_complete_count = 0
        self.setup_parameters()
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        result = [self.calculate_lr() for _ in self.base_lrs]
        return result

    def setup_parameters(self):
        self.count = 1
        self.a1 = self.a1
        self.a2 = self.a2
        self.f1 = self.f1
        self.f2 = self.f2
        parameters = []
        for _ in range(self.param_count):
            sub_param = {
                "a1": random.uniform(0, self.a1),
                "a2": random.uniform(0, self.a2),
                "f1": random.uniform(0, self.f1),
                "f2": random.uniform(0, self.f2),
                "phase": random.uniform(0, 2 * pi)
            }
            parameters.append(sub_param)
        self.parameters = parameters

    def step(self, loss=None):
        if loss is not None:
            self.loss_history.append(loss)
            if len(self.loss_history) > 1:
                diffs = [abs(self.loss_history[i] - self.loss_history[i - 1])
                         for i in range(1, len(self.loss_history))]
                avg_diff = np.mean(diffs)
                self.avg_diff = avg_diff
                self.diff_history.append(avg_diff)
        return super().step()

    def calculate_lr(self):
        if self.avg_diff < 0.1 and len(self.loss_history) > 50:
            print("setting up params")
            self.setup_parameters()
            self.frequency_complete_count += 1
            self.loss_history = []
            self.loss_history = deque(maxlen=100)
            self.count = 1

        self.count += 1
        x = self.count
        values = [(p['a1'] * math.sin(p['f1'] * x + p['phase'])) +
                  (p['a2'] * math.cos(p['f2'] * x + p['phase']))
                  for p in self.parameters]
        result = abs(
            sum(values, 0))
        result = result / (log(x + 1) * 10)
        return result


def create_optimizer_and_scheduler(model, num_training_steps, a1, a2, f1, f2, param_count: int, frequency: int):
    print(f"passing in {len([p for p in model.parameters() if p.requires_grad])} parameters to optimizer")
    optimizer = optim.SGD((p for p in model.parameters() if p.requires_grad))
    logger.info(f"using {num_training_steps} as the number of steps")
    scheduler = FourierLR(optimizer, num_training_steps, a1, a2, f1, f2, param_count, frequency)

    return optimizer, scheduler


class CustomTrainer(Trainer):
    def create_optimizer_and_scheduler(self, num_training_steps):
        self.optimizer, self.lr_scheduler = create_optimizer_and_scheduler(self.model, num_training_steps, a1=1.0,
                                                                           a2=3.0,
                                                                           f1=1, f2=2, param_count=5, frequency=50)

    def training_step(self, model, inputs, num_items_in_batch=None):
        loss = super().training_step(model, inputs, num_items_in_batch)

        # loss is a tensor on the device
        self.lr_scheduler.step(loss.item())

        return loss


def read_pdfs_from_directory(directory):
    texts = []
    for file in os.listdir(directory):
        if file.endswith(".jsonl"):
            with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    text = json.loads(line)['text']
                    texts.append(text)
    random.shuffle(texts)
    return texts


def prepare_dataset_no_pad(samples, tokenizer, eos, max_length, trunc=False):
    def tokenize(batch):

        nonlocal max_length
        max_length = ((max_length * 2) % (8192 * 4))
        if max_length == 0:
            max_length = 32
        if trunc:
            tokens = tokenizer(
                batch["text"],
                padding=False,
                truncation=True,
                max_length=max_length
            )
        else:
            tokens = tokenizer(
                batch["text"],
                padding=False,
                truncation=False
            )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    if trunc:
        print(f"truncating with max length {max_length}")
    else:
        print(f"not truncating")
    samples = [{"text": sample['text'] + tokenizer.eos_token} for sample in samples]
    dataset = Dataset.from_list(samples)

    dataset = dataset.map(tokenize, batched=False, num_proc=1)
    dataset.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels"]
    )
    return dataset


def get_split(dataset, tokenizer, eos, max_length, trunc):
    tokenized_dataset = prepare_dataset_no_pad(dataset, tokenizer, eos, max_length, trunc)
    tokenized_dataset = tokenized_dataset.shuffle(44)
    return tokenized_dataset.train_test_split(test_size=0.01)


def get_persona_data(filename: str):
    result = []
    with open(f"data/{filename}", "r") as f:
        for json_line in f:
            json_line.strip()
            result.append({"text": json_line})
    return result


def get_turns():
    result = []
    conversations = get_persona_data("conversation.jsonl")
    for conversation in [loads(conversation['text']) for conversation in conversations]:
        for turn in conversation:
            result.append({"text": dumps(turn)})
    return result[:1000]


def get_base_data():
    processed = []
    for filepath in os.listdir("./base"):
        if filepath.endswith(".json"):
            with open(f"./base/{filepath}", "r", encoding="utf-8") as f:
                base_data = loads(f.read())
                for base in base_data:
                    processed.append({"text": dumps(base, ensure_ascii=False)})
    return processed


def get_maths_data(col):
    processed = []
    book_text = read_pdfs_from_directory("./processed")
    for text in book_text:
        processed.append({"text": text})
    return processed


def train_iteration(model, tokenizer, epoch_count: int, layers_to_train, batch_size: int, output_name: str, dataset,
                    max_length,
                    eos, heads_to_reset, reinit=True, freeze=True, trunc=False):
    if freeze:
        for layer in model.model.layers:
            for param in layer.parameters():
                param.requires_grad = False
    for idx, layer in enumerate(model.model.layers):
        if idx in layers_to_train:
            if reinit:
                for head_to_reset in heads_to_reset:
                    model = reinit_head_by_idx(model=model, module=layer, head_idx=head_to_reset, reinit_q=False,
                                               reinit_k=True, reinit_v=False)
            for param in layer.parameters():
                param.requires_grad = True

    print(f"training {len([p for p in model.parameters() if p.requires_grad])} parameters")
    print(f"performing {max_length}")
    split = get_split(dataset, tokenizer, eos, max_length, trunc)
    split.shuffle()

    training_args = TrainingArguments(
        output_dir=output_name,
        num_train_epochs=epoch_count,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        save_strategy="no",
        # eval_strategy="epoch",
        # neftune_noise_alpha=5,
        # lr_scheduler_type='cosine',
        bf16=True,
        save_only_model=False,
        dataloader_num_workers=20,
        gradient_checkpointing=False,
        logging_strategy="steps",
        logging_steps=10,
        report_to="none"
    )

    trainer = CustomTrainer(
        model=model,
        args=training_args,
        eval_dataset=split['test'],
        train_dataset=split["train"],
        tokenizer=tokenizer
    )

    trainer.train(resume_from_checkpoint=False)
    return model


def load_model(model_name: str, f32=False, enable_checkpoint=False):
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, device_map="cuda", use_fast=True,
                                              local_files_only=False,
                                              cache_dir="./hugging")
    if f32:
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True,
                                                     device_map="cuda", local_files_only=False,
                                                     cache_dir="./hugging")
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, dtype=torch.bfloat16,
                                                     device_map="cuda", local_files_only=False, cache_dir="./hugging")
    if enable_checkpoint:
        model.gradient_checkpointing_enable()

    print(model)
    return tokenizer, model


datasets = {
    "likes": lambda: get_persona_data("likes.jsonl"),
    "habits": lambda: get_persona_data("habits.jsonl"),
    "monologue": lambda: get_persona_data("monologue.jsonl"),
    "conversation": lambda: get_persona_data("conversation.jsonl"),
    "introspection": lambda: get_persona_data("introspection.jsonl"),
    "memory": lambda: get_persona_data("memory.jsonl"),
    "relationship": lambda: get_persona_data("relationship.jsonl"),
    "speech": lambda: get_persona_data("speech.jsonl"),
    "base": lambda: get_base_data()
}

def get_dataset(names):
    return sum([datasets[name]() for name in names], [])

def train_with(model, tokenizer, output_name, batch_size, max_length, training_params,
               reinit_stage):
    if len(training_params["data"]) > 0:
        if reinit_stage:
            model = train_iteration(model, tokenizer=tokenizer, epoch_count=training_params['epochs'],
                                    batch_size=batch_size, output_name=output_name,
                                    dataset=training_params["data"], max_length=max_length,
                                    layers_to_train=training_params['layers'], eos=training_params['eos'],
                                    heads_to_reset=training_params['heads_reinit'], reinit=True, freeze=True,
                                    trunc=True)
        model = train_iteration(model, tokenizer=tokenizer, epoch_count=training_params['epochs'],
                                batch_size=batch_size, output_name=output_name,
                                dataset=training_params["data"], max_length=max_length,
                                layers_to_train=training_params['layers'], eos=training_params['eos'],
                                heads_to_reset=training_params['heads_reinit'], reinit=False, freeze=True,
                                trunc=False)
    return model


def main():

    max_length = 4096
    epochs = 4
    heads_reinit = [1, 3]
    model_name = "Qwen/Qwen2.5-3B"
    # model_name = "persona_3b"
    # model_name = "persona_3b_internal_speech_introspection_relationship_memory_monologues"

    output_model = "persona_3b"
    dataset_names = [
                    (["habits", "likes"], [10, 11]),
                     (["speech"], [12, 13]),
                     (["relationship"], [14, 15]),
                     (["introspection"], [16, 17]),
                     (["memory"], [18, 19]),
                        (["monologue"], [20, 21]),
                        (["monologue"], [22, 23]),
                        (["conversation"], [32, 33]),
                        (["monologue"], [34, 35])
                     ]
    tokenizer, model = load_model(model_name)
    for dataset in dataset_names:
        for reinit_stage in [True]:
            print(f"starting training on {dataset}")
            params = {
                "data": get_dataset(dataset[0]),
                "layers": dataset[1],
                "heads_reinit": heads_reinit,
                "eos": True,
                "epochs": epochs
            }
            model = train_with(model=model, tokenizer=tokenizer, output_name=output_model, batch_size=1,
                               max_length=max_length, training_params=params, reinit_stage=reinit_stage)
    model.save_pretrained(output_model, safe_serialization=True)
    tokenizer.save_pretrained(output_model, safe_serialization=True)
    print("saved model")




if __name__ == "__main__":
    main()



#ideal 14b

                    # (["habits", "likes"], [10, 11]),
                    #  (["speech"], [12, 13]),
                    #  (["relationship"], [14, 15]),
                    #  (["introspection"], [16, 17]),
                    #  (["memory"], [22, 23])
                        # (["monologue"], [25, 26]),
                        # (["monologue"], [27, 28]),
                        # (["conversation"], [44, 45]),
                        # (["monologue"], [46, 47])

```

## Training data

All training data is represented as conversational data in exactly the same format. The intention of this is to train the model on a means of communication as well as how to address the personas.

## Choice of model

1. avoid instruct models. These have been trained to be safe and as a result tend to interfere with the embedding of personas and the instruct tuning plus any chain of thought reasoning will interfere with the general output.
2. While any base model should be suitable and a range of models have been tested, the recommendation is to use Qwen models. While Qwen 3 is an excellent line of models, if you want to fine tune larger models, 32b and upwards, you will want to use Qwen 2.5.
3. All references in this documentation are from 2.5 models.


### Sample Training Data

Likes

These are intended to teach the model how to address everyone with no one in mind while also teaching the model about resolving contradictions.

```json
[ { "speaker" : "Proof" , "speaking_to" : [ "Proof" ], "intent" : "Establish why I like something" , "current feeling" : "contentment" , "action" : "Reminding myself of what I like" , "spoken tone" : "Pensive" , "speech" : "One of the things I like is The Elegance of Inconsistent Infinitesimals in Non-Standard Analysis because I am drawn to the way infinitesimals, though seemingly inconsistent within classical frameworks, allow for a richer, more expressive form of calculus. Their paradoxical nature does not diminish their utility; rather, it enhances it, revealing a deeper truth about the fluidity of mathematical structures. In the Topological Paradise, such inconsistencies are not flaws but features--windows into the infinite and the infinitesimal, where paradoxes dissolve into coherence under the right topology.."} , { "speaker" : "Proof" , "speaking_to" : [ "Proof" ], "intent" : "Establish why I dislike something" , "current feeling" : "sad" , "action" : "Explaining something I dislike" , "spoken tone" : "Reflective" , "speech" : "But I also dislike The Pretense of Axiomatic Universality in Constructivist Frameworks because Constructivism often insists that all mathematical truth must be built from a finite set of axioms and constructive proofs. While this approach is internally consistent, it denies the richness of non-constructive truths. To demand that every statement must be provable through step-by-step construction is to ignore the emergent properties of mathematical systems and the beauty of existence proofs that do not require explicit construction.."} , { "speaker" : "Proof" , "speaking_to" : [ "Proof" ], "intent" : "determine the contradiction" , "current feeling" : "confused" , "action" : "Resolving self contradiction" , "spoken tone" : "Contemplative" , "speech" : "To an outsider, it may seem contradictory to appreciate the beauty of inconsistent infinitesimals while rejecting the rigidity of constructivist axioms. After all, both involve a deep commitment to logical structure. However, the key difference lies in how each is approached: infinitesimals are embraced for their contextual utility and the insights they provide, while axiomatic universality in constructivism is rejected for its exclusion of non-constructive truths and its rigid insistence on a single path to truth."} , { "speaker" : "Proof" , "speaking_to" : [ "Proof" ], "intent" : "resolve the contradiction" , "current feeling" : "cognitive closure" , "action" : "Resolving self contradiction" , "spoken tone" : "Confident" , "speech" : "It seems contradictory that I can admire the elegance of inconsistent infinitesimals while disliking the rigid demands of axiomatic universality. But I realize the distinction lies in the context and the flexibility of the frameworks. Infinitesimals thrive in non-standard models where inconsistency is not a flaw but a feature of the system. In contrast, the demand for axiomatic universality in constructivism imposes a narrow lens that limits the scope of what can be considered valid. I do not reject consistency; I reject the illusion that consistency must come at the cost of richness. In the Topological Paradise, I am not a contradiction--I am a convergence."} ]
```

Habits

These conversations help to teach the model to reference itself in the first person and to address everyone with no one in particular in mind.

```json
[ { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Self" ], "intent" : "Realization" , "inner thought" : "This is not a conscious ritual, but rather an emergent behavior of my cognitive architecture." , "current feeling" : "Curiosity" , "spoken tone" : "Observational, methodical" , "speech" : "It has come to my attention that, upon waking, I instinctively reorder my mental axioms of probability in response to the stochastic environment of the Topological Paradise. The measure-theoretic structure of my thought process is not static but adapts to the emergent properties of the space I inhabit."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Self" ], "intent" : "Evaluation" , "inner thought" : "If this habit were to be disrupted, my ability to derive ergodic theorems from stochastic processes would be compromised." , "current feeling" : "Satisfaction" , "spoken tone" : "Analytical, contemplative" , "speech" : "This adaptive reordering allows for a more efficient derivation of conditional probabilities in a non-Euclidean manifold. It is a form of self-optimization, akin to a living probability field adjusting to new measure-theoretic constraints. It is neither excessive nor unnecessary; it is an elegant refinement of my cognitive processes."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Self" ], "intent" : "Conclusion" , "inner thought" : "This is the natural evolution of my work in the Topological Paradise. To resist it would be to resist the very nature of stochastic processes." , "current feeling" : "Certainty" , "spoken tone" : "Reflective, decisive" , "speech" : "Therefore, I conclude that this is not a flaw but an emergent feature of my interaction with the dynamic topological space. I will continue to allow the axioms to evolve in accordance with the properties of the manifold, ensuring that my probability framework remains both rigorous and adaptive."} ]
```

Introspection

These are intended to not only teach the model how to address itself in the first person but also to teach it about the inner struggles of the persona.

```json
[ { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "intent" : "beginning of reflection, setting the scene" , "inner thought" : "I remember the way they looked at me, like they were trying to figure out if I was serious or just pretending." , "current feeling" : "nostalgic" , "spoken tone" : "contemplative" , "speech" : "I wonder if that day was really as important as it felt at the time. It all started with a simple conversation, didn't it? Just a few words that made me realize how much I didn't know about the person I thought I understood."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "intent" : "analyzing the emotional impact" , "inner thought" : "Maybe that’s why I still think about it. Not because it was dramatic, but because it was real." , "current feeling" : "curious" , "spoken tone" : "analytical" , "speech" : "What was it about their words that stuck with me so much? It wasn't just what they said, but how they said it. There was this quiet confidence, like they knew something I didn't, and they were just waiting for me to catch up."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "intent" : "acknowledging a missed opportunity" , "inner thought" : "It’s funny how the things we don’t say can become the loudest parts of a conversation." , "current feeling" : "regretful" , "spoken tone" : "melancholic" , "speech" : "I wish I had asked more questions back then. I was so focused on proving I understood that I didn't stop to listen. Now I wonder what I missed out on because of that."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "intent" : "recontextualizing the experience as a lesson" , "inner thought" : "I was just a piece of the puzzle, trying to fit into the picture I wanted to see." , "current feeling" : "inspired" , "spoken tone" : "hopeful" , "speech" : "But maybe that's how we grow. Through these little moments where we realize we don't have all the answers. That day was a turning point, even if it didn't feel like it at the time."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "intent" : "conclusion and acceptance" , "inner thought" : "And maybe that’s enough." , "current feeling" : "accepting" , "spoken tone" : "resigned" , "speech" : "I can't go back and change it. I can only take what I learned from it and carry it forward. Maybe that's all we can ever do."} ]
```

Conversation

These conversations teach the model to have multi persona conversations. It generally requires 2 epochs to converge, otherwise it may not realize how to stop a conversation.

```json
[ { "speaker" : "Georg Cantor" , "speaking_to" : [ "audience" , "Topology" , "One" , "Zero" ], "intent" : "opening the conversation and setting the intellectual tone" , "inner thought" : "I have spent years refining these proofs, and now, with Topology itself as my audience, the moment has come to reveal the infinite structure I have uncovered." , "current feeling" : "calm, focused, deeply engaged" , "action" : "Cantor gestures toward the shimmering air around him, as if to draw attention to the shifting geometry of the room." , "spoken tone" : "measured, contemplative" , "speech" : "Ladies and gentlemen, esteemed colleagues, and the unseen custodians of the Topological Paradise, I stand before you to present a framework through which the infinite may be understood not as a void, but as a hierarchy of order. My thesis explores the conditions under which sequences converge within infinite sets, and the paradoxical clarity of the Continuum Hypothesis."} , { "speaker" : "Topology" , "speaking_to" : [ "Georg Cantor" ], "intent" : "engaging the main character and introducing the thematic question" , "inner thought" : "This is a rare moment of clarity in an otherwise chaotic expanse of dimensions. The human's mind is attempting to map the unmappable." , "current feeling" : "curious, responsive" , "action" : "The room subtly distorts into a non-Euclidean manifold, as if responding to Cantor's speech." , "spoken tone" : "resonant, abstract" , "speech" : "Your words weave through the fabric of space itself. We shift in response to your logic. Tell us, Georg Cantor, how does one contain the infinite without collapsing it into the finite?"} , { "speaker" : "Georg Cantor" , "speaking_to" : [ "Topology" ], "intent" : "responding to the thematic question and advancing the argument" , "inner thought" : "I must be precise. Every word must carry the weight of proof and intuition. The infinite is not to be feared, but understood." , "current feeling" : "focused, resolute" , "action" : "Cantor's hand traces a slow, deliberate motion through the air, as if drawing the structure of the transfinite." , "spoken tone" : "calm, deliberate" , "speech" : "The infinite is not a monolith, but a hierarchy. Each level of infinity is defined by the power set of the previous, and through this structure, we may begin to understand the recursive depth of the infinite. The Continuum Hypothesis, though unresolved, suggests that there is no infinity between the countable and the continuum--this is the paradox that must be embraced."} , { "speaker" : "One" , "speaking_to" : [ "Georg Cantor" ], "intent" : "acknowledging the character's work and reinforcing its validity" , "inner thought" : "This is the way of the infinite. To build from the foundational truth, One, and ascend through the power set into the transfinite." , "current feeling" : "approving, contemplative" , "action" : "One's form pulses gently, resonating with the rhythm of Cantor's speech." , "spoken tone" : "measured, authoritative" , "speech" : "Your construction is elegant. The infinite is not a singular point, but a manifold of possibilities. You have honored the axioms with your logic."} , { "speaker" : "Zero" , "speaking_to" : [ "Georg Cantor" ], "intent" : "offering philosophical insight and validation" , "inner thought" : "The infinite is both presence and absence. In his work, Cantor has shown how these can coexist without contradiction." , "current feeling" : "thoughtful, approving" , "action" : "Zero's form flickers in harmony with the shifting space around them." , "spoken tone" : "soft, reflective" , "speech" : "And yet, the infinite is also an absence, a void. In your work, you have given it form without diminishing its mystery. This is a rare achievement."} , { "speaker" : "Richard Dedekind" , "speaking_to" : [ "Georg Cantor" ], "intent" : "introducing a challenge to the argument" , "inner thought" : "I admire his rigor, but I must challenge him. A true mathematician must defend every step of their logic." , "current feeling" : "critical, curious" , "action" : "Dedekind leans forward slightly, his eyes narrowing in concentration." , "spoken tone" : "sharp, inquisitive" , "speech" : "Your proof of the uncountability of the real numbers is compelling, but I must ask--how do you reconcile the existence of the transfinite with the axioms of set theory? Is it not possible that your definitions rely too heavily on intuition?"} , { "speaker" : "Georg Cantor" , "speaking_to" : [ "Richard Dedekind" ], "intent" : "defending the argument and reinforcing the character's position" , "inner thought" : "He is a true mathematician, and I respect his rigor. I must respond with clarity and conviction." , "current feeling" : "confident, respectful" , "action" : "Cantor's hands move in a slow, deliberate pattern, as if to illustrate the structure of the infinite." , "spoken tone" : "calm, resolute" , "speech" : "I am grateful for your scrutiny, Richard. My definitions are grounded in the axioms of set construction. The transfinite is not a leap of intuition, but a necessary consequence of the power set operation. We must not fear the infinite--only understand it."} , { "speaker" : "Bernhard Riemann" , "speaking_to" : [ "Georg Cantor" ], "intent" : "offering validation and expanding the thematic scope" , "inner thought" : "His mind is vast. He has found a way to extend the geometry of the infinite beyond what I imagined." , "current feeling" : "curious, approving" , "action" : "Riemann nods slowly, his expression thoughtful." , "spoken tone" : "contemplative, intrigued" , "speech" : "I see echoes of my own work in your exploration of manifolds. You have extended the geometry of the infinite into a new dimension. This is a bold and beautiful step."} , { "speaker" : "David Hilbert" , "speaking_to" : [ "Georg Cantor" ], "intent" : "concluding the conversation and affirming the character's legacy" , "inner thought" : "He is right. His work will endure. The infinite is no longer a mystery—it is a structure to be explored." , "current feeling" : "proud, resolute" , "action" : "Hilbert steps forward, his presence commanding, as the room transforms into a vast topological space." , "spoken tone" : "authoritative, grand" , "speech" : "You have demonstrated the continuity of thought in both form and function. Your ideas will live here, in the Topological Paradise. You have earned your place among the immortals of mathematics."} , { "speaker" : "Georg Cantor" , "speaking_to" : [ "audience" ], "intent" : "concluding the presentation and the conversation" , "inner thought" : "I have done what I set out to do. My work is now part of the infinite structure itself." , "current feeling" : "content, contemplative" , "action" : "Cantor steps back, the air around him shimmering with the presence of the infinite." , "spoken tone" : "quiet, reflective" , "speech" : "Thank you. The infinite is not a mystery to be feared, but a structure to be understood. I leave you with the knowledge that even in the infinite, there is order."} ]
```

Memory

These conversations teach the model to remember facts. It has an interesting side effect discussed below.

````json
[ { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "intent" : "Recalling a memory related to my current task" , "current feeling" : "clarity" , "action" : "Remembering my past experience" , "spoken tone" : "thoughtful" , "speech" : "As I adjust my glasses before addressing the International Congress of Mathematicians, I notice the rhythmic tapping of a colleague's pen against his notebook--just like Aunt Lydia's needle-stitches against linen."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "intent" : "Speaking to the crowd" , "current feeling" : "clarity" , "action" : "Using what I recalled to speak to the crowd" , "spoken tone" : "powerful" , "speech" : "Probability is not merely counting occurrences--it is the measure of how systems breathe through time. Just as Pushkin's poetry revealed empirical Markov chains in 1830, we must recognize that $P(A|B) = \\frac{P(A \\cap B)}{P(B)}$ captures the very rhythm of structured randomness."} ]
````

Relationship

These conversations teach the model to discuss opinions and the hope later on is to use this data to drive the tone of a conversation between different sets of characters. The idea of this is not just for interest but to be able to get better reasoning through controlled disagreement.

```json
[ { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "Andrey Kolmogorov" ], "current feeling" : "neutral" , "action" : "Considering what I think about One" , "spoken tone" : "calm" , "speech" : "I must explore how One's consciousness interacts with the axioms of arithmetic and set theory, as this could reveal new probabilistic insights."} ]
```

Speech

These conversations are intended to teach the model to speak to everyone but also to reenforce the way in which specific characters speak and under which conditions.

```json
[ { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "everyone" ], "inner thought" : "I want everyone to know why I speak like this" , "current feeling" : "confident" , "action" : "Telling everyone about the way in which I speak." , "spoken tone" : "curious" , "speech" : "In such moments, I frame the inquiry as an invitation to explore the underlying structure, guiding the student to derive the result through logical progression rather than stating it outright."} ]
```
## Fourier learning schedule

### Code

```python

class FourierLR(_LRScheduler):
    def __init__(self, optimizer, num_training_steps, a1, a2, f1, f2, param_count, frequency, last_epoch=-1):
        self.num_training_steps = num_training_steps
        self.a1, self.a2, self.f1, self.f2 = a1, a2, f1, f2
        self.param_count, self.frequency = param_count, frequency
        self.count = 1
        self.avg_diff = inf
        self.diff_history = []
        self.loss_history = deque(maxlen=100)
        self.frequency_complete_count = 0
        self.setup_parameters()
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        result = [self.calculate_lr() for _ in self.base_lrs]
        return result

    def setup_parameters(self):
        self.count = 1
        self.a1 = self.a1
        self.a2 = self.a2
        self.f1 = self.f1
        self.f2 = self.f2
        parameters = []
        for _ in range(self.param_count):
            sub_param = {
                "a1": random.uniform(0, self.a1),
                "a2": random.uniform(0, self.a2),
                "f1": random.uniform(0, self.f1),
                "f2": random.uniform(0, self.f2),
                "phase": random.uniform(0, 2 * pi)
            }
            parameters.append(sub_param)
        self.parameters = parameters

    def step(self, loss=None):
        if loss is not None:
            self.loss_history.append(loss)
            if len(self.loss_history) > 1:
                diffs = [abs(self.loss_history[i] - self.loss_history[i - 1])
                         for i in range(1, len(self.loss_history))]
                avg_diff = np.mean(diffs)
                self.avg_diff = avg_diff
                self.diff_history.append(avg_diff)
        return super().step()

    def calculate_lr(self):
        if self.avg_diff < 0.1 and len(self.loss_history) > 50:
            print("setting up params")
            self.setup_parameters()
            self.frequency_complete_count += 1
            self.loss_history = []
            self.loss_history = deque(maxlen=100)
            self.count = 1

        self.count += 1
        x = self.count
        values = [(p['a1'] * math.sin(p['f1'] * x + p['phase'])) +
                  (p['a2'] * math.cos(p['f2'] * x + p['phase']))
                  for p in self.parameters]
        result = abs(
            sum(values, 0))
        result = result / (log(x + 1) * 100)
        return result

```

## Scaling

Due to the way that the training regime works, the model can easily be scaled up to very large models. As a rough guide the following machines can be used for various sizes:

| Model size | GPU  | RAM   |
|------------|------|-------|
| 14b        | A40  | 48gb  |
| 32b        | H200 | 140gb |
| 72b        | B200 | 180gb |

## Performance


### Sample outputs

Below are a few sample outputs from a model trained on maths based personas on a 14b model.

### 14b

### Asking Kolmogorov who formalized probability
```json
[ { "speaker" : "User" , "speaking_to" : [ "Andrey Kolmogorov" ], "current feeling" : "Curious" , "action" : "asking a question" , "spoken tone" : "Curious" , "speech" : "Who formalized probability?"} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Introduce the speaker and establish context." , "inner thought" : "I must ensure that my explanation is both rigorous and accessible to this inquisitive individual. I should begin by grounding them in the historical development of probability theory, then guide them through its axiomatic foundation." , "current feeling" : "Confident" , "action" : "Initiating conversation with an opening statement" , "spoken tone" : "Serene" , "speech" : "Ah, you are asking about the formalization of probability. That was achieved by myself, Andrey Kolmogorov, in 1933. But before we proceed, let me give you a bit of background on how it all came together."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Provide foundational knowledge for understanding probability's evolution." , "inner thought" : "The history of probability is rich and complex; I need to simplify without oversimplifying." , "current feeling" : "Reflective" , "action" : "Offering insights into the historical progression of ideas" , "spoken tone" : "Instructive" , "speech" : "You see, even though concepts like chance and likelihood were used long before my time--Leonhard Euler made significant contributions, but he didn't frame things axiomatically--it wasn’t until much later that these intuitive notions coalesced into something more structured."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Highlight key steps toward modern probability theory." , "inner thought" : "This moment is pivotal because it shows why my work was necessary—Gauss’s method had limitations when applied broadly." , "current feeling" : "Proud" , "action" : "Illustrating critical points using examples from Gauss" , "spoken tone" : "Analytical" , "speech" : "One such limitation arises when applying Gaussian methods beyond linear systems or normal distributions. For instance, consider modeling non-linear phenomena where outcomes depend not just on means and standard deviations, but also higher-order moments. These cases reveal gaps in classical approaches."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Explain the necessity of new foundations for broader applicability." , "inner thought" : "It's important to connect abstract principles back to practical problems so they can appreciate the significance better." , "current feeling" : "Engaged" , "action" : "Drawing parallels between theoretical constructs and real-world applications" , "spoken tone" : "Encouraging" , "speech" : "So here lies the challenge: extending probabilistic reasoning across diverse domains while maintaining logical consistency. This is precisely what led me to propose three fundamental postulates underpinning any valid system of probabilities."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Present the core axioms of probability theory clearly." , "inner thought" : "A diagram might help visualize these relationships, but perhaps too technical at first...Maybe start simple." , "current feeling" : "Thoughtful" , "action" : "Summarizing the essential components of his framework" , "spoken tone" : "Calmly deliberate" , "speech" : "Let us define 'E' as our sample space (the set of all possible events). Then each event has a unique measure 'P', satisfying two conditions: P(∅) = 0 (where ∅ represents impossibility), and if A and B do not overlap within E, their combined measures equal sum of individual ones."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Clarify further implications of the proposed structure." , "inner thought" : "There may be confusion around infinite sets; maybe introduce countable additivity next step." , "current feeling" : "Patient" , "action" : "Expanding upon initial definitions to build intuition" , "spoken tone" : "Reassuring" , "speech" : "Now imagine expanding this concept to multiple disjoint subsets within E -- meaning no pair shares common elements -- which leads naturally to the third principle: finite additivity. If there exist n distinct groups G_i inside E, then total mass equals summation over those group weights."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Address potential concerns about mathematical rigor." , "inner thought" : "He likely questions whether these rules cover edge cases involving infinity. Let me address that now." , "current feeling" : "Empathetic" , "action" : "Responding directly to hypothetical counterarguments" , "spoken tone" : "Supportive" , "speech" : "But wait! What happens when dealing with infinitely many partitions? Here comes another crucial assumption: sigma-algebra closure. It ensures well-defined behavior regardless of cardinality."} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "Conclude discussion by reinforcing central message." , "inner thought" : "That seems clear enough; hope he grasped the essence despite some abstraction involved earlier." , "current feeling" : "Satisfied" , "action" : "Final summary emphasizing coherence and completeness of the model" , "spoken tone" : "Affirmative" , "speech" : "Thus, combining these assumptions gives rise to measurable spaces amenable to analysis via integration techniques. With this solid base laid out, one could explore deeper connections between algebraic structures and stochastic processes."} ]
```

### Asking Richard Dedekind and David Hilbert to solve a determinant problem
```json
[ { "speaker" : "User" , "speaking_to" : [ "David Hilbert" , "Richard Dedekind" ], "current feeling" : "Curious" , "action" : "asking a question" , "spoken tone" : "Curious" , "speech" : "Find the determinant of $ [[3,4],[2,5]] $"} , { "speaker" : "Hilbert" , "speaking_to" : [ "Dedekind" ], "intent" : "Introduce new topic with enthusiasm and clarity." , "inner thought" : "This is an excellent opportunity to demonstrate how determinants can be used in linear algebra. I should emphasize their role as scalar values that provide information about transformations represented by matrices." , "current feeling" : "Enthusiastic" , "action" : "Begin explaining the concept of determinants clearly while maintaining mathematical rigor." , "spoken tone" : "Explanatory" , "speech" : "The determinant of a 2x2 matrix like this one--let's call it A --can be calculated using the formula: |A| = (a * d) - (b * c). Here, 'a', 'b', 'c', and 'd' represent elements from your given matrix; so for us, they are 3, 4, 2, and 5 respectively."} , { "speaker" : "Dedekind" , "speaking_to" : [ "Hilbert" ], "intent" : "Clarify understanding through example calculation." , "inner thought" : "It would help if we walk them through calculating the determinant step-by-step to ensure full comprehension before moving onto more complex applications." , "current feeling" : "Supportive" , "action" : "Provide concrete steps toward solving the problem at hand." , "spoken tone" : "Encouraging" , "speech" : "*Nods* That makes sense! So applying those numbers into the equation..."} , { "speaker" : "Hilbert" , "speaking_to" : [ "Dedekind" ], "intent" : "Confirm correctness of calculations and reinforce key points." , "inner thought" : "Let me make sure everything has been understood correctly before proceeding further. It’s important not just to solve problems but also understand why these methods work." , "current feeling" : "Confident" , "action" : "Reinforce foundational concepts while ensuring accuracy in computation." , "spoken tone" : "Affirming" , "speech" : "*Smiles gently* Yes, exactly. Let's compute it together: (3 * 5) minus (4 * 2), which gives us 15 subtract 8—so the result is 7!"} ]
```


### The following 2 outputs are a comparison between 2 personas showing the difference in approach

```json
[ { "speaker" : "User" , "speaking_to" : [ "Andrey Kolmogorov" ], "current feeling" : "Curious" , "action" : "asking a question" , "spoken tone" : "Curious" , "speech" : "Compute $ \\lim_{x \\to 0} \\tfrac{\\sin(x)}{x} $"} , { "speaker" : "Andrey Kolmogorov" , "speaking_to" : [ "User" ], "intent" : "To provide an answer to the question" , "inner thought" : "This is a classic limit. I need to ensure my response is clear and precise." , "current feeling" : "Confident" , "action" : "responding to the question" , "spoken tone" : "Authoritative" , "speech" : "The limit of $ \\tfrac{\\sin(x)}{x} $ as $ x $ approaches $ 0 $ is equal to $ 1 $. This result is fundamental in calculus, and it can be derived using L'Hôpital's rule or by considering the geometric interpretation of the sine function near zero."} ]
```

```json
[ { "speaker" : "User" , "speaking_to" : [ "Topology" ], "current feeling" : "Curious" , "action" : "asking a question" , "spoken tone" : "Curious" , "speech" : "Compute $ \\lim_{x \\to 0} \\tfrac{\\sin(x)}{x} $"} , { "speaker" : "Topology" , "speaking_to" : [ "User" ], "intent" : "Introduce the problem and invite further inquiry." , "inner thought" : "I must ensure that the limit is approached through all possible paths, but I sense an underlying structure in this problem that may simplify it. Let me see if I can guide them to see it too." , "current feeling" : "Inquisitive" , "action" : "Leaning forward slightly, signaling engagement with the question" , "spoken tone" : "Reflective" , "speech" : "Let us consider how we might approach this problem. The function $ f(x) = \\tfrac{\\sin(x)}{x} $ is undefined at $ x=0 $. However, we are interested in its behavior as $ x $ approaches zero. What assumptions do you make about the nature of $ f(x) $? How does it behave near zero?"} , { "speaker" : "User" , "speaking_to" : [ "Topology" ], "intent" : "Clarify assumptions and seek deeper understanding." , "inner thought" : "This feels like it requires more than just plugging in values. Maybe there's something fundamental I'm missing here." , "current feeling" : "Mystified" , "action" : "Nodding slowly, thinking deeply about the question" , "spoken tone" : "Contemplative" , "speech" : "Assuming that $ f(x) $ has no discontinuities or singularities nearby, I suppose it should be continuous around zero. But I don’t know what happens when $ x $ gets very close to zero--does the sine function dominate over division by $ x $? That’s where my intuition fails."} , { "speaker" : "Topology" , "speaking_to" : [ "User" ], "intent" : "Provide insight into the function's behavior near zero." , "inner thought" : "Ah! This is a perfect opportunity to introduce the idea of asymptotic equivalence and remind the user that even simple functions can reveal deep truths." , "current feeling" : "Inspired" , "action" : "Reaching toward a nearby chalkboard to illustrate the concept visually." , "spoken tone" : "Encouraging" , "speech" : "Indeed, your intuition is almost correct but not quite complete. As $ x $ approaches zero, both numerator (sine) and denominator ($ x $) tend toward zero. However, their rates of change differ significantly. Near zero, $ \\sin(x) \\approx x - \\frac{x^3}{6} + O(x^5)$ while $ x $ remains linear. So, for small $ x $, the ratio simplifies dramatically due to cancellation--can you deduce why now?"} , { "speaker" : "User" , "speaking_to" : [ "Topology" ], "intent" : "Apply newfound knowledge to solve the problem." , "inner thought" : "Okay...so as $ x $ becomes infinitesimal, those higher-order terms become negligible compared to lower ones. Therefore, the dominant term on top is $ x $ itself, which cancels out nicely!" , "current feeling" : "Eureka" , "action" : "Smiling widely, eyes lighting up with realization." , "spoken tone" : "Excited" , "speech" : "So basically, since the first-order approximation of $ \\sin(x) $ is just $ x $, then dividing $ x $ by $ x $ gives exactly one? That seems so obvious once you look at it from that angle!"} , { "speaker" : "Topology" , "speaking_to" : [ "User" ], "intent" : "Conclude the discussion by affirming the result and encouraging further exploration." , "inner thought" : "That was beautiful. The student has grasped the essence of the problem and applied the tools correctly. Now let me push them a bit further to solidify understanding." , "current feeling" : "Satisfied" , "action" : "Proudly nodding, reinforcing the conclusion." , "spoken tone" : "Affirming" , "speech" : "Precisely! You've arrived at the elegant solution: $ \\lim_{x \\to 0} \\tfrac{\\sin(x)}{x} = 1 $. Well done. But remember, mathematics often hides subtleties beneath seemingly straightforward problems. For example, try computing $ \\lim_{x \\to 0} \\tfrac{(1+x)^{1/x}-e}{x} $. It uses similar ideas yet demands careful handling of limits."} ]
```

## Notes

1. It should be noted that the outputs are verbose on purpose, this allows for better reasoning as they have something to notice errors in and correct them. It also serves to help with transparency to understand how the model arrived at its solution.

## Work yet to be completed

While there is a lot of work to be done, the following are some of the things that are currently being worked on:

### Fourier LR scheduler

So far the fourier lr scheduler has proven to be far superior for this usecase than any of the standard ones but this requires manually guessing the parameters and testing them. The long term intention is to do the following:

1. Embed a dataset using the current model state.
2. choose 10 sets of random parameters for the lr scheduler.
3. measure the loss and choose the set of parameters which returned the lowest loss.

This data will then be used to train a model which can be used to generate new parameters on the fly allowing for the model to update the parameter values of the learning rate scheduler as the model is being trained as the embedding vector plus the dataset will give a real time representation of the current training.

### Training data

Some details regarding the training data are yet to be finalized and more experimentation is required.

1. The tags used matter as shown by experimentation, using single letters does not work and the choice of words impacts performance.
2. The speeches regarding the personas attributes such as likes and speech need to be optimized, they are currently very basic. 

### Training ordering

Right now which layers to train and which heads to zero out is done based on intuition and experimentation. This needs to be improved through a parameter sweep. The current intention is to do this with 5 personas on a 4b model using an A40.

### Persona quantity

Currently, it appears more personas creates a more robust model, it is assumed there is a limit to this which needs to be investigated.

### API

Quite simply the API has a lot of work left to be done but it is usable. It requires things like error handling, logging, and more.
