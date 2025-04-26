from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

OPENROUTER_API_KEY = "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"  

class UserInput(BaseModel):
    user_word: str
    ai_word: str

@app.get('/')
async def root():
    return {'message': 'Hello World'}

# 1. Generate random word from AI
@app.get("/generate-ai-word")
def generate_ai_word():
    prompt = (
        "Give me a single, random word that represents a physical object or living thing. "
        "It should be something with volume or mass, like an animal, plant, or tangible object. "
        "Do not explain or add anything. Just reply with one word."
    )
    ai_word = query_llm(prompt).strip().split()[0]  # Get the first word from the response
    return {"ai_word": ai_word}

# 2. Judge if user word defeats AI word
@app.post("/battle")
def battle_result(data: UserInput):
    prompt = (
       f"Imagine a real-world scenario where '{data.user_word}' and '{data.ai_word}' face off in a practical situation. "
        "Think about their physical properties, how they interact in the real world, and which one would have the most practical impact in a direct confrontation. "
        "For example, a gun would likely overcome an elephant in a battle due to its destructive power. "
        "Reply with 'Yes' or 'No' followed by a brief, realistic explanation."
    )
    result = query_llm(prompt)
    return {"result": result}

# Util to call OpenRouter
def query_llm(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 15  # Limit the response to 20 tokens (words/pieces of words)
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    return res.json()["choices"][0]["message"]["content"]
