import itertools
import logging
import random

from random import shuffle, randint

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


def ask(question, model, tokenizer):
    inputs = tokenizer(question, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024 * 4,
            do_sample=True,
            temperature=0.3,
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
        # "intent": f"ask {speaker[0]}.",
        "emotion": "Curious",
        # "internal_thought": f"I must ask {speaker[0]}",
        "action": "asking a question",
        "tone": "Curious",
        "speech": question

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
    problem = problems[problem_name]
    return create_seed(speaker=speaker, monologue=monologue, question=problem["problem_statement"], prompter=prompter)


def execute_tests(model, tokenizer):
    max_new_tokens = 512 * 8
    problem_names = [
        "hat_puzzle",
        "sally",
        "multi_concept_math_word_problem",
        "factory"
    ]
    speakers = [
        "hypatia",
        "albert einstein",
        "richard dedekind"
    ]

    prompter = "User"
    for speaker in speakers:
        for problem_name in problem_names:
            try:
                seed = create_seed_from_file(problem_name=problem_name, prompter=prompter, speaker=speaker,
                                             problems=problems)
                print(f"With maximum new tokens {max_new_tokens}")
                response = ask(seed, model, tokenizer)
                response = response.strip()
                print(f"Seed: {seed}")
                response = response.replace("\\n", "")
                print(f"raw response: {response}")
                response_json = json.loads(response)
                print("formatted response")
                for r in response_json:
                    print(f"{r['speaker']}: {r['speech']}\n")

            except Exception as ex:
                print(ex)
            print("------------------------------------------------------------------------")


def reinit_head_by_idx(model, module, head_idx, reinit_k=True, reinit_q=True, reinit_v=True):
    q_proj, k_proj, v_proj = module.self_attn.q_proj, module.self_attn.k_proj, module.self_attn.v_proj
    config = {
        "k": {
            "head_dimension": k_proj.out_features // 8
        },
        "v": {
            "head_dimension": v_proj.out_features // 8
        },
        "q": {
            "head_dimension": q_proj.out_features // 32
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
        final_hidden = outputs.hidden_states[-1]
        pooled = final_hidden.mean(dim=1)
        all_embs.append(pooled.squeeze(0))
    return torch.stack(all_embs)


class FourierLR(_LRScheduler):
    def __init__(self, optimizer, num_training_steps, a1, a2, f1, f2, param_count, last_epoch=-1):
        self.num_training_steps = num_training_steps
        self.a1, self.a2, self.f1, self.f2 = a1, a2, f1, f2
        self.param_count = param_count
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


def create_optimizer_and_scheduler(model, num_training_steps, a1, a2, f1, f2, param_count: int):
    print(f"passing in {len([p for p in model.parameters() if p.requires_grad])} parameters to optimizer")
    optimizer = optim.SGD((p for p in model.parameters() if p.requires_grad))
    logger.info(f"using {num_training_steps} as the number of steps")
    scheduler = FourierLR(optimizer, num_training_steps, a1, a2, f1, f2, param_count)

    return optimizer, scheduler


class CustomTrainer(Trainer):
    def create_optimizer_and_scheduler(self, num_training_steps):
        self.optimizer, self.lr_scheduler = create_optimizer_and_scheduler(self.model, num_training_steps, a1=1,
                                                                           a2=5,
                                                                           f1=1, f2=100, param_count=500)

    def training_step(self, model, inputs, num_items_in_batch=None):
        loss = super().training_step(model, inputs, num_items_in_batch)

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
        if trunc:
            start = randint(0, len(batch["text"]) // 2)
            increase_start = 0
            for i in range(len(batch["text"]) - start - 1):
                increase_start += 1
                if batch["text"][start + increase_start] == " ":
                    increase_start += 1
                    break
            if start + increase_start < len(batch["text"]) - 100:
                start = start + increase_start
            batch["text"] = batch["text"][start:]
        tokens = tokenizer(
            batch["text"],
            padding=False,
            truncation=True,
            max_length=max_length
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


def get_maths_data():
    processed = []
    book_text = read_pdfs_from_directory("./processed")
    for text in book_text:
        processed.append({"text": text})
    return processed


def train_iteration(model, tokenizer, epoch_count: int, layers_to_train, batch_size: int, output_name: str, dataset,
                    max_length,
                    eos, heads_to_reset, reinit=True, freeze=True, trunc=False, checkpointing=True):
    if freeze:
        for layer in model.model.layers:
            for param in layer.parameters():
                param.requires_grad = False
    for idx, layer in enumerate(model.model.layers):
        if idx in layers_to_train:
            if reinit:
                for head_to_reset in heads_to_reset:
                    model = reinit_head_by_idx(model=model, module=layer, head_idx=head_to_reset, reinit_q=True,
                                               reinit_k=False, reinit_v=False)
            for j, param in enumerate(layer.parameters()):
                param.requires_grad = True

    print(f"training {len([p for p in model.parameters() if p.requires_grad])} parameters")
    print(f"performing {max_length}")
    split = get_split(dataset, tokenizer, eos, max_length, trunc)
    split.shuffle()

    training_args = TrainingArguments(
        output_dir=output_name,
        num_train_epochs=epoch_count,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        save_strategy="no",
        # eval_strategy="epoch",
        # neftune_noise_alpha=5,
        # lr_scheduler_type='cosine',
        bf16=True,
        save_only_model=False,
        dataloader_num_workers=5,
        gradient_checkpointing=checkpointing,
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
                                              fix_mistral_regex=True)
    if not f32:
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, dtype=torch.bfloat16,
                                                     device_map="cuda", local_files_only=False,
                                                     )
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True,
                                                     device_map="cuda", local_files_only=False,
                                                     token="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")
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
    "facts": lambda: get_persona_data("facts.jsonl"),
    "base": lambda: get_base_data(),
    "maths": lambda: get_maths_data(),
    "turns": lambda: get_turns(),
    "self_describe": lambda: get_persona_data("casual_conversation.jsonl")
}


def get_dataset(names):
    return sum([datasets[name]() for name in names], [])


def train_with(model, tokenizer, output_name, batch_size, max_length, trunc_max_length, training_params,
               reinit_stage, enable_checkpointing=True, trunc=True):
    if len(training_params["data"]) > 0:
        if trunc:
            model = train_iteration(model, tokenizer=tokenizer, epoch_count=training_params['epochs'],
                                    batch_size=batch_size, output_name=output_name,
                                    dataset=training_params["data"], max_length=trunc_max_length,
                                    layers_to_train=training_params['layers'], eos=training_params['eos'],
                                    heads_to_reset=training_params['heads_reinit'], reinit=reinit_stage, freeze=True,
                                    trunc=True, checkpointing=enable_checkpointing)
        model = train_iteration(model, tokenizer=tokenizer, epoch_count=training_params['epochs'],
                                batch_size=batch_size, output_name=output_name,
                                dataset=training_params["data"], max_length=max_length,
                                layers_to_train=training_params['layers'], eos=training_params['eos'],
                                heads_to_reset=training_params['heads_reinit'], reinit=False, freeze=True,
                                trunc=False, checkpointing=enable_checkpointing)
    return model


def main():
    max_length = 4096 * 2
    trunc_max_length = 1024 * 2
    epochs = 1
    enable_checkpointing = False
    heads_reinit = [1, 3, 7]
    reinit = False
    trunc = True
    # model_name = "Qwen/Qwen3-14B-Base"
    # model_name="Qwen/Qwen2.5-32B"
    model_name = "persona_14b_base_details"
    # model_name = "persona_14b_base_conversation"

    output_model = "persona_14b_base_details_conversation"
    # output_model = "persona_4b_base_details_conversation_2"
    # output_model = "persona_4b_base_2_conversation_32_33_34_35"
    dataset_names = [
        # (["base"], [3]),
        # (["habits", "likes","facts"], [11]),
        # (["speech"], [12]),
        # (["memory"], [20]),
        # (["introspection"], [30]),
        # (["habits", "likes","facts"], [12]),
        # (["habits", "likes","facts"], [13]),

        # (["speech"], [15]),
        # (["speech"], [16]),
        # (["relationship"], [17]),
        # (["relationship"], [18]),
        # (["relationship"], [19]),

        # (["introspection"], [21]),
        # (["introspection"], [22]),

        # (["memory"], [24]),
        # (["memory"], [25]),

        # (["conversation", "self_describe"], [32]),

        # (["monologue"], [37]),
        (["conversation", "self_describe"], [38]),
        (["monologue"], [39])
    ]
    tokenizer, model = load_model(model_name, enable_checkpoint=enable_checkpointing, f32=False)
    heads_reinit = [1, 3, 7]
    for i in range(1):
        for dataset in dataset_names:
            print(f"starting training on {dataset}")
            params = {
                "data": get_dataset(dataset[0]),
                "layers": dataset[1],
                "heads_reinit": heads_reinit,
                "eos": True,
                "epochs": epochs
            }
            model = train_with(model=model, tokenizer=tokenizer, output_name=output_model, batch_size=1,
                               max_length=max_length,
                               trunc_max_length=trunc_max_length,
                               training_params=params,
                               reinit_stage=reinit,
                               trunc=trunc,
                               enable_checkpointing=enable_checkpointing)
        # execute_tests(model, tokenizer)
        model.save_pretrained(output_model, safe_serialization=True)
        tokenizer.save_pretrained(output_model, safe_serialization=True)

        print("saved model")


if __name__ == "__main__":
    random.seed(42)  # ensure that all runs use the same sequence.
    main()

