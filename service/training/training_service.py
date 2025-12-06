import logging
import random

from service.training.FourierLR import FourierLR

random.seed(42)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os

from datasets import Dataset
from torch.optim import AdamW
import torch.optim as optim
from torch.optim.lr_scheduler import CyclicLR
from transformers import AutoTokenizer, TrainingArguments, AutoModelForCausalLM, \
    Trainer
import torch
from json import loads, dumps
import json


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
            "head_dimension": q_proj.out_features // 40
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




def create_optimizer_and_scheduler(model, num_training_steps, a1, a2, f1, f2, param_count: int):
    print(f"passing in {len([p for p in model.parameters() if p.requires_grad])} parameters to optimizer")
    optimizer = optim.SGD((p for p in model.parameters() if p.requires_grad))
    logger.info(f"using {num_training_steps} as the number of steps")
    scheduler = FourierLR(optimizer, num_training_steps, a1, a2, f1, f2, param_count)

    return optimizer, scheduler


class CustomTrainer(Trainer):
    def create_optimizer_and_scheduler(self, num_training_steps):
        self.optimizer, self.lr_scheduler = create_optimizer_and_scheduler(self.model, num_training_steps, a1=1,
                                                                           a2=10.0,
                                                                           f1=1, f2=300, param_count=300)

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

        nonlocal max_length
        max_length = ((max_length * 2) % (1024))
        if max_length == 0:
            max_length = 4
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
                # if i == j:
                # print(f"setting param {i}")
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






def train_with(model, tokenizer, output_name, batch_size, max_length, training_params,
               reinit_stage, enable_checkpointing=True):
    if len(training_params["data"]) > 0:
        model = train_iteration(model, tokenizer=tokenizer, epoch_count=training_params['epochs'],
                                batch_size=batch_size, output_name=output_name,
                                dataset=training_params["data"], max_length=max_length,
                                layers_to_train=training_params['layers'], eos=training_params['eos'],
                                heads_to_reset=training_params['heads_reinit'], reinit=reinit_stage, freeze=True,
                                trunc=reinit_stage, checkpointing=enable_checkpointing)
        model = train_iteration(model, tokenizer=tokenizer, epoch_count=training_params['epochs'],
                                batch_size=batch_size, output_name=output_name,
                                dataset=training_params["data"], max_length=max_length,
                                layers_to_train=training_params['layers'], eos=training_params['eos'],
                                heads_to_reset=training_params['heads_reinit'], reinit=False, freeze=True,
                                trunc=False, checkpointing=enable_checkpointing)
    return model


def main():
    max_length = 4096
    epochs = 2
    heads_reinit = [1, 5, 7, 9]
    reinit = False
    model_name = "Qwen/Qwen3-4B-Base"
    # model_name="Qwen/Qwen2.5-32B"
    # model_name = "persona_14b_base_conversation"
    # model_name = "persona_4b_base_conversation"

    output_model = "persona_4b_base"
    # output_model = "persona_14b_base_conversation"
    # output_model = "persona_4b_base_2_conversation_32_33_34_35"
    dataset_names = [
        # (["maths"], [5, 6, 7])
        # (["base"], [7]),
        # (["base"], [8]),
        (["base"], [9]),
        (["habits", "likes", "facts"], [10]),
        # (["habits", "likes", "facts"], [11]),
        # (["habits", "likes", "facts"], [12]),
        (["speech"], [11]),
        # (["speech"], [14]),
        # (["speech"], [15]),
        (["introspection"], [12]),
        # (["introspection"], [17]),
        # (["introspection"], [18]),
        # (["memory"], [19]),
        (["memory"], [20])
        # (["memory"], [21])

        # (["monologue"], [21]),
        # (["monologue"], [22]),
        # (["conversation"], [37]),
        # (["conversation"], [38]),
        # (["monologue"], [39])

    ]
    tokenizer, model = load_model(model_name, enable_checkpoint=False, f32=False)
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
                           max_length=max_length, training_params=params, reinit_stage=reinit)
    model.save_pretrained(output_model, safe_serialization=True)
    tokenizer.save_pretrained(output_model, safe_serialization=True)
    print("saved model")


if __name__ == "__main__":
    main()
