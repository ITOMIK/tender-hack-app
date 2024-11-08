from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
app = FastAPI()

# Укажите имя модели
model_name = "distilgpt2"

# Загрузка токенизатора и модели
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_response/{res}")
async def get_response(res: str):

    # Токенизация текста
    input_ids = tokenizer(res, return_tensors="pt").input_ids.to(model.device)

    # Генерация текста
    output = model.generate(input_ids, max_length=50, do_sample=True, top_p=0.9, temperature=0.7)

    # Декодирование и вывод текста
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response
