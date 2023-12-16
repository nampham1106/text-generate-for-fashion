from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from utils import load_model
from typing import Optional

app = FastAPI()

model, tokenizer = load_model()

class GenerationInput(BaseModel):
    prompt: str
    max_length: Optional[int] = 100
    k: Optional[int] = 3
    on: Optional[int] = 3

@app.post("/generate/")
async def generate_text(data: GenerationInput):
    input_ids = tokenizer.encode(data.prompt, return_tensors="pt")

    generated_sequence = model.generate(
        input_ids=input_ids,
        max_length=data.max_length,
        num_beams=data.k,
        no_repeat_ngram_size=3,
        num_return_sequences=3,
        eos_token_id=50259,
        use_cache=True
    )

    generated_texts = []
    for i in range(data.on):
        x = generated_sequence[i]
        text = tokenizer.decode(
            x,
            skip_special_tokens=False,
            clean_up_tokenization_spaces=True,
        )
        generated_texts.append(text)

    return {"generated_texts": generated_texts}

