from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_model(model_name: str, f32=False, enable_checkpoint=False):
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, device_map="cuda", use_fast=True,
                                              local_files_only=False, token="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",
                                              cache_dir="./hugging")
    if not f32:
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, dtype=torch.bfloat16,
                                                     device_map="cuda", local_files_only=False,
                                                     token="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",
                                                     cache_dir="./hugging")
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True,
                                                     device_map="cuda", local_files_only=False,
                                                     token="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",
                                                     cache_dir="./hugging")
    if enable_checkpoint:
        model.gradient_checkpointing_enable()

    print(model)
    return tokenizer, model