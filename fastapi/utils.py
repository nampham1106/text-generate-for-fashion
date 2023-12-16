from transformers import GPT2LMHeadModel, AutoTokenizer
from typing import Optional

MODEL_NAME = "./models"


def load_model():
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    return model, tokenizer


