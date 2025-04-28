from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

OPENROUTER_API_KEY = "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"  

class UserInput(BaseModel):
    user_word: str
    ai_word: str

@app.get('/')
async def root():
    return {'message': 'Hello World'}

generated_words = set()

generated_words = set()

@app.get("/generate-ai-word")
def generate_ai_word():
    prompt = (
        "Give me a single, random word that represents a physical object or living thing. "
        "It should be something with volume or mass, like an animal, plant, or tangible object. "
        "Do not explain or add anything. Just reply with one word."
    )

    for _ in range(5):  # Try 5 times to find a new word
        ai_word = query_llm(prompt).strip().split()[0].lower()
        if ai_word not in generated_words:
            generated_words.add(ai_word)
            return {"ai_word": ai_word}
    
    return {"error": "Couldn't generate a unique word, please try again."}

@app.post("/battle")
def battle_result(data: UserInput):
    prompt = (
        f"Imagine a real-world scenario where '{data.user_word}' and '{data.ai_word}' face off in a practical situation. "
        "Think about their physical properties, how they interact in the real world, and which one would have the most practical impact in a direct confrontation. "
        "For example, a gun would likely overcome an elephant in a battle due to its destructive power. "
        "Reply with 'Yes' or 'No' followed by a brief, realistic explanation."
    )

    result = query_llm(prompt)
    result = result.strip().lower()  # Remove leading/trailing spaces and convert to lowercase

    # Check if the result contains "yes" or "no" and return the appropriate response
    if result.startswith("yes"):
        return {"result": "yes"}
    elif result.startswith("no"):
        return {"result": "no"}
    else:
        return {"result": "error in battle result"}

def query_llm(prompt):
    headers = {
    "Authorization": f"Bearer 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",
    "Content-Type": "application/json"
    }
    payload = {
       "model": "mistralai/mixtral-8x7b-instruct",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 5
    }    
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        # Check if the response is valid
        if res.status_code == 200:
            res_data = res.json()
            print(f"Response Data: {json.dumps(res_data, indent=2)}")
            if "choices" in res_data and len(res_data["choices"]) > 0:
                return res_data["choices"][0]["message"]["content"]
            else:
                raise KeyError("'choices' not found in the response")
        else:
            raise Exception(f"API Request Failed with status code {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Error during API request: {str(e)}")
        return "Error in generating AI word"

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
