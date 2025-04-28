from core.game_logic import LinkedList, global_counter, cache, check_profanity
from core.ai_client import query_llm
from pydantic import BaseModel
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Create session linked list for guesses
session_guesses = LinkedList()

# Create set for generated AI words
generated_words = set()

class UserInput(BaseModel):
    user_word: str
    ai_word: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

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
    # 1. Check for Profanity
    if check_profanity(data.user_word):
        return {"result": "Profanity detected! Game Over."}

    # 2. Check in cache first
    cache_key = (data.user_word.lower(), data.ai_word.lower())
    if cache_key in cache:
        verdict = cache[cache_key]
    else:
        # 3. Query the LLM
        prompt = (
        f"Who would likely win in a confrontation: '{data.ai_word}' or '{data.user_word}'? "
        f"Start your response with 'Yes' if '{data.ai_word}' wins or 'No' if '{data.user_word}' wins, followed by reasoning. "
        f"Keep your reasoning brief and conclude your answer completely."
        )

    verdict = query_llm(prompt)
    verdict = verdict.strip().lower()
    cache[cache_key] = verdict  # Save to cache

    # 4. Interpret Result
    if verdict.startswith("yes"):
        # 5. Check for duplicate guess
        if not session_guesses.add_word(data.user_word.lower()):
            return {"result": "Duplicate! Game Over."}

        # 6. Update Global Counter
        global_counter[data.user_word.lower()] = global_counter.get(data.user_word.lower(), 0) + 1

        return {
            "result": "yes",
            "guess_count": global_counter[data.user_word.lower()],
            "history": session_guesses.get_history()
        }
    elif verdict.startswith("no"):
        return {"result": "no"}
    else:
        return {"result": "error in battle result"}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
