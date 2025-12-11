import json
from json import dumps, loads
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "persona_4b_base_details_conversation"

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=False, device_map="cuda", use_fast=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=False, device_map="cuda",
                                             dtype=torch.bfloat16)
model.eval()

tokenizer.pad_token = tokenizer.eos_token


settings = {
    "do_sample": True
}


def ask(question):
    inputs = tokenizer(question, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=settings['max_new_tokens'],
            do_sample=settings['do_sample'],
            temperature=settings['temperature'],
            # top_p = 0.4,
            # top_k = 400,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)


with open("problems.json", "r") as problem_file:
    problems = loads(problem_file.read())


def create_seed(question: str, prompter: str, speaker: str, monologue: bool, tone: str = None, action: str = None):
    seed_json = {
        "speaker": "User",
        "speaking to": speaker,
        "intent": "solve problem",
        "emotion": "Curious",
        # "internal_thought": f"I must ask {speaker[0]}",
        "action": "asking a question",
        "tone": "Curious",
        "speech": question
        # "speech": "We know that (x+y)/3 = 10, z = 15, find (x+y+z)/3"
        # "speech": "if 3x - y = 12 what is the value of (8^x)/(2^y)? possible answers are a) 2^12 b) 4^4 c) 8^2 d) the value cannot be determined from the given information."
        # "speech": "prove the riemann hypothesis"

    }
    seed_json = {key: value for key, value in seed_json.items() if value is not None}
    seed_json = [seed_json]

    seed_text = dumps(seed_json, ensure_ascii=False)
    seed_text = seed_text.replace("[{", "[ {")
    seed_text = seed_text.replace("\":", "\" :")
    seed_text = seed_text.replace("{\"", "{ \"")
    seed_text = seed_text.replace("}\"", "} \"")
    seed_text = seed_text.replace("]}", "] }")
    seed_text = seed_text.replace("\",", "\" ,")
    seed_text = seed_text.replace("},", "} ,")
    seed_text = seed_text.replace("}]", "} ]")
    seed_text = seed_text.replace("[\"", "[ \"")
    seed_text = seed_text.replace("\"]", "\" ]")
    seed_text = seed_text[:len(seed_text) - 1] + ","
    return seed_text


def create_seed_from_file(problem_name: str, prompter: str, speaker: str, problems):
    monologue = True
    # if speaker == "everyone":
    #     monologue = False
    problem = problems[problem_name]
    return create_seed(speaker=speaker, monologue=monologue, question=problem["problem_statement"], prompter=prompter)


if __name__ == "__main__":
    test_results = {}
    max_new_tokens = 512 * 8
    # problem_name = "invented_dedekind_cuts"
    # problem_name = "hat_puzzle"
    # problem_name = "who_are_you"
    # problem_name = "parameter_differentiation"
    # problem_name = "teach_probability"
    problem_name = "multi_concept_math_word_problem"
    # problem_name = "factory"
    # speaker = ["Andrey Kolmogorov"]
    # speaker = ["David Hilbert"]
    # speaker = ["topology"]
    # speaker = ["richard dedekind"]
    # speaker = ["Geometry"]
    # speaker = ["albert einstein"]
    # speaker = ["hypatia"]
    speaker = ["richard dedekind", "hypatia"]
    # speaker = ["Richard Feynman"]
    # speaker = ["One", "Two"]
    # speaker = ["Leonhard Euler"]
    # speaker = ["Bernhard Riemann"]
    # speaker = ["Zara"]
    # speaker = "Seven"
    # speaker = ["everyone"]
    # speaker = ["Bob", "Jill"]
    # speaker = ["David Hilbert", "Richard Dedekind"]
    # speaker = ["David Hilbert", "Richard Dedekind", "Andrey Kolmogorov"]
    prompter = "User"
    seed = create_seed_from_file(problem_name=problem_name, prompter=prompter, speaker=speaker, problems=problems)
    settings['max_new_tokens'] = max_new_tokens
    print(f"With maximum new tokens {max_new_tokens}")
    temperature = 0.3
    settings['temperature'] = temperature
    response = ask(seed)
    response = response.strip()
    # response = response.replace('\\\\', '\\')
    print(f"Seed: {seed}")
    print(f"Max new tokens: {settings['max_new_tokens']}")
    # print(f"Response: {response.encode('utf-8').decode('unicode_escape')}")
    # print(response)
    # response = response.encode('utf-8').decode('unicode_escape')
    response = response.replace("\\n", "")
    print(response)
    response_json = json.loads(response)

    for r in response_json:
        print(f"{r['speaker']}: {r['speech']}\n")
    print("------------------------------------------------------------------------")
